"""
routes/ai.py – AI classification, recommendation, and chat endpoints.
"""

import logging
from datetime import datetime

from flask import Blueprint, request, g

from extensions import db
from models import Complaint, ComplaintCategory, ChatMessage, Evidence, Department
from services.classification import classify_complaint, get_department_for_category
from services.ai_service import (
    get_or_create_ai_user,
    get_or_create_chat_complaint,
    generate_document_analysis,
    generate_legal_chat_response,
)
from utils.helpers import ok, err, _log_activity, allowed_file
from utils.auth import auth_required

import os
import uuid
from werkzeug.utils import secure_filename

logger = logging.getLogger("verilaw")

ai_bp = Blueprint("ai", __name__, url_prefix="/api/v1/ai")

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")


@ai_bp.route("/classify", methods=["POST"])
@auth_required
def ai_classify():
    data = request.get_json(silent=True) or {}
    desc = (data.get("description") or "").strip()
    if not desc:
        return err("description is required.", 400)
    category, confidence = classify_complaint(desc)
    return ok({"category": category, "confidence": confidence})


@ai_bp.route("/recommend", methods=["POST"])
@auth_required
def ai_recommend():
    data     = request.get_json(silent=True) or {}
    category = (data.get("category") or "").strip()
    if not category:
        return err("category is required.", 400)
    dept_name = get_department_for_category(category)
    if not dept_name:
        return err("No department recommendation for this category.", 404)
    dept = Department.query.filter_by(department_name=dept_name).first()
    return ok({
        "department":         dept_name,
        "department_details": dept.to_dict() if dept else None,
        "reason":             f"{category} complaints are handled by {dept_name}.",
        "confidence":         95.0,
    })


@ai_bp.route("/chat", methods=["POST"])
@auth_required
def ai_chat_endpoint():
    data         = request.get_json(silent=True) or {}
    message_text = (data.get("message") or "").strip()
    evidence_id  = data.get("evidence_id")
    complaint_id = data.get("complaint_id")

    if not message_text and not evidence_id:
        return err("message or evidence_id is required.", 400)

    ai_user = get_or_create_ai_user()

    if not complaint_id:
        workspace    = get_or_create_chat_complaint(g.user.user_id)
        complaint_id = workspace.complaint_id

    if message_text:
        user_msg = ChatMessage(
            sender_id=g.user.user_id,
            receiver_id=ai_user.user_id,
            content=message_text,
            complaint_id=complaint_id,
        )
        db.session.add(user_msg)
        db.session.commit()

    if evidence_id:
        ev = Evidence.query.get(evidence_id)
        if not ev:
            return err("Evidence file not found.", 404)
        # IDOR check
        comp = Complaint.query.get(ev.complaint_id)
        if comp and comp.user_id != g.user.user_id and g.user.role != "admin":
            return err("Access denied.", 403)

        reply_content = generate_document_analysis(
            file_name=ev.original_name,
            file_type=ev.file_type,
            file_size_kb=round((ev.file_size or 0) / 1024, 1),
            ocr_text=ev.ocr_text or "",
        )
    else:
        reply_content = generate_legal_chat_response(message_text)

    ai_msg = ChatMessage(
        sender_id=ai_user.user_id,
        receiver_id=g.user.user_id,
        content=reply_content,
        complaint_id=complaint_id,
    )
    db.session.add(ai_msg)
    db.session.commit()

    return ok({
        "message_id": ai_msg.message_id,
        "sender_id":  ai_msg.sender_id,
        "receiver_id":ai_msg.receiver_id,
        "content":    ai_msg.content,
        "created_at": ai_msg.created_at.isoformat(),
    })


@ai_bp.route("/chat/history", methods=["GET"])
@auth_required
def get_ai_chat_history():
    ai_user      = get_or_create_ai_user()
    me           = g.user.user_id
    complaint_id = request.args.get("complaint_id", type=int)

    q = ChatMessage.query.filter(
        ((ChatMessage.sender_id == me) & (ChatMessage.receiver_id == ai_user.user_id)) |
        ((ChatMessage.sender_id == ai_user.user_id) & (ChatMessage.receiver_id == me))
    )
    if complaint_id:
        q = q.filter_by(complaint_id=complaint_id)

    msgs          = q.order_by(ChatMessage.created_at.asc()).all()
    messages_list = [m.to_dict() for m in msgs]

    if not messages_list:
        greeting = ("Hello! I am VeriLaw AI. I can help you verify documents, detect fraud, "
                    "generate complaints, and provide legal guidance. How can I assist you today?")
        if complaint_id:
            comp = Complaint.query.get(complaint_id)
            if comp and comp.title != "AI Conversation Workspace":
                greeting = (
                    f"Welcome back! I am ready to assist you with your case: **{comp.title}** "
                    f"({comp.category.category_name if comp.category else 'General'}). "
                    "Feel free to ask legal questions or upload evidence files below."
                )
        messages_list.append({
            "message_id": 0,
            "sender_id":  ai_user.user_id,
            "receiver_id":me,
            "content":    greeting,
            "created_at": datetime.utcnow().isoformat(),
        })

    return ok({"messages": messages_list})


