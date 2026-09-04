"""
utils/auth.py – JWT authentication and role-based access decorators.
"""

import logging
from functools import wraps

from flask import g
from flask_jwt_extended import jwt_required

from utils.helpers import err, _current_user

logger = logging.getLogger("verilaw")

# In-memory JWT blacklist for revoked tokens (per-process; resets on restart).
# For production with multiple workers, use Redis or DB-backed storage.
_revoked_tokens: set = set()


def revoke_token(jti: str) -> None:
    """Add a JWT ID to the revoked set."""
    _revoked_tokens.add(jti)


def is_token_revoked(jti: str) -> bool:
    """Return True if the JWT has been revoked."""
    return jti in _revoked_tokens


def auth_required(fn):
    """JWT required + active-user check."""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        from flask_jwt_extended import get_jwt
        jti = get_jwt().get("jti")
        if jti and is_token_revoked(jti):
            return err("Token has been revoked. Please log in again.", 401)
        user = _current_user()
        if not user:
            return err("User not found or account deactivated.", 401)
        g.user = user
        return fn(*args, **kwargs)
    return wrapper


def role_required(*roles):
    """JWT required + role check."""
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            from flask_jwt_extended import get_jwt
            jti = get_jwt().get("jti")
            if jti and is_token_revoked(jti):
                return err("Token has been revoked. Please log in again.", 401)
            user = _current_user()
            if not user:
                return err("User not found or account deactivated.", 401)
            if user.role not in roles:
                return err("Access forbidden: insufficient permissions.", 403)
            g.user = user
            return fn(*args, **kwargs)
        return wrapper
    return decorator
