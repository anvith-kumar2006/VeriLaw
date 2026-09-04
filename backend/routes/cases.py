"""
routes/cases.py – Case management (create, list, get, update, archive/delete).
"""

import logging
from datetime import datetime

from flask import Blueprint, request, g
from sqlalchemy import or_, case as sql_case

from extensions import db
from models import Case
from utils.helpers import ok, err, _log_activity, _notify
from utils.auth import auth_required

logger = logging.getLogger("verilaw")

cases_bp = Blueprint("cases", __name__)

ALLOWED_CASE_STATUSES = {
    "Draft", "Active", "Verification Running", "Complaint Generated", "Resolved", "Archived"
}
ALLOWED_CASE_PRIORITIES = {"Low", "Medium", "High", "Critical"}


# Register on both /api/cases and /api/v1/cases for backward compat
@cases_bp.route("/api/cases", methods=["POST"])
@cases_bp.route("/api/v1/cases", methods=["POST"])
@auth_required
def create_case():
    data = request.get_json(silent=True)
    if data is None or not isinstance(data, dict):
        return err("Invalid request body. JSON payload is required.", 400)

    title       = data.get("title")
    category    = data.get("category")
    description = data.get("description")
    status      = data.get("status", "Draft")
    priority    = data.get("priority", "Medium")

    if title is None or not str(title).strip():
        return err("Title is required.", 400)
    if category is None or not str(category).strip():
        return err("Category is required.", 400)

    title    = str(title).strip()
    category = str(category).strip()

    if len(title) > 255:
        return err("Title exceeds maximum length of 255 characters.", 400)
    if len(category) > 100:
        return err("Category exceeds maximum length of 100 characters.", 400)
    if description is not None:
        description = str(description).strip()
        if len(description) > 10000:
            return err("Description exceeds maximum length of 10000 characters.", 400)
    if status not in ALLOWED_CASE_STATUSES:
        return err(f"Invalid status. Allowed values: {', '.join(sorted(ALLOWED_CASE_STATUSES))}", 400)
    if priority not in ALLOWED_CASE_PRIORITIES:
        return err(f"Invalid priority. Allowed values: {', '.join(sorted(ALLOWED_CASE_PRIORITIES))}", 400)

    try:
        new_case = Case(
            user_id=g.user.user_id,
            title=title,
            category=category,
            description=description,
            status=status,
            priority=priority,
        )
        db.session.add(new_case)
        db.session.commit()

        _log_activity(g.user.user_id, f"Case Created: {title}")
        _notify(g.user.user_id, "Case Created", f'Case "{title}" was successfully created.', "success")

        return {"success": True, "case_id": new_case.id, "message": "Case created successfully.",
                "data": new_case.to_dict()}, 201
    except Exception as exc:
        db.session.rollback()
        logger.error("Error creating case: %s", exc)
        return err("Internal server error during case creation.", 500)


@cases_bp.route("/api/cases", methods=["GET"])
@cases_bp.route("/api/v1/cases", methods=["GET"])
@auth_required
def list_cases():
    try:
        q = Case.query.filter_by(user_id=g.user.user_id)

        search_val = request.args.get("search", "").strip()
        if search_val:
            q = q.filter(or_(
                Case.title.ilike(f"%{search_val}%"),
                Case.category.ilike(f"%{search_val}%"),
            ))

        sort_param = request.args.get("sort", "newest").strip().lower()
        if sort_param == "oldest":
            q = q.order_by(Case.created_at.asc())
        elif sort_param == "priority":
            p_order = sql_case(
                (Case.priority == "Critical", 1),
                (Case.priority == "High",     2),
                (Case.priority == "Medium",   3),
                (Case.priority == "Low",      4),
                else_=5,
            )
            q = q.order_by(p_order, Case.created_at.desc())
        elif sort_param == "status":
            s_order = sql_case(
                (Case.status == "Active",               1),
                (Case.status == "Verification Running", 2),
                (Case.status == "Complaint Generated",  3),
                (Case.status == "Draft",                4),
                (Case.status == "Resolved",             5),
                (Case.status == "Archived",             6),
                else_=7,
            )
            q = q.order_by(s_order, Case.created_at.desc())
        else:
            q = q.order_by(Case.created_at.desc())

        cases_list = q.all()
        return ok([c.to_dict() for c in cases_list], "Cases retrieved successfully.")
    except Exception as exc:
        logger.error("Error listing cases: %s", exc)
        return err("Internal server error during cases retrieval.", 500)