@ai_bp.route("/chat/threads", methods=["GET"])
@auth_required
def get_chat_threads():
    user_id    = g.user.user_id
    complaints = Complaint.query.filter_by(user_id=user_id).order_by(Complaint.updated_at.desc()).all()
    workspace  = get_or_create_chat_complaint(user_id)

    threads = [{
        "id":         workspace.complaint_id,
        "title":      "General Legal Assistant",
        "category":   "General",
        "updated_at": workspace.updated_at.isoformat(),
    }]
    for c in complaints:
        if c.complaint_id == workspace.complaint_id:
            continue
        threads.append({
            "id":         c.complaint_id,
            "title":      c.title or "Untitled Verification",
            "category":   c.category.category_name if c.category else "Unclassified",
            "updated_at": c.updated_at.isoformat(),
        })
    return ok({"threads": threads})


@ai_bp.route("/chat/threads/<int:complaint_id>", methods=["DELETE"])
@auth_required
def delete_chat_thread(complaint_id):
    comp = Complaint.query.get(complaint_id)
    if not comp:
        return err("Thread not found.", 404)
    if comp.user_id != g.user.user_id and g.user.role != "admin":
        return err("Access denied.", 403)

    ai_user = get_or_create_ai_user()
    if comp.title == "AI Conversation Workspace":
        ChatMessage.query.filter(
            ((ChatMessage.sender_id == g.user.user_id) & (ChatMessage.receiver_id == ai_user.user_id) &
             (ChatMessage.complaint_id == complaint_id)) |
            ((ChatMessage.sender_id == ai_user.user_id) & (ChatMessage.receiver_id == g.user.user_id) &
             (ChatMessage.complaint_id == complaint_id))
        ).delete()
        db.session.commit()
        return ok(message="Chat history cleared.")

    Evidence.query.filter_by(complaint_id=complaint_id).delete()
    ChatMessage.query.filter_by(complaint_id=complaint_id).delete()
    db.session.delete(comp)
    db.session.commit()
    return ok(message="Thread deleted successfully.")


@ai_bp.route("/upload", methods=["POST"])
@auth_required
def ai_upload_endpoint():
    file = request.files.get("file")
    if not file:
        return err("file is required.", 400)

    filename = file.filename
    if not filename or not allowed_file(filename):
        return err("File type not allowed.", 400)

    workspace_id = request.form.get("complaint_id", type=int)
    if workspace_id:
        workspace = Complaint.query.get(workspace_id)
        if workspace and workspace.user_id != g.user.user_id and g.user.role != "admin":
            return err("Access denied.", 403)
    else:
        workspace = get_or_create_chat_complaint(g.user.user_id)

    if not workspace:
        return err("Complaint workspace not found.", 404)

    from services.evidence_service import extract_ocr_text, infer_category
    original = secure_filename(filename)
    if not original or "." not in original:
        return err("Invalid file name.", 400)
    ext    = original.rsplit(".", 1)[1].lower()
    stored = f"{uuid.uuid4().hex}.{ext}"
    path   = os.path.join(UPLOAD_FOLDER, stored)
    file.save(path)
    size = os.path.getsize(path)

    ocr_text, _ = extract_ocr_text(original, path)
    category    = infer_category(original)

    from models import Evidence
    ev = Evidence(
        complaint_id=workspace.complaint_id,
        file_name=stored,
        original_name=original,
        file_type=ext.upper(),
        file_size=size,
        file_path=path,
        ocr_text=ocr_text,
        category=category,
    )
    db.session.add(ev)
    db.session.commit()
    _log_activity(g.user.user_id, f"Uploaded document for AI verification: {original}")

    return ok({
        "evidence_id":   ev.evidence_id,
        "complaint_id":  ev.complaint_id,
        "original_name": ev.original_name,
        "file_type":     ev.file_type,
        "file_size":     ev.file_size,
        "ocr_text":      ev.ocr_text,
    }, "Document uploaded successfully.", 201)


@ai_bp.route("/document/<int:evidence_id>", methods=["GET"])
@auth_required
def get_ai_document_details(evidence_id):
    ev = Evidence.query.get(evidence_id)
    if not ev:
        return err("Document not found.", 404)
    comp = Complaint.query.get(ev.complaint_id)
    if not comp:
        return err("Complaint not found.", 404)
    if comp.user_id != g.user.user_id and g.user.role != "admin":
        return err("Access denied.", 403)

    fraud_prob = 15.0
    confidence = 0.95
    doc_type   = ev.file_type or "Document"
    name_lower = (ev.original_name or "").lower()

    if any(kw in name_lower for kw in ("agree", "contract")):
        fraud_prob, confidence, doc_type = 92.0, 0.94, "Property Agreement"
    elif any(kw in name_lower for kw in ("invoice", "bill")):
        fraud_prob, confidence, doc_type = 64.0, 0.88, "Invoice Statement"
    elif any(kw in name_lower for kw in ("id", "pan", "aadhaar")):
        fraud_prob, confidence, doc_type = 8.0, 0.98, "Identity Verification"

    return ok({
        "evidence_id":   ev.evidence_id,
        "original_name": ev.original_name,
        "file_type":     ev.file_type,
        "file_size":     ev.file_size,
        "upload_time":   ev.upload_time.isoformat(),
        "ocr_text":      ev.ocr_text or "[No text extracted]",
        "analysis": {
            "document_type":    doc_type,
            "fraud_probability":fraud_prob,
            "confidence_score": confidence,
            "status":           "Rule-Based Heuristic Analysis (Fallback)",
            "analysis_mode":    "Rule-Based Heuristic",
        },
    })
