"""
routes/evidence.py – Evidence upload, list, download, and delete.
"""

import os
import uuid
import logging

from flask import Blueprint, request, g, send_from_directory
from werkzeug.utils import secure_filename

from extensions import db
from models import Evidence, Complaint
from services.evidence_service import extract_ocr_text
from utils.helpers import ok, err, _log_activity, allowed_file
from utils.auth import auth_required

logger = logging.getLogger("verilaw")

evidence_bp = Blueprint("evidence", __name__, url_prefix="/api/v1/evidence")

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")


@evidence_bp.route("/upload", methods=["POST"])
@auth_required
def upload_evidence():
    complaint_id = request.form.get("complaint_id", type=int)
    if not complaint_id:
        return err("complaint_id is required.", 400)

    complaint = Complaint.query.get(complaint_id)
    if not complaint:
        return err("Complaint not found.", 404)
    if complaint.user_id != g.user.user_id and g.user.role != "admin":
        return err("Access denied.", 403)
    if Evidence.query.filter_by(complaint_id=complaint_id).count() >= 10:
        return err("Maximum 10 files per complaint.", 400)

    files    = request.files.getlist("files")
    uploaded = 0
    failed   = 0

    for f in files:
        filename = f.filename if f else None
        if f and filename and allowed_file(filename):
            original = secure_filename(filename)
            if not original or "." not in original:
                failed += 1
                continue
            ext    = original.rsplit(".", 1)[1].lower()
            stored = f"{uuid.uuid4().hex}.{ext}"
            path   = os.path.join(UPLOAD_FOLDER, stored)
            f.save(path)
            size = os.path.getsize(path)

            ocr_text, _ = extract_ocr_text(original, path)

            ev = Evidence(
                complaint_id=complaint_id,
                file_name=stored,
                original_name=original,
                file_type=ext.upper(),
                file_size=size,
                file_path=path,
                ocr_text=ocr_text if ocr_text else None,
            )
            db.session.add(ev)
            uploaded += 1
        else:
            failed += 1

    db.session.commit()
    _log_activity(g.user.user_id, f"Evidence Uploaded: {uploaded} files for complaint {complaint_id}")
    return ok({"uploaded_files": uploaded, "failed_files": failed}, "Evidence uploaded.", 201)


@evidence_bp.route("/<int:complaint_id>", methods=["GET"])
@auth_required
def list_evidence(complaint_id):
    complaint = Complaint.query.get(complaint_id)
    if not complaint:
        return err("Complaint not found.", 404)
    if complaint.user_id != g.user.user_id and g.user.role != "admin":
        return err("Access denied.", 403)
    ev_list = Evidence.query.filter_by(complaint_id=complaint_id).all()
    return ok([e.to_dict() for e in ev_list])


@evidence_bp.route("/<int:evidence_id>", methods=["DELETE"])
@auth_required
def delete_evidence(evidence_id):
    ev = Evidence.query.get(evidence_id)
    if not ev:
        return err("Evidence not found.", 404)
    complaint = Complaint.query.get(ev.complaint_id)
    if not complaint:
        return err("Complaint not found.", 404)
    if complaint.user_id != g.user.user_id and g.user.role != "admin":
        return err("Access denied.", 403)
    try:
        if ev.file_path and os.path.exists(ev.file_path):
            os.remove(ev.file_path)
    except OSError:
        pass
    db.session.delete(ev)
    db.session.commit()
    return ok(message="Evidence deleted successfully.")


@evidence_bp.route("/download/<int:evidence_id>", methods=["GET"])
@auth_required
def download_evidence(evidence_id):
    ev = Evidence.query.get(evidence_id)
    if not ev:
        return err("Evidence not found.", 404)
    complaint = Complaint.query.get(ev.complaint_id)
    if not complaint:
        return err("Complaint not found.", 404)
    if complaint.user_id != g.user.user_id and g.user.role != "admin":
        return err("Access denied.", 403)
    return send_from_directory(
        UPLOAD_FOLDER, ev.file_name,
        as_attachment=True, download_name=ev.original_name,
    )
