"""
routes/chat.py – Human-to-human chat messaging.
"""

import logging

from flask import Blueprint, request, g

from extensions import db
from models import ChatMessage, User
from utils.helpers import ok, err, _notify
from utils.auth import auth_required

logger = logging.getLogger("verilaw")

chat_bp = Blueprint("chat", __name__, url_prefix="/api/v1/chat")


@chat_bp.route("/send", methods=["POST"])
@auth_required
def send_message():
    data         = request.get_json(silent=True) or {}
    receiver_id  = data.get("receiver_id")
    content      = (data.get("content") or "").strip()
    complaint_id = data.get("complaint_id")

    if not receiver_id or not content:
        return err("receiver_id and content are required.", 400)
    if not User.query.get(receiver_id):
        return err("Receiver not found.", 404)

    msg = ChatMessage(
        sender_id=g.user.user_id,
        receiver_id=receiver_id,
        content=content,
        complaint_id=complaint_id,
    )
    db.session.add(msg)
    db.session.commit()
    _notify(receiver_id, "New Message",
            f"You have a new message from {g.user.full_name}.", "info")
    return ok(msg.to_dict(), "Message sent.", 201)


@chat_bp.route("/<int:other_user_id>", methods=["GET"])
@auth_required
def get_chat(other_user_id):
    me    = g.user.user_id
    page  = request.args.get("page",  1,  type=int)
    limit = min(request.args.get("limit", 20, type=int), 100)

    msgs = ChatMessage.query.filter(
        ((ChatMessage.sender_id == me) & (ChatMessage.receiver_id == other_user_id)) |
        ((ChatMessage.sender_id == other_user_id) & (ChatMessage.receiver_id == me))
    ).order_by(ChatMessage.created_at.desc()).offset((page - 1) * limit).limit(limit).all()

    unread = [m for m in msgs if m.receiver_id == me and not m.is_read]
    for m in unread:
        m.is_read = True
    if unread:
        db.session.commit()

    return ok({"messages": [m.to_dict() for m in reversed(msgs)]})


@chat_bp.route("/unread", methods=["GET"])
@auth_required
def unread_count():
    count = ChatMessage.query.filter_by(receiver_id=g.user.user_id, is_read=False).count()
    return ok({"unread_count": count})
