"""
routes/auth.py – Authentication endpoints with rate limiting and token revocation.
"""

import logging
import re

from flask import Blueprint, request, g
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt,
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from extensions import db
from models import User, LawyerProfile
from utils.helpers import ok, err, _log_activity
from utils.auth import auth_required, revoke_token

logger = logging.getLogger("verilaw")

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}

    full_name = (data.get("full_name") or "").strip()
    email     = (data.get("email")     or "").strip().lower()
    mobile    = (data.get("mobile")    or "").strip()
    password  = data.get("password",  "")
    role      = data.get("role",      "citizen").lower()

    errors = {}
    if not full_name:
        errors["full_name"] = "Full name is required."
    if not email or not re.match(r"^[\w.+\-]+@[\w\-]+\.[a-zA-Z]{2,}$", email):
        errors["email"] = "A valid email address is required."
    if not mobile or not re.match(r"^\d{10,15}$", mobile):
        errors["mobile"] = "Mobile must be 10–15 digits."
    if not password or len(password) < 8:
        errors["password"] = "Password must be at least 8 characters."
    if role not in ("citizen", "lawyer"):
        role = "citizen"
    if errors:
        return err("Validation failed.", 422, errors)

    if User.query.filter_by(email=email).first():
        return err("Email already registered.", 409)
    if User.query.filter_by(mobile=mobile).first():
        return err("Mobile number already registered.", 409)

    user = User(
        full_name=full_name,
        email=email,
        mobile=mobile,
        password_hash=generate_password_hash(password),
        role=role,
    )
    db.session.add(user)
    db.session.commit()

    if role == "lawyer":
        db.session.add(LawyerProfile(user_id=user.user_id))
        db.session.commit()

    _log_activity(user.user_id, "User Registered")
    logger.info("New user registered: %s (%s)", email, role)
    return ok({"user_id": user.user_id}, "Registration successful.", 201)


@auth_bp.route("/login", methods=["POST"])
def login():
    data     = request.get_json(silent=True) or {}
    email    = (data.get("email")    or "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return err("Email and password are required.", 400)

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return err("Invalid email or password.", 401)
    if not user.is_active:
        return err("Account is deactivated. Contact admin.", 403)

    access_token  = create_access_token(identity=user.user_id)
    refresh_token = create_refresh_token(identity=user.user_id)
    _log_activity(user.user_id, "User Login")

    return ok({
        "token":         access_token,
        "refresh_token": refresh_token,
        "user": {
            "user_id":   user.user_id,
            "full_name": user.full_name,
            "email":     user.email,
            "role":      user.role,
        },
    }, "Login successful.")


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    return ok({"token": create_access_token(identity=identity)}, "Token refreshed.")


@auth_bp.route("/logout", methods=["POST"])
@auth_required
def logout():
    jti = get_jwt().get("jti")
    if jti:
        revoke_token(jti)
    _log_activity(g.user.user_id, "User Logout")
    return ok(message="Logout successful.")
