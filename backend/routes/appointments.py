"""
routes/appointments.py – Appointment booking and management.
"""

import logging
from datetime import datetime

from flask import Blueprint, request, g

from extensions import db
from models import Appointment, User
from utils.helpers import ok, err, _notify
from utils.auth import auth_required

logger = logging.getLogger("verilaw")

appointments_bp = Blueprint("appointments", __name__, url_prefix="/api/v1/appointments")


@appointments_bp.route("", methods=["POST"])
@auth_required
def book_appointment():
    data             = request.get_json(silent=True) or {}
    lawyer_id        = data.get("lawyer_id")
    scheduled_at_str = data.get("scheduled_at")
    complaint_id     = data.get("complaint_id")
    duration_mins    = data.get("duration_mins", 30)
    notes            = (data.get("notes") or "").strip()

    if not lawyer_id or not scheduled_at_str:
        return err("lawyer_id and scheduled_at are required.", 400)

    lawyer = User.query.get(lawyer_id)
    if not lawyer or lawyer.role != "lawyer":
        return err("Lawyer not found.", 404)

    try:
        scheduled_at = datetime.fromisoformat(scheduled_at_str)
    except ValueError:
        return err("Invalid scheduled_at – use ISO format (YYYY-MM-DDTHH:MM:SS).", 422)

    appt = Appointment(
        citizen_id=g.user.user_id,
        lawyer_id=lawyer_id,
        complaint_id=complaint_id,
        scheduled_at=scheduled_at,
        duration_mins=duration_mins,
        notes=notes,
        status="Pending",
    )
    db.session.add(appt)
    db.session.commit()

    _notify(
        lawyer_id, "New Appointment Request",
        f"{g.user.full_name} requested an appointment on "
        f"{scheduled_at.strftime('%d %b %Y %H:%M')}.", "info",
    )
    return ok(appt.to_dict(), "Appointment booked.", 201)


@appointments_bp.route("", methods=["GET"])
@auth_required
def list_appointments():
    user = g.user
    if user.role == "citizen":
        appts = Appointment.query.filter_by(citizen_id=user.user_id).all()
    elif user.role == "lawyer":
        appts = Appointment.query.filter_by(lawyer_id=user.user_id).all()
    else:
        appts = Appointment.query.all()
    return ok([a.to_dict() for a in appts])


@appointments_bp.route("/<int:appointment_id>", methods=["PUT"])
@auth_required
def update_appointment(appointment_id):
    appt = Appointment.query.get(appointment_id)
    if not appt:
        return err("Appointment not found.", 404)
    user = g.user
    if appt.citizen_id != user.user_id and appt.lawyer_id != user.user_id and user.role != "admin":
        return err("Access denied.", 403)

    data   = request.get_json(silent=True) or {}
    valid  = ("Pending", "Confirmed", "Cancelled", "Completed")
    status = data.get("status")
    if status:
        if status not in valid:
            return err(f"Valid statuses: {valid}", 422)
        appt.status = status
    if "notes" in data:
        appt.notes = data["notes"]
    db.session.commit()
    return ok(appt.to_dict(), "Appointment updated.")


@appointments_bp.route("/<int:appointment_id>", methods=["DELETE"])
@auth_required
def cancel_appointment(appointment_id):
    appt = Appointment.query.get(appointment_id)
    if not appt:
        return err("Appointment not found.", 404)
    if appt.citizen_id != g.user.user_id and g.user.role != "admin":
        return err("Access denied.", 403)
    appt.status = "Cancelled"
    db.session.commit()
    return ok(message="Appointment cancelled.")
