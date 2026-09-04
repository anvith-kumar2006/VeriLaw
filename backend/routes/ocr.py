"""OCR extraction and entity endpoints."""

import re

from flask import Blueprint, request

from extensions import db
from models import Evidence
from utils.auth import auth_required
from utils.helpers import ok, err

ocr_bp = Blueprint("ocr", __name__, url_prefix="/api/v1/ocr")


@ocr_bp.route("/extract", methods=["POST"])
@auth_required
def extract_ocr():
    data = request.get_json(silent=True) or {}
    evidence_id = data.get("evidence_id")
    if not evidence_id:
        return err("evidence_id is required.", 400)
    evidence = Evidence.query.get(evidence_id)
    if not evidence:
        return err("Evidence not found.", 404)
    ocr_text = evidence.ocr_text or "[OCR not yet processed.]"
    return ok({"ocr_text": ocr_text, "confidence": 96.0 if evidence.ocr_text else 0.0})


@ocr_bp.route("/entities", methods=["POST"])
@auth_required
def extract_entities():
    data = request.get_json(silent=True) or {}
    evidence_id = data.get("evidence_id")
    if not evidence_id:
        return err("evidence_id is required.", 400)
    evidence = Evidence.query.get(evidence_id)
    if not evidence:
        return err("Evidence not found.", 404)
    text = evidence.ocr_text or ""
    dates = re.findall(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", text)
    amounts = re.findall(r"₹[\d,]+(?:\.\d{2})?|\bINR\s*[\d,]+\b", text)
    emails = re.findall(r"\b[\w.+\-]+@[\w\-]+\.[a-zA-Z]{2,}\b", text)
    return ok({"persons": [], "dates": dates, "amounts": amounts,
               "emails": emails, "organizations": []})