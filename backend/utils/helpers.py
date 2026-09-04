"""
utils/helpers.py – Shared response helpers, file utilities, and internal helpers.
"""

import os
import logging

from flask import jsonify, request, g
from flask_jwt_extended import get_jwt_identity

logger = logging.getLogger("verilaw")

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "pdf", "mp3", "wav"}


# ──────────────────────────────────────────────────────────────────────
# RESPONSE HELPERS
# ──────────────────────────────────────────────────────────────────────

def ok(data=None, message="Success", code=200):
    body = {"success": True, "message": message}
    if data is not None:
        body["data"] = data
    return jsonify(body), code


def err(message="Error", code=400, errors=None):
    body = {"success": False, "message": message}
    if errors:
        body["errors"] = errors
    return jsonify(body), code


# ──────────────────────────────────────────────────────────────────────
# FILE UTILITIES
# ──────────────────────────────────────────────────────────────────────

def allowed_file(filename):
    """Return True if the file extension is in the allowed set."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ──────────────────────────────────────────────────────────────────────
# INTERNAL HELPERS
# ──────────────────────────────────────────────────────────────────────

def _log_activity(user_id, activity):
    """Log a user activity. Silently continues on failure."""
    try:
        # Import here to avoid circular imports at module load time
        from extensions import db
        from models import ActivityLog
        entry = ActivityLog(
            user_id=user_id,
            activity=activity,
            ip_address=request.remote_addr,
            user_agent=(request.headers.get("User-Agent") or "")[:500],
        )
        db.session.add(entry)
        db.session.commit()
    except Exception as exc:
        logger.warning("Activity log failed (user_id=%s): %s", user_id, exc)
        try:
            from extensions import db
            db.session.rollback()
        except Exception:
            pass


def _notify(user_id, title, message, ntype="info"):
    """Create an in-app notification. Silently continues on failure."""
    try:
        from extensions import db
        from models import Notification
        notif = Notification(user_id=user_id, title=title, message=message, type=ntype)
        db.session.add(notif)
        db.session.commit()
    except Exception as exc:
        logger.warning("Notification failed (user_id=%s): %s", user_id, exc)
        try:
            from extensions import db
            db.session.rollback()
        except Exception:
            pass


def _current_user():
    """Return the authenticated User object from JWT identity, or None."""
    try:
        from models import User
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or not user.is_active:
            return None
        return user
    except Exception as exc:
        logger.warning("_current_user failed: %s", exc)
        return None
