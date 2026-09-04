"""
routes/admin.py – Administrative management endpoints.
"""

import logging

from flask import Blueprint, request

from extensions import db
from models import User, Complaint, Evidence, GeneratedDocument, Appointment, Feedback, Notification
from utils.helpers import ok, err
from utils.auth import role_required

logger = logging.getLogger("verilaw")

admin_bp = Blueprint("admin", __name__, url_prefix="/api/v1/admin")


@admin_bp.route("/stats", methods=["GET"])
@role_required("admin")
def admin_stats():
    return ok({
        "total_users":        User.query.count(),
        "total_citizens":     User.query.filter_by(role="citizen").count(),
        "total_lawyers":      User.query.filter_by(role="lawyer").count(),
        "total_admins":       User.query.filter_by(role="admin").count(),
        "total_complaints":   Complaint.query.count(),
        "total_evidence":     Evidence.query.count(),
        "total_documents":    GeneratedDocument.query.count(),
        "total_appointments": Appointment.query.count(),
        "total_feedback":     Feedback.query.count(),
    })


@admin_bp.route("/users", methods=["GET"])
@role_required("admin")
def admin_list_users():
    page  = request.args.get("page",  1,  type=int)
    limit = min(request.args.get("limit", 20, type=int), 100)
    role  = request.args.get("role")
    q     = User.query
    if role:
        q = q.filter_by(role=role)
    total = q.count()
    users = q.order_by(User.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    return ok({"total": total, "page": page, "data": [u.to_dict() for u in users]})


@admin_bp.route("/users/<int:user_id>", methods=["GET"])
@role_required("admin")
def admin_get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return err("User not found.", 404)
    return ok(user.to_dict())


@admin_bp.route("/users/<int:user_id>/toggle-active", methods=["PUT"])
@role_required("admin")
def admin_toggle_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return err("User not found.", 404)
    user.is_active = not user.is_active
    db.session.commit()
    return ok({"is_active": user.is_active},
              f"User {'activated' if user.is_active else 'deactivated'}.")


@admin_bp.route("/users/<int:user_id>/role", methods=["PUT"])
@role_required("admin")
def admin_change_role(user_id):
    user     = User.query.get(user_id)
    if not user:
        return err("User not found.", 404)
    data     = request.get_json(silent=True) or {}
    new_role = data.get("role")
    if new_role not in ("citizen", "lawyer", "admin"):
        return err("Valid roles: citizen, lawyer, admin.", 422)
    user.role = new_role
    db.session.commit()
    return ok({"role": user.role}, "User role updated.")


@admin_bp.route("/complaints", methods=["GET"])
@role_required("admin")
def admin_list_complaints():
    page   = request.args.get("page",   1,  type=int)
    limit  = min(request.args.get("limit", 20, type=int), 100)
    status = request.args.get("status")
    q      = Complaint.query
    if status:
        q = q.filter_by(status=status)
    total      = q.count()
    complaints = q.order_by(Complaint.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    return ok({"total": total, "page": page, "data": [c.to_dict() for c in complaints]})


@admin_bp.route("/notify-all", methods=["POST"])
@role_required("admin")
def admin_notify_all():
    data    = request.get_json(silent=True) or {}
    title   = (data.get("title")   or "System Announcement").strip()
    message = (data.get("message") or "").strip()
    if not message:
        return err("message is required.", 400)
    users = User.query.filter_by(is_active=True).all()
    for u in users:
        db.session.add(Notification(user_id=u.user_id, title=title, message=message))
    db.session.commit()
    return ok({"notified": len(users)}, "Broadcast notification sent.")
