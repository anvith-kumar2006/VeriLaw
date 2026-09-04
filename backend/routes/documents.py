"""
routes/documents.py – Document generation and download.
"""

import os
import uuid
import logging

from flask import Blueprint, request, g, send_from_directory

from extensions import db
from models import Complaint, ComplaintCategory, Department, Evidence, GeneratedDocument
from services.document_service import generate_pdf, generate_html
from utils.helpers import ok, err, _log_activity
from utils.auth import auth_required

logger = logging.getLogger("verilaw")

documents_bp = Blueprint("documents", __name__, url_prefix="/api/v1/documents")

GENERATED_DOCS_FOLDER = os.path.join(os.getcwd(), "generated_documents")


@documents_bp.route("/generate", methods=["POST"])
@auth_required
def generate_document():
    data         = request.get_json(silent=True) or {}
    complaint_id = data.get("complaint_id")
    doc_type     = (data.get("document_type") or "PDF").upper()

    if not complaint_id:
        return err("complaint_id is required.", 400)
    complaint = Complaint.query.get(complaint_id)
    if not complaint:
        return err("Complaint not found.", 404)
    if complaint.user_id != g.user.user_id and g.user.role != "admin":
        return err("Access denied.", 403)
    if doc_type not in ("PDF", "HTML"):
        return err("Supported types: PDF, HTML.", 400)

    user       = g.user
    category   = ComplaintCategory.query.get(complaint.category_id) if complaint.category_id else None
    department = Department.query.get(complaint.department_id)      if complaint.department_id else None
    evidence   = Evidence.query.filter_by(complaint_id=complaint_id).all()

    stamp     = uuid.uuid4().hex[:8]
    file_name = f"complaint_{complaint_id}_{stamp}.{doc_type.lower()}"
    file_path = os.path.join(GENERATED_DOCS_FOLDER, file_name)

    if doc_type == "HTML":
        generate_html(file_path, user, complaint, category, department, evidence)
    else:
        generate_pdf(file_path, user, complaint, category, department, evidence)

    gen_doc = GeneratedDocument(
        complaint_id=complaint_id,
        user_id=user.user_id,
        document_type=doc_type,
        file_path=file_path,
    )
    db.session.add(gen_doc)
    complaint.status = "Completed"
    db.session.commit()

    _log_activity(user.user_id, f"Document Generated: {doc_type} for complaint {complaint_id}")
    return ok({
        "document_id":  gen_doc.document_id,
        "download_url": f"/api/v1/documents/download/{gen_doc.document_id}",
    }, "Document generated successfully.", 201)


@documents_bp.route("/download/<int:document_id>", methods=["GET"])
@auth_required
def download_document(document_id):
    gen_doc = GeneratedDocument.query.get(document_id)
    if not gen_doc:
        return err("Document not found.", 404)
    if gen_doc.user_id != g.user.user_id and g.user.role != "admin":
        return err("Access denied.", 403)
    return send_from_directory(
        GENERATED_DOCS_FOLDER,
        os.path.basename(gen_doc.file_path),
        as_attachment=True,
    )


@documents_bp.route("", methods=["GET"])
@auth_required
def list_documents():
    q = GeneratedDocument.query
    if g.user.role != "admin":
        q = q.filter_by(user_id=g.user.user_id)
    docs = q.order_by(GeneratedDocument.generated_at.desc()).all()
    return ok([d.to_dict() for d in docs])


@documents_bp.route("/<int:document_id>", methods=["DELETE"])
@auth_required
def delete_document(document_id):
    gen_doc = GeneratedDocument.query.get(document_id)
    if not gen_doc:
        return err("Document not found.", 404)
    if gen_doc.user_id != g.user.user_id and g.user.role != "admin":
        return err("Access denied.", 403)
    try:
        if gen_doc.file_path and os.path.exists(gen_doc.file_path):
            os.remove(gen_doc.file_path)
    except OSError:
        pass
    db.session.delete(gen_doc)
    db.session.commit()
    return ok(message="Document deleted successfully.")
