"""Complaint timeline generation endpoint."""

from flask import Blueprint, g, request

from extensions import db
from models import Complaint, Evidence
from utils.auth import auth_required
from utils.helpers import ok, err

timeline_bp = Blueprint("timeline", __name__, url_prefix="/api/v1/timeline")


@timeline_bp.route("/generate", methods=["POST"])
@auth_required
def generate_timeline():
    data = request.get_json(silent=True) or {}
    complaint_id = data.get("complaint_id")
    if not complaint_id:
        return err("complaint_id is required.", 400)
    complaint = Complaint.query.get(complaint_id)
    if not complaint:
        return err("Complaint not found.", 404)
    if complaint.user_id != g.user.user_id and g.user.role != "admin":
        return err("Access denied.", 403)

    evidence_list = Evidence.query.filter_by(complaint_id=complaint_id).order_by(Evidence.upload_time).all()
    timeline = []
    if complaint.incident_date:
        timeline.append({"date": complaint.incident_date.isoformat(), "event": "Incident Date"})
    for evidence in evidence_list:
        timeline.append({"date": evidence.upload_time.date().isoformat(),
                         "event": f"Evidence uploaded: {evidence.original_name}"})
    timeline.append({"date": complaint.created_at.date().isoformat(), "event": "Complaint Filed"})
    timeline.sort(key=lambda item: item["date"])
    return ok({"timeline": timeline})