@cases_bp.route("/api/cases/<int:case_id>", methods=["GET"])
@cases_bp.route("/api/v1/cases/<int:case_id>", methods=["GET"])
@auth_required
def get_case(case_id):
    try:
        case_obj = Case.query.get(case_id)
        if not case_obj:
            return err("Case not found.", 404)
        if case_obj.user_id != g.user.user_id:
            return err("Access denied.", 403)
        return ok(case_obj.to_dict(), "Case retrieved successfully.")
    except Exception as exc:
        logger.error("Error getting case: %s", exc)
        return err("Internal server error during case retrieval.", 500)


@cases_bp.route("/api/cases/<int:case_id>", methods=["PUT"])
@cases_bp.route("/api/v1/cases/<int:case_id>", methods=["PUT"])
@auth_required
def update_case(case_id):
    try:
        case_obj = Case.query.get(case_id)
        if not case_obj:
            return err("Case not found.", 404)
        if case_obj.user_id != g.user.user_id:
            return err("Access denied.", 403)

        data = request.get_json(silent=True)
        if data is None or not isinstance(data, dict) or not data:
            return err("Request body must be a non-empty JSON object.", 400)

        if "title" in data:
            val = str(data["title"] or "").strip()
            if not val:
                return err("Title cannot be empty.", 400)
            if len(val) > 255:
                return err("Title exceeds maximum length of 255 characters.", 400)
            case_obj.title = val

        if "category" in data:
            val = str(data["category"] or "").strip()
            if not val:
                return err("Category cannot be empty.", 400)
            if len(val) > 100:
                return err("Category exceeds maximum length of 100 characters.", 400)
            case_obj.category = val

        if "description" in data:
            val = data["description"]
            if val is not None:
                val = str(val).strip()
                if len(val) > 10000:
                    return err("Description exceeds maximum length of 10000 characters.", 400)
            case_obj.description = val

        if "status" in data:
            if data["status"] not in ALLOWED_CASE_STATUSES:
                return err(f"Invalid status. Allowed values: {', '.join(sorted(ALLOWED_CASE_STATUSES))}", 400)
            case_obj.status = data["status"]

        if "priority" in data:
            if data["priority"] not in ALLOWED_CASE_PRIORITIES:
                return err(f"Invalid priority. Allowed values: {', '.join(sorted(ALLOWED_CASE_PRIORITIES))}", 400)
            case_obj.priority = data["priority"]

        case_obj.updated_at = datetime.utcnow()
        db.session.commit()
        _log_activity(g.user.user_id, f"Case Updated: {case_obj.title}")
        return ok(case_obj.to_dict(), "Case updated successfully.")
    except Exception as exc:
        db.session.rollback()
        logger.error("Error updating case: %s", exc)
        return err("Internal server error during case update.", 500)


@cases_bp.route("/api/cases/<int:case_id>", methods=["DELETE"])
@cases_bp.route("/api/v1/cases/<int:case_id>", methods=["DELETE"])
@auth_required
def delete_case(case_id):
    try:
        case_obj = Case.query.get(case_id)
        if not case_obj:
            return err("Case not found.", 404)
        if case_obj.user_id != g.user.user_id:
            return err("Access denied.", 403)

        case_obj.status     = "Archived"
        case_obj.updated_at = datetime.utcnow()
        db.session.commit()

        _log_activity(g.user.user_id, f"Case Archived: {case_obj.title}")
        _notify(g.user.user_id, "Case Archived", f'Your case "{case_obj.title}" was archived.', "info")
        return ok(case_obj.to_dict(), "Case archived successfully.")
    except Exception as exc:
        db.session.rollback()
        logger.error("Error archiving case: %s", exc)
        return err("Internal server error during case archiving.", 500)
