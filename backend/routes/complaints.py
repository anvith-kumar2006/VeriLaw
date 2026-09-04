"""
routes/complaints.py – Complaint CRUD and category override.
"""

import logging
from datetime import datetime

from flask import Blueprint, request, g

from extensions import db
from models import Complaint, ComplaintCategory, Department
from services.classification import classify_complaint, get_department_for_category
from utils.helpers import ok, err, _log_activity, _notify
from utils.auth import auth_required

logger = logging.getLogger("verilaw")

complaints_bp = Blueprint("complaints", __name__, url_prefix="/api/v1/complaints")


@complaints_bp.route("", methods=["POST"])
@auth_required
def create_complaint():
    data        = request.get_json(silent=True) or {}
    title       = (data.get("title")       or "").strip()
    description = (data.get("description") or "").strip()
    state       = (data.get("state")       or "").strip()
    district    = (data.get("district")    or "").strip()
    inc_date    = data.get("incident_date")

    errors = {}
    if not title or len(title) > 200:
        errors["title"] = "Title is required (max 200 chars)."
    if not description or len(description) < 30:
        errors["description"] = "Description must be at least 30 characters."
    if not state:
        errors["state"] = "State is required."
    if not district:
        errors["district"] = "District is required."
    if errors:
        return err("Validation failed.", 422, errors)

    incident_date = None
    if inc_date:
        try:
            incident_date = datetime.strptime(inc_date, "%Y-%m-%d").date()
        except ValueError:
            return err("Invalid incident_date – use YYYY-MM-DD.", 422)

    cat_name, confidence = classify_complaint(f"{title} {description}")
    category   = ComplaintCategory.query.filter_by(category_name=cat_name).first()
    dept_name  = get_department_for_category(cat_name)
    department = Department.query.filter_by(department_name=dept_name).first()

    complaint = Complaint(
        user_id=g.user.user_id,
        category_id=category.category_id if category else None,
        department_id=department.department_id if department else None,
        title=title,
        description=description,
        state=state,
        district=district,
        incident_date=incident_date,
        ai_confidence=confidence,
        status="Draft",
    )
    db.session.add(complaint)
    db.session.commit()

    _notify(
        g.user.user_id,
        "Complaint Filed",
        f'Your complaint "{title}" was classified as "{cat_name}" ({confidence}% confidence).',
        "success",
    )
    return ok({
        "complaint_id":  complaint.complaint_id,
        "status":        complaint.status,
        "category":      cat_name,
        "department":    dept_name,
        "ai_confidence": confidence,
    }, "Complaint created successfully.", 201)


@complaints_bp.route("", methods=["GET"])
@auth_required
def list_complaints():
    user   = g.user
    page   = request.args.get("page",   1,  type=int)
    limit  = min(request.args.get("limit", 10, type=int), 50)
    status = request.args.get("status")
    cat    = request.args.get("category")

    q = Complaint.query
    if user.role != "admin":
        q = q.filter_by(user_id=user.user_id)
    if status:
        q = q.filter_by(status=status)
    if cat:
        cat_obj = ComplaintCategory.query.filter_by(category_name=cat).first()
        if cat_obj:
            q = q.filter_by(category_id=cat_obj.category_id)

    total      = q.count()
    complaints = q.order_by(Complaint.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    return ok({
        "page":          page,
        "page_size":     limit,
        "total_records": total,
        "data":          [c.to_dict() for c in complaints],
    })


@complaints_bp.route("/<int:complaint_id>", methods=["GET"])
@auth_required
def get_complaint(complaint_id):
    complaint = Complaint.query.get(complaint_id)
    if not complaint:
        return err("Complaint not found.", 404)
    if g.user.role != "admin" and complaint.user_id != g.user.user_id:
        return err("Access denied.", 403)
    return ok(complaint.to_dict())


@complaints_bp.route("/<int:complaint_id>", methods=["PUT"])
@auth_required
def update_complaint(complaint_id):
    complaint = Complaint.query.get(complaint_id)
    if not complaint:
        return err("Complaint not found.", 404)
    if g.user.role != "admin" and complaint.user_id != g.user.user_id:
        return err("Access denied.", 403)

    data = request.get_json(silent=True) or {}
    for field in ("title", "description", "state", "district"):
        if field in data:
            setattr(complaint, field, data[field].strip())
    if "status" in data and g.user.role == "admin":
        complaint.status = data["status"]
    if "incident_date" in data:
        try:
            complaint.incident_date = datetime.strptime(data["incident_date"], "%Y-%m-%d").date()
        except ValueError:
            return err("Invalid incident_date – use YYYY-MM-DD.", 422)

    db.session.commit()
    _log_activity(g.user.user_id, f"Complaint Updated: {complaint.title}")
    return ok(message="Complaint updated successfully.")


@complaints_bp.route("/<int:complaint_id>", methods=["DELETE"])
@auth_required
def delete_complaint(complaint_id):
    complaint = Complaint.query.get(complaint_id)
    if not complaint:
        return err("Complaint not found.", 404)
    if g.user.role != "admin" and complaint.user_id != g.user.user_id:
        return err("Access denied.", 403)
    db.session.delete(complaint)
    db.session.commit()
    _log_activity(g.user.user_id, f"Complaint Deleted: {complaint_id}")
    return ok(message="Complaint deleted successfully.")


@complaints_bp.route("/<int:complaint_id>/category", methods=["PUT"])
@auth_required
def override_category(complaint_id):
    complaint = Complaint.query.get(complaint_id)
    if not complaint:
        return err("Complaint not found.", 404)
    if g.user.role != "admin" and complaint.user_id != g.user.user_id:
        return err("Access denied.", 403)

    data        = request.get_json(silent=True) or {}
    category_id = data.get("category_id")
    if not category_id:
        return err("category_id is required.", 422)

    cat = ComplaintCategory.query.get(category_id)
    if not cat:
        return err("Category not found.", 404)

    complaint.category_id = category_id
    dept = Department.query.filter_by(
        department_name=get_department_for_category(cat.category_name)
    ).first()
    if dept:
        complaint.department_id = dept.department_id
    db.session.commit()
    return ok(message="Complaint category updated successfully.")
