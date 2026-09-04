"""
routes/notifications.py – Notification management.
"""

import logging

from flask import Blueprint, request, g

from extensions import db
from models import Notification
from utils.helpers import ok, err
from utils.auth import auth_required

logger = logging.getLogger("verilaw")

notifications_bp = Blueprint("notifications", __name__, url_prefix="/api/v1/notifications")


@notifications_bp.route("", methods=["GET"])
@auth_required
def get_notifications():
    page    = request.args.get("page",  1,  type=int)
    limit   = min(request.args.get("limit", 10, type=int), 50)
    is_read = request.args.get("is_read")

    q = Notification.query.filter_by(user_id=g.user.user_id)
    if is_read is not None:
        q = q.filter_by(is_read=(is_read.lower() == "true"))

    total  = q.count()
    notifs = q.order_by(Notification.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    return ok({"total": total, "page": page, "data": [n.to_dict() for n in notifs]})


@notifications_bp.route("/<int:notification_id>/read", methods=["PUT"])
@auth_required
def mark_notification_read(notification_id):
    notif = Notification.query.get(notification_id)
    if not notif or notif.user_id != g.user.user_id:
        return err("Notification not found.", 404)
    notif.is_read = True
    db.session.commit()
    return ok(message="Notification marked as read.")


@notifications_bp.route("/read-all", methods=["PUT"])
@auth_required
def mark_all_read():
    Notification.query.filter_by(user_id=g.user.user_id, is_read=False).update({"is_read": True})
    db.session.commit()
    return ok(message="All notifications marked as read.")
