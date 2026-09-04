"""
routes/users.py – User profile and lawyer profile endpoints.
"""

import re
import logging

from flask import Blueprint, request, g
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from models import User, LawyerProfile
from utils.helpers import ok, err, _log_activity
from utils.auth import auth_required, role_required

logger = logging.getLogger("verilaw")

users_bp = Blueprint("users", __name__, url_prefix="/api/v1")


# ──────────────────────────────────────────────────────────────────────
# PROFILE
# ──────────────────────────────────────────────────────────────────────

@users_bp.route("/profile", methods=["GET"])
@auth_required
def get_profile():
    return ok(g.user.to_dict())


@users_bp.route("/profile", methods=["PUT"])
@auth_required
def update_profile():
    data      = request.get_json(silent=True) or {}
    user      = g.user
    full_name = (data.get("full_name") or "").strip()
    mobile    = (data.get("mobile")    or "").strip()

    if not full_name:
        return err("Full name is required.", 422)
    if mobile and not re.match(r"^\d{10,15}$", mobile):
        return err("Mobile must be 10–15 digits.", 422)
    if mobile and mobile != user.mobile:
        if User.query.filter(User.mobile == mobile, User.user_id != user.user_id).first():
            return err("Mobile number already in use.", 409)

    user.full_name = full_name
    if mobile:
        user.mobile = mobile
    db.session.commit()
    _log_activity(user.user_id, "Profile Updated")
    return ok(message="Profile updated successfully.")


@users_bp.route("/profile/password", methods=["PUT"])
@auth_required
def change_password():
    data             = request.get_json(silent=True) or {}
    user             = g.user
    current_password = data.get("current_password", "")
    new_password     = data.get("new_password",     "")

    if not check_password_hash(user.password_hash, current_password):
        return err("Current password is incorrect.", 400)
    if len(new_password) < 8:
        return err("New password must be at least 8 characters.", 422)

    user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    _log_activity(user.user_id, "Password Changed")
    return ok(message="Password changed successfully.")


# ──────────────────────────────────────────────────────────────────────
# LAWYER PROFILES
# ──────────────────────────────────────────────────────────────────────

@users_bp.route("/lawyers", methods=["GET"])
def list_lawyers():
    page           = request.args.get("page",           1,  type=int)
    limit          = min(request.args.get("limit",      10, type=int), 50)
    specialization = request.args.get("specialization")
    location       = request.args.get("location")

    q = db.session.query(LawyerProfile, User).join(
        User, LawyerProfile.user_id == User.user_id
    ).filter(User.is_active == True, LawyerProfile.availability == True)

    if specialization:
        q = q.filter(LawyerProfile.specialization.ilike(f"%{specialization}%"))
    if location:
        q = q.filter(LawyerProfile.location.ilike(f"%{location}%"))

    total = q.count()
    rows  = q.order_by(LawyerProfile.rating.desc()).offset((page - 1) * limit).limit(limit).all()

    lawyers = []
    for lp, u in rows:
        d = lp.to_dict()
        d["full_name"] = u.full_name
        d["email"]     = u.email
        lawyers.append(d)

    return ok({"page": page, "limit": limit, "total": total, "lawyers": lawyers})


@users_bp.route("/lawyers/<int:lawyer_id>", methods=["GET"])
def get_lawyer(lawyer_id):
    lp = LawyerProfile.query.filter_by(user_id=lawyer_id).first()
    if not lp:
        return err("Lawyer not found.", 404)
    u = User.query.get(lawyer_id)
    if not u:
        return err("Lawyer not found.", 404)
    d = lp.to_dict()
    d["full_name"] = u.full_name
    d["email"]     = u.email
    return ok(d)


@users_bp.route("/lawyers/profile", methods=["PUT"])
@role_required("lawyer")
def update_lawyer_profile():
    data = request.get_json(silent=True) or {}
    lp   = LawyerProfile.query.filter_by(user_id=g.user.user_id).first()
    if not lp:
        lp = LawyerProfile(user_id=g.user.user_id)
        db.session.add(lp)

    for field in ("bar_council_number", "specialization", "about", "location"):
        if field in data:
            setattr(lp, field, data[field])
    if "experience_years" in data:
        lp.experience_years = int(data["experience_years"])
    if "availability" in data:
        lp.availability = bool(data["availability"])

    db.session.commit()
    return ok(lp.to_dict(), "Lawyer profile updated.")


# ──────────────────────────────────────────────────────────────────────
# CATEGORIES & DEPARTMENTS
# ──────────────────────────────────────────────────────────────────────

@users_bp.route("/categories", methods=["GET"])
def get_categories():
    from models import ComplaintCategory
    cats = ComplaintCategory.query.order_by(ComplaintCategory.category_name).all()
    return ok([c.to_dict() for c in cats])


@users_bp.route("/departments", methods=["GET"])
def get_departments():
    from models import Department
    depts = Department.query.order_by(Department.department_name).all()
    return ok([d.to_dict() for d in depts])


@users_bp.route("/departments/<int:department_id>", methods=["GET"])
def get_department(department_id):
    from models import Department
    dept = Department.query.get(department_id)
    if not dept:
        return err("Department not found.", 404)
    return ok(dept.to_dict())
