"""
routes/reports.py – Reporting and feedback endpoints.
"""

import logging

from flask import Blueprint, request, g
from sqlalchemy import func

from extensions import db
from models import (
    Complaint, ComplaintCategory, Department, User,
    Evidence, GeneratedDocument, ActivityLog, Feedback,
)
from utils.helpers import ok, err
from utils.auth import auth_required, role_required

logger = logging.getLogger("verilaw")

reports_bp = Blueprint("reports", __name__, url_prefix="/api/v1")


# ──────────────────────────────────────────────────────────────────────
# REPORTS
# ──────────────────────────────────────────────────────────────────────

@reports_bp.route("/reports/summary", methods=["GET"])
@auth_required
def report_summary():
    user = g.user
    if user.role == "admin":
        by_status = db.session.query(Complaint.status, func.count()).group_by(Complaint.status).all()
        by_cat    = db.session.query(
            ComplaintCategory.category_name, func.count(Complaint.complaint_id)
        ).join(Complaint, Complaint.category_id == ComplaintCategory.category_id).group_by(
            ComplaintCategory.category_name
        ).all()
        return ok({
            "total_users":      User.query.count(),
            "total_complaints": Complaint.query.count(),
            "total_evidence":   Evidence.query.count(),
            "by_status":        {s: c for s, c in by_status},
            "by_category":      {s: c for s, c in by_cat},
        })
    else:
        by_status = db.session.query(Complaint.status, func.count()).filter(
            Complaint.user_id == user.user_id
        ).group_by(Complaint.status).all()
        return ok({
            "total_complaints": Complaint.query.filter_by(user_id=user.user_id).count(),
            "total_documents":  GeneratedDocument.query.filter_by(user_id=user.user_id).count(),
            "by_status":        {s: c for s, c in by_status},
        })


@reports_bp.route("/reports/department-stats", methods=["GET"])
@role_required("admin")
def report_department_stats():
    stats = db.session.query(
        Department.department_name, func.count(Complaint.complaint_id)
    ).join(Complaint, Complaint.department_id == Department.department_id).group_by(
        Department.department_name
    ).all()
    return ok({"department_stats": {n: c for n, c in stats}})


@reports_bp.route("/reports/activity", methods=["GET"])
@role_required("admin")
def report_activity():
    page  = request.args.get("page",  1,  type=int)
    limit = min(request.args.get("limit", 20, type=int), 100)
    logs  = ActivityLog.query.order_by(
        ActivityLog.created_at.desc()
    ).offset((page - 1) * limit).limit(limit).all()
    return ok({"page": page, "data": [l.to_dict() for l in logs]})


# ──────────────────────────────────────────────────────────────────────
# FEEDBACK
# ──────────────────────────────────────────────────────────────────────

@reports_bp.route("/feedback", methods=["POST"])
@auth_required
def submit_feedback():
    data         = request.get_json(silent=True) or {}
    rating       = data.get("rating")
    comment      = (data.get("comment") or "").strip()
    complaint_id = data.get("complaint_id")

    if not isinstance(rating, int) or not (1 <= rating <= 5):
        return err("Rating must be an integer between 1 and 5.", 422)

    fb = Feedback(
        user_id=g.user.user_id,
        complaint_id=complaint_id,
        rating=rating,
        comment=comment,
    )
    db.session.add(fb)
    db.session.commit()
    return ok(fb.to_dict(), "Feedback submitted.", 201)


@reports_bp.route("/feedback", methods=["GET"])
@auth_required
def list_feedback():
    if g.user.role == "admin":
        fbs = Feedback.query.order_by(Feedback.created_at.desc()).all()
    else:
        fbs = Feedback.query.filter_by(user_id=g.user.user_id).all()
    return ok([f.to_dict() for f in fbs])
