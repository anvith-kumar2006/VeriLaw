"""
Judiciary Flow (VeriLaw) — Complete Flask Backend
Single-file backend: app.py
Stack: Flask + Flask-SQLAlchemy + Flask-JWT-Extended + Flask-CORS
Database: MySQL (via PyMySQL) / PostgreSQL (via psycopg2) — configurable via DATABASE_URL
"""

import os
import re
import uuid
import json
import logging
from datetime import datetime, timedelta
from functools import wraps

from flask import Flask, request, jsonify, send_from_directory, g
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity,
)
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy import text, func

# ═══════════════════════════════════════════════════════════════════
# LOGGING
# ═══════════════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("verilaw")

# ═══════════════════════════════════════════════════════════════════
# APP CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

app = Flask(__name__)

# ── Database URL ──────────────────────────────────────────────────
DATABASE_URL = os.environ.get("DATABASE_URL", "")

# Replit provides postgres:// — SQLAlchemy needs postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Fallback: SQLite for zero-config local dev
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///verilaw.db"
    logger.warning("DATABASE_URL not set — falling back to SQLite (dev only).")

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "pool_size": 5,
    "max_overflow": 10,
}

# ── JWT ───────────────────────────────────────────────────────────
JWT_SECRET = os.environ.get(
    "JWT_SECRET_KEY",
    os.environ.get("SESSION_SECRET", "judiciary-flow-jwt-secret-change-in-prod"),
)
app.config["JWT_SECRET_KEY"] = JWT_SECRET
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"

# ── File Upload ───────────────────────────────────────────────────
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
GENERATED_DOCS_FOLDER = os.path.join(os.getcwd(), "generated_documents")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_DOCS_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "pdf", "mp3", "wav"}
MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20 MB

app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

# ── Initialise Extensions ─────────────────────────────────────────
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)


# ═══════════════════════════════════════════════════════════════════
# DATABASE MODELS
# ═══════════════════════════════════════════════════════════════════

class User(db.Model):
    __tablename__ = "users"

    user_id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name     = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(150), nullable=False, unique=True, index=True)
    mobile        = db.Column(db.String(15),  nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role          = db.Column(db.String(20),  nullable=False, default="citizen")
    is_active     = db.Column(db.Boolean,     nullable=False, default=True)
    created_at    = db.Column(db.DateTime,    nullable=False, default=datetime.utcnow)
    updated_at    = db.Column(db.DateTime,    nullable=False, default=datetime.utcnow,
                              onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "user_id":    self.user_id,
            "full_name":  self.full_name,
            "email":      self.email,
            "mobile":     self.mobile,
            "role":       self.role,
            "is_active":  self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class LawyerProfile(db.Model):
    __tablename__ = "lawyer_profiles"

    profile_id         = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    user_id            = db.Column(db.Integer,     db.ForeignKey("users.user_id", ondelete="CASCADE"),
                                   nullable=False, unique=True)
    bar_council_number = db.Column(db.String(100), nullable=True)
    specialization     = db.Column(db.String(200), nullable=True)
    experience_years   = db.Column(db.Integer,     nullable=False, default=0)
    about              = db.Column(db.Text,        nullable=True)
    availability       = db.Column(db.Boolean,     nullable=False, default=True)
    rating             = db.Column(db.Numeric(3, 2), nullable=False, default=0.00)
    total_cases        = db.Column(db.Integer,     nullable=False, default=0)
    location           = db.Column(db.String(200), nullable=True)
    created_at         = db.Column(db.DateTime,    nullable=False, default=datetime.utcnow)
    updated_at         = db.Column(db.DateTime,    nullable=False, default=datetime.utcnow,
                                   onupdate=datetime.utcnow)

    user = db.relationship("User", foreign_keys=[user_id])

    def to_dict(self):
        return {
            "profile_id":         self.profile_id,
            "user_id":            self.user_id,
            "bar_council_number": self.bar_council_number,
            "specialization":     self.specialization,
            "experience_years":   self.experience_years,
            "about":              self.about,
            "availability":       self.availability,
            "rating":             float(self.rating) if self.rating else 0.0,
            "total_cases":        self.total_cases,
            "location":           self.location,
        }


class ComplaintCategory(db.Model):
    __tablename__ = "complaint_categories"

    category_id   = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(100), nullable=False, unique=True)
    description   = db.Column(db.Text,        nullable=True)
    keywords      = db.Column(db.Text,        nullable=True)

    def to_dict(self):
        return {
            "category_id":   self.category_id,
            "category_name": self.category_name,
            "description":   self.description,
        }


class Department(db.Model):
    __tablename__ = "departments"

    department_id   = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    department_name = db.Column(db.String(150), nullable=False)
    description     = db.Column(db.Text,        nullable=True)
    website         = db.Column(db.String(255), nullable=True)
    helpline        = db.Column(db.String(20),  nullable=True)
    email           = db.Column(db.String(150), nullable=True)

    def to_dict(self):
        return {
            "department_id":   self.department_id,
            "department_name": self.department_name,
            "description":     self.description,
            "website":         self.website,
            "helpline":        self.helpline,
            "email":           self.email,
        }


class Complaint(db.Model):
    __tablename__ = "complaints"

    complaint_id  = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    user_id       = db.Column(db.Integer,     db.ForeignKey("users.user_id", ondelete="CASCADE"),
                              nullable=False, index=True)
    category_id   = db.Column(db.Integer,     db.ForeignKey("complaint_categories.category_id",
                              ondelete="SET NULL"), nullable=True, index=True)
    department_id = db.Column(db.Integer,     db.ForeignKey("departments.department_id",
                              ondelete="SET NULL"), nullable=True, index=True)
    title         = db.Column(db.String(200), nullable=False)
    description   = db.Column(db.Text,        nullable=False)
    state         = db.Column(db.String(100), nullable=False)
    district      = db.Column(db.String(100), nullable=False)
    incident_date = db.Column(db.Date,        nullable=True)
    ai_confidence = db.Column(db.Numeric(5, 2), nullable=True)
    status        = db.Column(db.String(20),  nullable=False, default="Draft", index=True)
    created_at    = db.Column(db.DateTime,    nullable=False, default=datetime.utcnow)
    updated_at    = db.Column(db.DateTime,    nullable=False, default=datetime.utcnow,
                              onupdate=datetime.utcnow)

    user       = db.relationship("User",             foreign_keys=[user_id])
    category   = db.relationship("ComplaintCategory", foreign_keys=[category_id])
    department = db.relationship("Department",        foreign_keys=[department_id])

    def to_dict(self):
        return {
            "complaint_id":  self.complaint_id,
            "user_id":       self.user_id,
            "category_id":   self.category_id,
            "department_id": self.department_id,
            "title":         self.title,
            "description":   self.description,
            "state":         self.state,
            "district":      self.district,
            "incident_date": self.incident_date.isoformat() if self.incident_date else None,
            "ai_confidence": float(self.ai_confidence) if self.ai_confidence else None,
            "status":        self.status,
            "category":      self.category.to_dict() if self.category else None,
            "department":    self.department.to_dict() if self.department else None,
            "created_at":    self.created_at.isoformat() if self.created_at else None,
            "updated_at":    self.updated_at.isoformat() if self.updated_at else None,
        }


class Evidence(db.Model):
    __tablename__ = "evidence"

    evidence_id   = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    complaint_id  = db.Column(db.Integer,     db.ForeignKey("complaints.complaint_id",
                              ondelete="CASCADE"), nullable=False, index=True)
    file_name     = db.Column(db.String(255), nullable=False)
    original_name = db.Column(db.String(255), nullable=True)
    file_type     = db.Column(db.String(50),  nullable=True)
    file_size     = db.Column(db.BigInteger,  nullable=True)
    file_path     = db.Column(db.String(500), nullable=True)
    ocr_text      = db.Column(db.Text,        nullable=True)
    category      = db.Column(db.String(100), nullable=True)
    upload_time   = db.Column(db.DateTime,    nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "evidence_id":   self.evidence_id,
            "complaint_id":  self.complaint_id,
            "file_name":     self.file_name,
            "original_name": self.original_name,
            "file_type":     self.file_type,
            "file_size":     self.file_size,
            "ocr_text":      self.ocr_text,
            "category":      self.category,
            "upload_time":   self.upload_time.isoformat() if self.upload_time else None,
        }


class GeneratedDocument(db.Model):
    __tablename__ = "generated_documents"

    document_id   = db.Column(db.Integer,    primary_key=True, autoincrement=True)
    complaint_id  = db.Column(db.Integer,    db.ForeignKey("complaints.complaint_id",
                              ondelete="CASCADE"), nullable=False, index=True)
    user_id       = db.Column(db.Integer,    db.ForeignKey("users.user_id",
                              ondelete="CASCADE"), nullable=False, index=True)
    document_type = db.Column(db.String(10), nullable=False, default="PDF")
    file_path     = db.Column(db.String(500), nullable=True)
    generated_at  = db.Column(db.DateTime,   nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "document_id":    self.document_id,
            "complaint_id":   self.complaint_id,
            "user_id":        self.user_id,
            "document_type":  self.document_type,
            "file_path":      self.file_path,
            "generated_at":   self.generated_at.isoformat() if self.generated_at else None,
            "download_url":   f"/api/v1/documents/download/{self.document_id}",
        }


class ActivityLog(db.Model):
    __tablename__ = "activity_logs"

    log_id     = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    user_id    = db.Column(db.Integer,     db.ForeignKey("users.user_id", ondelete="CASCADE"),
                           nullable=False, index=True)
    activity   = db.Column(db.String(255), nullable=False)
    ip_address = db.Column(db.String(45),  nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime,    nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "log_id":     self.log_id,
            "user_id":    self.user_id,
            "activity":   self.activity,
            "ip_address": self.ip_address,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Appointment(db.Model):
    __tablename__ = "appointments"

    appointment_id = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    citizen_id     = db.Column(db.Integer,  db.ForeignKey("users.user_id", ondelete="CASCADE"),
                               nullable=False, index=True)
    lawyer_id      = db.Column(db.Integer,  db.ForeignKey("users.user_id", ondelete="CASCADE"),
                               nullable=False, index=True)
    complaint_id   = db.Column(db.Integer,  db.ForeignKey("complaints.complaint_id",
                               ondelete="SET NULL"), nullable=True)
    scheduled_at   = db.Column(db.DateTime, nullable=False)
    duration_mins  = db.Column(db.Integer,  nullable=False, default=30)
    status         = db.Column(db.String(20), nullable=False, default="Pending", index=True)
    notes          = db.Column(db.Text,     nullable=True)
    created_at     = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at     = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,
                               onupdate=datetime.utcnow)

    citizen = db.relationship("User", foreign_keys=[citizen_id])
    lawyer  = db.relationship("User", foreign_keys=[lawyer_id])

    def to_dict(self):
        return {
            "appointment_id": self.appointment_id,
            "citizen_id":     self.citizen_id,
            "lawyer_id":      self.lawyer_id,
            "complaint_id":   self.complaint_id,
            "scheduled_at":   self.scheduled_at.isoformat() if self.scheduled_at else None,
            "duration_mins":  self.duration_mins,
            "status":         self.status,
            "notes":          self.notes,
            "created_at":     self.created_at.isoformat() if self.created_at else None,
        }


class ChatMessage(db.Model):
    __tablename__ = "chat_messages"

    message_id   = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    sender_id    = db.Column(db.Integer,  db.ForeignKey("users.user_id", ondelete="CASCADE"),
                             nullable=False, index=True)
    receiver_id  = db.Column(db.Integer,  db.ForeignKey("users.user_id", ondelete="CASCADE"),
                             nullable=False, index=True)
    complaint_id = db.Column(db.Integer,  db.ForeignKey("complaints.complaint_id",
                             ondelete="SET NULL"), nullable=True)
    content      = db.Column(db.Text,     nullable=False)
    is_read      = db.Column(db.Boolean,  nullable=False, default=False, index=True)
    created_at   = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    sender   = db.relationship("User", foreign_keys=[sender_id])
    receiver = db.relationship("User", foreign_keys=[receiver_id])

    def to_dict(self):
        return {
            "message_id":   self.message_id,
            "sender_id":    self.sender_id,
            "receiver_id":  self.receiver_id,
            "complaint_id": self.complaint_id,
            "content":      self.content,
            "is_read":      self.is_read,
            "created_at":   self.created_at.isoformat() if self.created_at else None,
        }


class Notification(db.Model):
    __tablename__ = "notifications"

    notification_id = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    user_id         = db.Column(db.Integer,     db.ForeignKey("users.user_id", ondelete="CASCADE"),
                                nullable=False, index=True)
    title           = db.Column(db.String(200), nullable=False)
    message         = db.Column(db.Text,        nullable=False)
    type            = db.Column(db.String(20),  nullable=False, default="info")
    is_read         = db.Column(db.Boolean,     nullable=False, default=False, index=True)
    created_at      = db.Column(db.DateTime,    nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "notification_id": self.notification_id,
            "user_id":         self.user_id,
            "title":           self.title,
            "message":         self.message,
            "type":            self.type,
            "is_read":         self.is_read,
            "created_at":      self.created_at.isoformat() if self.created_at else None,
        }


class Feedback(db.Model):
    __tablename__ = "feedback"

    feedback_id  = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    user_id      = db.Column(db.Integer,  db.ForeignKey("users.user_id", ondelete="CASCADE"),
                             nullable=False, index=True)
    complaint_id = db.Column(db.Integer,  db.ForeignKey("complaints.complaint_id",
                             ondelete="SET NULL"), nullable=True)
    rating       = db.Column(db.Integer,  nullable=False)
    comment      = db.Column(db.Text,     nullable=True)
    created_at   = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "feedback_id":  self.feedback_id,
            "user_id":      self.user_id,
            "complaint_id": self.complaint_id,
            "rating":       self.rating,
            "comment":      self.comment,
            "created_at":   self.created_at.isoformat() if self.created_at else None,
        }


class Report(db.Model):
    __tablename__ = "reports"

    report_id    = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    generated_by = db.Column(db.Integer,     db.ForeignKey("users.user_id", ondelete="CASCADE"),
                             nullable=False, index=True)
    report_type  = db.Column(db.String(50),  nullable=False)
    parameters   = db.Column(db.Text,        nullable=True)
    file_path    = db.Column(db.String(500), nullable=True)
    created_at   = db.Column(db.DateTime,    nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "report_id":    self.report_id,
            "generated_by": self.generated_by,
            "report_type":  self.report_type,
            "parameters":   self.parameters,
            "file_path":    self.file_path,
            "created_at":   self.created_at.isoformat() if self.created_at else None,
        }


# ═══════════════════════════════════════════════════════════════════
# RESPONSE HELPERS
# ═══════════════════════════════════════════════════════════════════

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


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ═══════════════════════════════════════════════════════════════════
# INTERNAL HELPERS
# ═══════════════════════════════════════════════════════════════════

def _log_activity(user_id, activity):
    try:
        entry = ActivityLog(
            user_id=user_id,
            activity=activity,
            ip_address=request.remote_addr,
            user_agent=(request.headers.get("User-Agent") or "")[:500],
        )
        db.session.add(entry)
        db.session.commit()
    except Exception as exc:
        logger.warning("Activity log failed: %s", exc)
        db.session.rollback()


def _notify(user_id, title, message, ntype="info"):
    try:
        notif = Notification(user_id=user_id, title=title, message=message, type=ntype)
        db.session.add(notif)
        db.session.commit()
    except Exception as exc:
        logger.warning("Notification failed: %s", exc)
        db.session.rollback()


def _current_user():
    """Return the authenticated User object, or abort with 401."""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or not user.is_active:
        return None
    return user


# ═══════════════════════════════════════════════════════════════════
# AUTH DECORATORS
# ═══════════════════════════════════════════════════════════════════

def auth_required(fn):
    """JWT required + active-user check."""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
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
            user = _current_user()
            if not user:
                return err("User not found or account deactivated.", 401)
            if user.role not in roles:
                return err("Access forbidden: insufficient permissions.", 403)
            g.user = user
            return fn(*args, **kwargs)
        return wrapper
    return decorator


# ═══════════════════════════════════════════════════════════════════
# AI CLASSIFIER (keyword-based, no external ML dependency)
# ═══════════════════════════════════════════════════════════════════

_KW = {
    "Consumer Complaint":  ["product","defective","refund","seller","purchase","ecommerce","delivery","quality","warranty"],
    "Labour Complaint":    ["salary","employer","workplace","job","harassment","termination","wage","employee","pf","esi"],
    "Cyber Crime":         ["online","fraud","hack","phishing","scam","cyber","internet","password","otp","upi","debit"],
    "Property Dispute":    ["land","property","rent","tenant","encroachment","lease","boundary","ownership","plot","title"],
    "Banking Complaint":   ["bank","loan","account","credit","debit","emi","atm","transaction","neft","rtgs","ifsc"],
    "Insurance Complaint": ["insurance","claim","policy","premium","settlement","coverage","maturity","nominee"],
    "Municipal Complaint": ["water","roads","garbage","electricity","municipality","drainage","street","light","pothole"],
    "RTI":                 ["rti","information","government","public","transparency","records","right","cpio"],
    "Women Safety":        ["harassment","dowry","domestic","violence","women","safety","abuse","stalking","acid"],
    "Tenant Dispute":      ["rent","landlord","tenant","eviction","deposit","lease","accommodation","notice"],
}

_DEPT_MAP = {
    "Consumer Complaint":  "Consumer Commission",
    "Labour Complaint":    "Labour Department",
    "Cyber Crime":         "Cyber Crime Cell",
    "Property Dispute":    "Land Revenue Department",
    "Banking Complaint":   "Banking Ombudsman",
    "Insurance Complaint": "IRDAI",
    "Municipal Complaint": "Municipal Corporation",
    "RTI":                 "Central Information Commission",
    "Women Safety":        "National Commission for Women",
    "Tenant Dispute":      "District Court",
}


def classify_complaint(text):
    words = set(re.findall(r"\b\w+\b", text.lower()))
    scores = {cat: sum(1 for kw in kws if kw in words) for cat, kws in _KW.items()}
    best = max(scores, key=scores.get)
    total = sum(scores.values()) or 1
    confidence = round(min((scores[best] / total) * 100, 99.99), 2)
    if scores[best] == 0:
        best, confidence = "Consumer Complaint", 50.0
    return best, confidence


# ═══════════════════════════════════════════════════════════════════
# ROUTES — HEALTH CHECK
# ═══════════════════════════════════════════════════════════════════

@app.route("/api/v1/health", methods=["GET"])
def health_check():
    try:
        db.session.execute(text("SELECT 1"))
        return ok({"status": "healthy", "database": "connected", "version": "1.0.0"})
    except Exception as exc:
        return err(f"Database error: {exc}", 503)


# ═══════════════════════════════════════════════════════════════════
# ROUTES — AUTH
# ═══════════════════════════════════════════════════════════════════

@app.route("/api/v1/auth/register", methods=["POST"])
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


@app.route("/api/v1/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
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


@app.route("/api/v1/auth/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    return ok({"token": create_access_token(identity=identity)}, "Token refreshed.")


@app.route("/api/v1/auth/logout", methods=["POST"])
@auth_required
def logout():
    _log_activity(g.user.user_id, "User Logout")
    return ok(message="Logout successful.")


# ═══════════════════════════════════════════════════════════════════
# ROUTES — USER PROFILE
# ═══════════════════════════════════════════════════════════════════

@app.route("/api/v1/profile", methods=["GET"])
@auth_required
def get_profile():
    return ok(g.user.to_dict())


@app.route("/api/v1/profile", methods=["PUT"])
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


@app.route("/api/v1/profile/password", methods=["PUT"])
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


# ═══════════════════════════════════════════════════════════════════
# ROUTES — LAWYER PROFILES
# ═══════════════════════════════════════════════════════════════════

@app.route("/api/v1/lawyers", methods=["GET"])
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


@app.route("/api/v1/lawyers/<int:lawyer_id>", methods=["GET"])
def get_lawyer(lawyer_id):
    lp = LawyerProfile.query.filter_by(user_id=lawyer_id).first()
    if not lp:
        return err("Lawyer not found.", 404)
    u  = User.query.get(lawyer_id)
    d  = lp.to_dict()
    d["full_name"] = u.full_name
    d["email"]     = u.email
    return ok(d)


@app.route("/api/v1/lawyers/profile", methods=["PUT"])
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


# ═══════════════════════════════════════════════════════════════════
# ROUTES — CATEGORIES & DEPARTMENTS
# ═══════════════════════════════════════════════════════════════════

@app.route("/api/v1/categories", methods=["GET"])
def get_categories():
    cats = ComplaintCategory.query.order_by(ComplaintCategory.category_name).all()
    return ok([c.to_dict() for c in cats])


@app.route("/api/v1/departments", methods=["GET"])
def get_departments():
    depts = Department.query.order_by(Department.department_name).all()
    return ok([d.to_dict() for d in depts])


@app.route("/api/v1/departments/<int:department_id>", methods=["GET"])
def get_department(department_id):
    dept = Department.query.get(department_id)
    if not dept:
        return err("Department not found.", 404)
    return ok(dept.to_dict())


# ═══════════════════════════════════════════════════════════════════
# ROUTES — COMPLAINTS
# ═══════════════════════════════════════════════════════════════════

@app.route("/api/v1/complaints", methods=["POST"])
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
            return err("Invalid incident_date — use YYYY-MM-DD.", 422)

    # AI classification
    cat_name, confidence = classify_complaint(f"{title} {description}")
    category   = ComplaintCategory.query.filter_by(category_name=cat_name).first()
    dept_name  = _DEPT_MAP.get(cat_name, "")
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


@app.route("/api/v1/complaints", methods=["GET"])
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


@app.route("/api/v1/complaints/<int:complaint_id>", methods=["GET"])
@auth_required
def get_complaint(complaint_id):
    complaint = Complaint.query.get(complaint_id)
    if not complaint:
        return err("Complaint not found.", 404)
    if g.user.role != "admin" and complaint.user_id != g.user.user_id:
        return err("Access denied.", 403)
    return ok(complaint.to_dict())


@app.route("/api/v1/complaints/<int:complaint_id>", methods=["PUT"])
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
            return err("Invalid incident_date — use YYYY-MM-DD.", 422)

    db.session.commit()
    _log_activity(g.user.user_id, f"Complaint Updated: {complaint.title}")
    return ok(message="Complaint updated successfully.")


@app.route("/api/v1/complaints/<int:complaint_id>", methods=["DELETE"])
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


@app.route("/api/v1/complaints/<int:complaint_id>/category", methods=["PUT"])
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
    dept = Department.query.filter_by(department_name=_DEPT_MAP.get(cat.category_name, "")).first()
    if dept:
        complaint.department_id = dept.department_id
    db.session.commit()
    return ok(message="Complaint category updated successfully.")


# ═══════════════════════════════════════════════════════════════════
# ROUTES — AI
# ═══════════════════════════════════════════════════════════════════

@app.route("/api/v1/ai/classify", methods=["POST"])
@auth_required
def ai_classify():
    data = request.get_json(silent=True) or {}
    desc = (data.get("description") or "").strip()
    if not desc:
        return err("description is required.", 400)
    category, confidence = classify_complaint(desc)
    return ok({"category": category, "confidence": confidence})


@app.route("/api/v1/ai/recommend", methods=["POST"])
@auth_required
def ai_recommend():
    data     = request.get_json(silent=True) or {}
    category = (data.get("category") or "").strip()
    if not category:
        return err("category is required.", 400)
    dept_name = _DEPT_MAP.get(category)
    if not dept_name:
        return err("No department recommendation for this category.", 404)
    dept = Department.query.filter_by(department_name=dept_name).first()
    return ok({
        "department":        dept_name,
        "department_details": dept.to_dict() if dept else None,
        "reason":            f"{category} complaints are handled by {dept_name}.",
        "confidence":        95.0,
    })


# ═══════════════════════════════════════════════════════════════════
# ROUTES — EVIDENCE
# ═══════════════════════════════════════════════════════════════════

@app.route("/api/v1/evidence/upload", methods=["POST"])
@auth_required
def upload_evidence():
    complaint_id = request.form.get("complaint_id", type=int)
    if not complaint_id:
        return err("complaint_id is required.", 400)

    complaint = Complaint.query.get(complaint_id)
    if not complaint:
        return err("Complaint not found.", 404)
    if complaint.user_id != g.user.user_id and g.user.role != "admin":
        return err("Access denied.", 403)
    if Evidence.query.filter_by(complaint_id=complaint_id).count() >= 10:
        return err("Maximum 10 files per complaint.", 400)

    files    = request.files.getlist("files")
    uploaded = 0
    failed   = 0

    for f in files:
        if f and allowed_file(f.filename):
            original  = secure_filename(f.filename)
            ext       = original.rsplit(".", 1)[1].lower()
            stored    = f"{uuid.uuid4().hex}.{ext}"
            path      = os.path.join(UPLOAD_FOLDER, stored)
            f.save(path)
            size = os.path.getsize(path)

            ev = Evidence(
                complaint_id=complaint_id,
                file_name=stored,
                original_name=original,
                file_type=ext.upper(),
                file_size=size,
                file_path=path,
            )
            db.session.add(ev)
            uploaded += 1
        else:
            failed += 1

    db.session.commit()
    _log_activity(g.user.user_id, f"Evidence Uploaded: {uploaded} files for complaint {complaint_id}")
    return ok({"uploaded_files": uploaded, "failed_files": failed}, "Evidence uploaded.", 201)


@app.route("/api/v1/evidence/<int:complaint_id>", methods=["GET"])
@auth_required
def list_evidence(complaint_id):
    complaint = Complaint.query.get(complaint_id)
    if not complaint:
        return err("Complaint not found.", 404)
    if complaint.user_id != g.user.user_id and g.user.role != "admin":
        return err("Access denied.", 403)
    ev_list = Evidence.query.filter_by(complaint_id=complaint_id).all()
    return ok([e.to_dict() for e in ev_list])


@app.route("/api/v1/evidence/<int:evidence_id>", methods=["DELETE"])
@auth_required
def delete_evidence(evidence_id):
    ev = Evidence.query.get(evidence_id)
    if not ev:
        return err("Evidence not found.", 404)
    complaint = Complaint.query.get(ev.complaint_id)
    if complaint.user_id != g.user.user_id and g.user.role != "admin":
        return err("Access denied.", 403)
    try:
        if ev.file_path and os.path.exists(ev.file_path):
            os.remove(ev.file_path)
    except OSError:
        pass
    db.session.delete(ev)
    db.session.commit()
    return ok(message="Evidence deleted successfully.")


@app.route("/api/v1/evidence/download/<int:evidence_id>", methods=["GET"])
@auth_required
def download_evidence(evidence_id):
    ev = Evidence.query.get(evidence_id)
    if not ev:
        return err("Evidence not found.", 404)
    complaint = Complaint.query.get(ev.complaint_id)
    if complaint.user_id != g.user.user_id and g.user.role != "admin":
        return err("Access denied.", 403)
    return send_from_directory(
        UPLOAD_FOLDER, ev.file_name,
        as_attachment=True, download_name=ev.original_name,
    )


# ═══════════════════════════════════════════════════════════════════
# ROUTES — OCR (lightweight; install pytesseract for real OCR)
# ═══════════════════════════════════════════════════════════════════

@app.route("/api/v1/ocr/extract", methods=["POST"])
@auth_required
def ocr_extract():
    data        = request.get_json(silent=True) or {}
    evidence_id = data.get("evidence_id")
    if not evidence_id:
        return err("evidence_id is required.", 400)
    ev = Evidence.query.get(evidence_id)
    if not ev:
        return err("Evidence not found.", 404)

    ocr_text = ev.ocr_text or (
        "[OCR not yet processed. "
        "Install pytesseract and opencv-python to enable full OCR.]"
    )
    return ok({"ocr_text": ocr_text, "confidence": 0.0 if not ev.ocr_text else 96.0})


@app.route("/api/v1/ocr/status/<int:evidence_id>", methods=["GET"])
@auth_required
def ocr_status(evidence_id):
    ev = Evidence.query.get(evidence_id)
    if not ev:
        return err("Evidence not found.", 404)
    return ok({"status": "Completed" if ev.ocr_text else "Pending"})


@app.route("/api/v1/ocr/entities", methods=["POST"])
@auth_required
def extract_entities():
    data        = request.get_json(silent=True) or {}
    evidence_id = data.get("evidence_id")
    if not evidence_id:
        return err("evidence_id is required.", 400)
    ev = Evidence.query.get(evidence_id)
    if not ev:
        return err("Evidence not found.", 404)
    text   = ev.ocr_text or ""
    dates  = re.findall(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", text)
    amounts = re.findall(r"₹[\d,]+(?:\.\d{2})?|\bINR\s*[\d,]+\b", text)
    emails = re.findall(r"\b[\w.+\-]+@[\w\-]+\.[a-zA-Z]{2,}\b", text)
    return ok({"persons": [], "dates": dates, "amounts": amounts,
               "emails": emails, "organizations": []})


# ═══════════════════════════════════════════════════════════════════
# ROUTES — TIMELINE
# ═══════════════════════════════════════════════════════════════════

@app.route("/api/v1/timeline/generate", methods=["POST"])
@auth_required
def generate_timeline():
    data         = request.get_json(silent=True) or {}
    complaint_id = data.get("complaint_id")
    if not complaint_id:
        return err("complaint_id is required.", 400)
    complaint = Complaint.query.get(complaint_id)
    if not complaint:
        return err("Complaint not found.", 404)

    ev_list  = Evidence.query.filter_by(complaint_id=complaint_id).order_by(Evidence.upload_time).all()
    timeline = []
    if complaint.incident_date:
        timeline.append({"date": complaint.incident_date.isoformat(), "event": "Incident Date"})
    for ev in ev_list:
        timeline.append({"date": ev.upload_time.date().isoformat(),
                         "event": f"Evidence uploaded: {ev.original_name}"})
    timeline.append({"date": complaint.created_at.date().isoformat(), "event": "Complaint Filed"})
    timeline.sort(key=lambda x: x["date"])
    return ok({"timeline": timeline})


# ═══════════════════════════════════════════════════════════════════
# ROUTES — DOCUMENT GENERATION
# ═══════════════════════════════════════════════════════════════════

@app.route("/api/v1/documents/generate", methods=["POST"])
@auth_required
def generate_document():
    data         = request.get_json(silent=True) or {}
    complaint_id = data.get("complaint_id")
    doc_type     = (data.get("document_type") or "PDF").upper()

    if not complaint_id:
        return err("complaint_id is required.", 400)
    complaint = Complaint.query.get(complaint_id)
    if not complaint:
        return err("Complaint not found.", 404)
    if complaint.user_id != g.user.user_id and g.user.role != "admin":
        return err("Access denied.", 403)
    if doc_type not in ("PDF", "HTML"):
        return err("Supported types: PDF, HTML.", 400)

    user       = g.user
    category   = ComplaintCategory.query.get(complaint.category_id) if complaint.category_id else None
    department = Department.query.get(complaint.department_id)      if complaint.department_id else None
    evidence   = Evidence.query.filter_by(complaint_id=complaint_id).all()

    stamp      = uuid.uuid4().hex[:8]
    file_name  = f"complaint_{complaint_id}_{stamp}.{doc_type.lower()}"
    file_path  = os.path.join(GENERATED_DOCS_FOLDER, file_name)

    if doc_type == "HTML":
        ev_rows = "".join(
            f"<tr><td>{e.original_name}</td><td>{e.file_type}</td>"
            f"<td>{round((e.file_size or 0)/1024, 1)} KB</td></tr>"
            for e in evidence
        )
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>Complaint — {complaint.title}</title>
  <style>
    body {{font-family:Arial,sans-serif;margin:40px;color:#222;}}
    h1   {{color:#1a3a5c;border-bottom:2px solid #1a3a5c;padding-bottom:8px;}}
    h2   {{color:#2c5f8a;margin-top:28px;}}
    table{{width:100%;border-collapse:collapse;margin-top:10px;}}
    th,td{{padding:10px 14px;border:1px solid #ccc;text-align:left;}}
    th   {{background:#1a3a5c;color:#fff;}}
    tr:nth-child(even){{background:#f4f8ff;}}
    .footer{{margin-top:60px;border-top:1px solid #ccc;padding-top:20px;}}
  </style>
</head>
<body>
  <h1>⚖ Judiciary Flow — Complaint Document</h1>
  <p><strong>Generated:</strong> {datetime.utcnow().strftime("%d %B %Y %H:%M UTC")}</p>

  <h2>Complainant</h2>
  <table>
    <tr><th>Name</th><td>{user.full_name}</td></tr>
    <tr><th>Email</th><td>{user.email}</td></tr>
    <tr><th>Mobile</th><td>{user.mobile}</td></tr>
  </table>

  <h2>Authority</h2>
  <table>
    <tr><th>Department</th><td>{department.department_name if department else "N/A"}</td></tr>
    <tr><th>Helpline</th><td>{department.helpline if department and department.helpline else "N/A"}</td></tr>
    <tr><th>Website</th><td>{department.website if department and department.website else "N/A"}</td></tr>
  </table>

  <h2>Complaint Details</h2>
  <table>
    <tr><th>Title</th><td>{complaint.title}</td></tr>
    <tr><th>Category</th><td>{category.category_name if category else "N/A"}</td></tr>
    <tr><th>State</th><td>{complaint.state}</td></tr>
    <tr><th>District</th><td>{complaint.district}</td></tr>
    <tr><th>Incident Date</th><td>{complaint.incident_date or "N/A"}</td></tr>
    <tr><th>Status</th><td>{complaint.status}</td></tr>
    <tr><th>AI Confidence</th><td>{complaint.ai_confidence}%</td></tr>
  </table>

  <h2>Description</h2>
  <p style="line-height:1.7">{complaint.description}</p>

  <h2>Evidence</h2>
  <table>
    <tr><th>File Name</th><th>Type</th><th>Size</th></tr>
    {ev_rows or "<tr><td colspan='3'>No evidence uploaded.</td></tr>"}
  </table>

  <div class="footer">
    <p>Complainant Signature: _________________________ &nbsp;&nbsp; Date: _____________</p>
  </div>
</body>
</html>"""
        with open(file_path, "w", encoding="utf-8") as fh:
            fh.write(html_content)

    else:  # PDF
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import (
                SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
            )

            doc    = SimpleDocTemplate(file_path, pagesize=A4,
                                       leftMargin=50, rightMargin=50,
                                       topMargin=60, bottomMargin=60)
            styles = getSampleStyleSheet()
            story  = []

            story.append(Paragraph("⚖ JUDICIARY FLOW", styles["Title"]))
            story.append(Paragraph("Complaint Document", styles["Heading1"]))
            story.append(Spacer(1, 8))
            story.append(Paragraph(
                f"Generated: {datetime.utcnow().strftime('%d %B %Y %H:%M UTC')}",
                styles["Normal"],
            ))
            story.append(Spacer(1, 14))

            def section(title, rows):
                story.append(Paragraph(title, styles["Heading2"]))
                t = Table(rows, colWidths=[160, 330])
                t.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#1a3a5c")),
                    ("TEXTCOLOR",  (0, 0), (0, -1), colors.white),
                    ("GRID",       (0, 0), (-1, -1), 0.4, colors.grey),
                    ("ROWBACKGROUNDS", (1, 0), (-1, -1),
                     [colors.HexColor("#f4f8ff"), colors.white]),
                    ("PADDING",    (0, 0), (-1, -1), 8),
                ]))
                story.append(t)
                story.append(Spacer(1, 12))

            section("Complainant", [
                ["Name",   user.full_name],
                ["Email",  user.email],
                ["Mobile", user.mobile],
            ])
            section("Authority", [
                ["Department", department.department_name if department else "N/A"],
                ["Helpline",   department.helpline if department and department.helpline else "N/A"],
                ["Website",    department.website  if department and department.website  else "N/A"],
            ])
            section("Complaint Details", [
                ["Title",          complaint.title],
                ["Category",       category.category_name if category else "N/A"],
                ["State",          complaint.state],
                ["District",       complaint.district],
                ["Incident Date",  str(complaint.incident_date or "N/A")],
                ["Status",         complaint.status],
                ["AI Confidence",  f"{complaint.ai_confidence}%"],
            ])

            story.append(Paragraph("Description", styles["Heading2"]))
            story.append(Paragraph(complaint.description, styles["Normal"]))
            story.append(Spacer(1, 12))

            if evidence:
                story.append(Paragraph("Evidence", styles["Heading2"]))
                ev_data = [["File Name", "Type", "Size"]] + [
                    [e.original_name, e.file_type,
                     f"{round((e.file_size or 0)/1024, 1)} KB"]
                    for e in evidence
                ]
                et = Table(ev_data, colWidths=[250, 60, 180])
                et.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a3a5c")),
                    ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
                    ("GRID",       (0, 0), (-1, -1), 0.4, colors.grey),
                    ("PADDING",    (0, 0), (-1, -1), 6),
                ]))
                story.append(et)
                story.append(Spacer(1, 12))

            story.append(Spacer(1, 30))
            story.append(Paragraph(
                "Complainant Signature: _______________________   Date: _______________",
                styles["Normal"],
            ))
            doc.build(story)

        except ImportError:
            # Fallback: plain text file
            with open(file_path, "w", encoding="utf-8") as fh:
                fh.write(f"COMPLAINT: {complaint.title}\n")
                fh.write(f"Category:  {category.category_name if category else 'N/A'}\n")
                fh.write(f"Status:    {complaint.status}\n\n")
                fh.write(complaint.description)

    gen_doc = GeneratedDocument(
        complaint_id=complaint_id,
        user_id=user.user_id,
        document_type=doc_type,
        file_path=file_path,
    )
    db.session.add(gen_doc)
    complaint.status = "Completed"
    db.session.commit()

    _log_activity(user.user_id, f"Document Generated: {doc_type} for complaint {complaint_id}")
    return ok({
        "document_id":   gen_doc.document_id,
        "download_url":  f"/api/v1/documents/download/{gen_doc.document_id}",
    }, "Document generated successfully.", 201)


@app.route("/api/v1/documents/download/<int:document_id>", methods=["GET"])
@auth_required
def download_document(document_id):
    gen_doc = GeneratedDocument.query.get(document_id)
    if not gen_doc:
        return err("Document not found.", 404)
    if gen_doc.user_id != g.user.user_id and g.user.role != "admin":
        return err("Access denied.", 403)
    return send_from_directory(
        GENERATED_DOCS_FOLDER,
        os.path.basename(gen_doc.file_path),
        as_attachment=True,
    )


@app.route("/api/v1/documents", methods=["GET"])
@auth_required
def list_documents():
    q = GeneratedDocument.query
    if g.user.role != "admin":
        q = q.filter_by(user_id=g.user.user_id)
    docs = q.order_by(GeneratedDocument.generated_at.desc()).all()
    return ok([d.to_dict() for d in docs])


@app.route("/api/v1/documents/<int:document_id>", methods=["DELETE"])
@auth_required
def delete_document(document_id):
    gen_doc = GeneratedDocument.query.get(document_id)
    if not gen_doc:
        return err("Document not found.", 404)
    if gen_doc.user_id != g.user.user_id and g.user.role != "admin":
        return err("Access denied.", 403)
    try:
        if gen_doc.file_path and os.path.exists(gen_doc.file_path):
            os.remove(gen_doc.file_path)
    except OSError:
        pass
    db.session.delete(gen_doc)
    db.session.commit()
    return ok(message="Document deleted successfully.")


# ═══════════════════════════════════════════════════════════════════
# ROUTES — CHAT
# ═══════════════════════════════════════════════════════════════════

@app.route("/api/v1/chat/send", methods=["POST"])
@auth_required
def send_message():
    data        = request.get_json(silent=True) or {}
    receiver_id = data.get("receiver_id")
    content     = (data.get("content") or "").strip()
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


@app.route("/api/v1/chat/<int:other_user_id>", methods=["GET"])
@auth_required
def get_chat(other_user_id):
    me    = g.user.user_id
    page  = request.args.get("page",  1,  type=int)
    limit = min(request.args.get("limit", 20, type=int), 100)

    msgs = ChatMessage.query.filter(
        ((ChatMessage.sender_id   == me) & (ChatMessage.receiver_id == other_user_id)) |
        ((ChatMessage.sender_id   == other_user_id) & (ChatMessage.receiver_id == me))
    ).order_by(ChatMessage.created_at.desc()).offset((page - 1) * limit).limit(limit).all()

    # Mark incoming as read
    unread = [m for m in msgs if m.receiver_id == me and not m.is_read]
    for m in unread:
        m.is_read = True
    if unread:
        db.session.commit()

    return ok({"messages": [m.to_dict() for m in reversed(msgs)]})


@app.route("/api/v1/chat/unread", methods=["GET"])
@auth_required
def unread_count():
    count = ChatMessage.query.filter_by(receiver_id=g.user.user_id, is_read=False).count()
    return ok({"unread_count": count})


# ═══════════════════════════════════════════════════════════════════
# ROUTES — NOTIFICATIONS
# ═══════════════════════════════════════════════════════════════════

@app.route("/api/v1/notifications", methods=["GET"])
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


@app.route("/api/v1/notifications/<int:notification_id>/read", methods=["PUT"])
@auth_required
def mark_notification_read(notification_id):
    notif = Notification.query.get(notification_id)
    if not notif or notif.user_id != g.user.user_id:
        return err("Notification not found.", 404)
    notif.is_read = True
    db.session.commit()
    return ok(message="Notification marked as read.")


@app.route("/api/v1/notifications/read-all", methods=["PUT"])
@auth_required
def mark_all_read():
    Notification.query.filter_by(user_id=g.user.user_id, is_read=False).update({"is_read": True})
    db.session.commit()
    return ok(message="All notifications marked as read.")


# ═══════════════════════════════════════════════════════════════════
# ROUTES — FEEDBACK
# ═══════════════════════════════════════════════════════════════════

@app.route("/api/v1/feedback", methods=["POST"])
@auth_required
def submit_feedback():
    data         = request.get_json(silent=True) or {}
    rating       = data.get("rating")
    comment      = (data.get("comment") or "").strip()
    complaint_id = data.get("complaint_id")

    if not isinstance(rating, int) or not (1 <= rating <= 5):
        return err("Rating must be an integer between 1 and 5.", 422)

    fb = Feedback(
        user_id=g.user.user_id,
        complaint_id=complaint_id,
        rating=rating,
        comment=comment,
    )
    db.session.add(fb)
    db.session.commit()
    return ok(fb.to_dict(), "Feedback submitted.", 201)


@app.route("/api/v1/feedback", methods=["GET"])
@auth_required
def list_feedback():
    if g.user.role == "admin":
        fbs = Feedback.query.order_by(Feedback.created_at.desc()).all()
    else:
        fbs = Feedback.query.filter_by(user_id=g.user.user_id).all()
    return ok([f.to_dict() for f in fbs])


# ═══════════════════════════════════════════════════════════════════
# ROUTES — APPOINTMENTS
# ═══════════════════════════════════════════════════════════════════

@app.route("/api/v1/appointments", methods=["POST"])
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
        return err("Invalid scheduled_at — use ISO format (YYYY-MM-DDTHH:MM:SS).", 422)

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


@app.route("/api/v1/appointments", methods=["GET"])
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


@app.route("/api/v1/appointments/<int:appointment_id>", methods=["PUT"])
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


@app.route("/api/v1/appointments/<int:appointment_id>", methods=["DELETE"])
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


# ═══════════════════════════════════════════════════════════════════
# ROUTES — REPORTS
# ═══════════════════════════════════════════════════════════════════

@app.route("/api/v1/reports/summary", methods=["GET"])
@auth_required
def report_summary():
    user = g.user
    if user.role == "admin":
        by_status   = db.session.query(Complaint.status, func.count()).group_by(Complaint.status).all()
        by_cat      = db.session.query(
            ComplaintCategory.category_name, func.count(Complaint.complaint_id)
        ).join(Complaint, Complaint.category_id == ComplaintCategory.category_id).group_by(
            ComplaintCategory.category_name
        ).all()
        return ok({
            "total_users":      User.query.count(),
            "total_complaints": Complaint.query.count(),
            "total_evidence":   Evidence.query.count(),
            "by_status":        {s: c for s, c in by_status},
            "by_category":      {s: c for s, c in by_cat},
        })
    else:
        by_status = db.session.query(Complaint.status, func.count()).filter(
            Complaint.user_id == user.user_id
        ).group_by(Complaint.status).all()
        return ok({
            "total_complaints": Complaint.query.filter_by(user_id=user.user_id).count(),
            "total_documents":  GeneratedDocument.query.filter_by(user_id=user.user_id).count(),
            "by_status":        {s: c for s, c in by_status},
        })


@app.route("/api/v1/reports/department-stats", methods=["GET"])
@role_required("admin")
def report_department_stats():
    stats = db.session.query(
        Department.department_name, func.count(Complaint.complaint_id)
    ).join(Complaint, Complaint.department_id == Department.department_id).group_by(
        Department.department_name
    ).all()
    return ok({"department_stats": {n: c for n, c in stats}})


@app.route("/api/v1/reports/activity", methods=["GET"])
@role_required("admin")
def report_activity():
    page  = request.args.get("page",  1,  type=int)
    limit = min(request.args.get("limit", 20, type=int), 100)
    logs  = ActivityLog.query.order_by(
        ActivityLog.created_at.desc()
    ).offset((page - 1) * limit).limit(limit).all()
    return ok({"page": page, "data": [l.to_dict() for l in logs]})


# ═══════════════════════════════════════════════════════════════════
# ROUTES — ADMIN
# ═══════════════════════════════════════════════════════════════════

@app.route("/api/v1/admin/stats", methods=["GET"])
@role_required("admin")
def admin_stats():
    return ok({
        "total_users":        User.query.count(),
        "total_citizens":     User.query.filter_by(role="citizen").count(),
        "total_lawyers":      User.query.filter_by(role="lawyer").count(),
        "total_admins":       User.query.filter_by(role="admin").count(),
        "total_complaints":   Complaint.query.count(),
        "total_evidence":     Evidence.query.count(),
        "total_documents":    GeneratedDocument.query.count(),
        "total_appointments": Appointment.query.count(),
        "total_feedback":     Feedback.query.count(),
    })


@app.route("/api/v1/admin/users", methods=["GET"])
@role_required("admin")
def admin_list_users():
    page  = request.args.get("page",  1,  type=int)
    limit = min(request.args.get("limit", 20, type=int), 100)
    role  = request.args.get("role")
    q     = User.query
    if role:
        q = q.filter_by(role=role)
    total = q.count()
    users = q.order_by(User.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    return ok({"total": total, "page": page, "data": [u.to_dict() for u in users]})


@app.route("/api/v1/admin/users/<int:user_id>", methods=["GET"])
@role_required("admin")
def admin_get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return err("User not found.", 404)
    return ok(user.to_dict())


@app.route("/api/v1/admin/users/<int:user_id>/toggle-active", methods=["PUT"])
@role_required("admin")
def admin_toggle_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return err("User not found.", 404)
    user.is_active = not user.is_active
    db.session.commit()
    return ok({"is_active": user.is_active},
              f"User {'activated' if user.is_active else 'deactivated'}.")


@app.route("/api/v1/admin/users/<int:user_id>/role", methods=["PUT"])
@role_required("admin")
def admin_change_role(user_id):
    user     = User.query.get(user_id)
    if not user:
        return err("User not found.", 404)
    data     = request.get_json(silent=True) or {}
    new_role = data.get("role")
    if new_role not in ("citizen", "lawyer", "admin"):
        return err("Valid roles: citizen, lawyer, admin.", 422)
    user.role = new_role
    db.session.commit()
    return ok({"role": user.role}, "User role updated.")


@app.route("/api/v1/admin/complaints", methods=["GET"])
@role_required("admin")
def admin_list_complaints():
    page   = request.args.get("page",   1,  type=int)
    limit  = min(request.args.get("limit", 20, type=int), 100)
    status = request.args.get("status")
    q      = Complaint.query
    if status:
        q = q.filter_by(status=status)
    total      = q.count()
    complaints = q.order_by(Complaint.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    return ok({"total": total, "page": page, "data": [c.to_dict() for c in complaints]})


@app.route("/api/v1/admin/notify-all", methods=["POST"])
@role_required("admin")
def admin_notify_all():
    data    = request.get_json(silent=True) or {}
    title   = (data.get("title")   or "System Announcement").strip()
    message = (data.get("message") or "").strip()
    if not message:
        return err("message is required.", 400)
    users = User.query.filter_by(is_active=True).all()
    for u in users:
        db.session.add(Notification(user_id=u.user_id, title=title, message=message))
    db.session.commit()
    return ok({"notified": len(users)}, "Broadcast notification sent.")


# ═══════════════════════════════════════════════════════════════════
# GLOBAL ERROR HANDLERS
# ═══════════════════════════════════════════════════════════════════

@app.errorhandler(400)
def bad_request(e):
    return err("Bad request.", 400)

@app.errorhandler(401)
def unauthorized(e):
    return err("Unauthorized. Please login.", 401)

@app.errorhandler(403)
def forbidden(e):
    return err("Forbidden.", 403)

@app.errorhandler(404)
def not_found(e):
    return err("Resource not found.", 404)

@app.errorhandler(405)
def method_not_allowed(e):
    return err("Method not allowed.", 405)

@app.errorhandler(413)
def file_too_large(e):
    return err("File too large. Maximum size is 20 MB.", 413)

@app.errorhandler(500)
def internal_error(e):
    logger.error("Internal server error: %s", e, exc_info=True)
    db.session.rollback()
    return err("Internal server error.", 500)


@jwt.expired_token_loader
def expired_token(jwt_header, jwt_payload):
    return err("Token has expired.", 401)

@jwt.invalid_token_loader
def invalid_token(error):
    return err("Invalid token.", 401)

@jwt.unauthorized_loader
def missing_token(error):
    return err("Authorization token is missing.", 401)


# ═══════════════════════════════════════════════════════════════════
# DATABASE INITIALISATION & SEEDING
# ═══════════════════════════════════════════════════════════════════

_CATEGORIES = [
    ("Consumer Complaint",  "Consumer product or service issues",            "product,defective,refund,seller,purchase,ecommerce"),
    ("Labour Complaint",    "Employment and workplace related complaints",    "salary,employer,workplace,job,harassment,termination"),
    ("Cyber Crime",         "Online fraud and cyber incidents",              "online,fraud,hack,phishing,scam,cyber,internet"),
    ("Property Dispute",    "Land and property related issues",              "land,property,rent,tenant,encroachment,lease"),
    ("Banking Complaint",   "Bank and financial institution complaints",     "bank,loan,account,credit,debit,emi,fraud,atm"),
    ("Insurance Complaint", "Insurance claim and policy disputes",           "insurance,claim,policy,premium,settlement"),
    ("Municipal Complaint", "Civic amenities and municipal issues",          "water,roads,garbage,electricity,municipality,drainage"),
    ("RTI",                 "Right to Information requests",                 "rti,information,government,public,transparency"),
    ("Women Safety",        "Women safety and harassment complaints",        "harassment,dowry,domestic,violence,women,safety"),
    ("Tenant Dispute",      "Landlord and tenant conflicts",                 "rent,landlord,tenant,eviction,deposit,lease"),
]

_DEPARTMENTS = [
    ("Consumer Commission",          "Handles consumer disputes",                         "https://consumerhelpline.gov.in",  "1800-11-4000", "consumerhelpline@nic.in"),
    ("Labour Department",            "Handles employment and labour disputes",             "https://labour.gov.in",            "1800-11-2222", "labour@nic.in"),
    ("Cyber Crime Cell",             "Handles cyber crime complaints",                     "https://cybercrime.gov.in",        "1930",         "cybercrime@nic.in"),
    ("Land Revenue Department",      "Handles property and land disputes",                "https://dolr.gov.in",              None,           "dolr@nic.in"),
    ("Banking Ombudsman",            "Handles banking related complaints",                 "https://bankingombudsman.rbi.org", "14448",        "rbi@rbi.org.in"),
    ("IRDAI",                        "Insurance Regulatory and Development Authority",     "https://www.irdai.gov.in",         "155255",       "complaints@irdai.gov.in"),
    ("Municipal Corporation",        "Handles civic and municipal complaints",             None,                               None,           None),
    ("Central Information Commission","Handles RTI appeals and complaints",               "https://cic.gov.in",               None,           "cic@nic.in"),
    ("National Commission for Women","Handles women safety and harassment cases",         "https://ncw.nic.in",               "7827170170",   "ncw@nic.in"),
    ("District Court",               "Handles civil disputes including tenant issues",     None,                               None,           None),
    ("Police Department",            "Handles criminal complaints and FIR registration",  None,                               "100",          None),
]


def init_db():
    """Create all tables and seed reference data."""
    db.create_all()
    logger.info("Tables created (if not existing).")

    for name, desc, kw in _CATEGORIES:
        if not ComplaintCategory.query.filter_by(category_name=name).first():
            db.session.add(ComplaintCategory(category_name=name, description=desc, keywords=kw))

    for name, desc, web, helpline, email in _DEPARTMENTS:
        if not Department.query.filter_by(department_name=name).first():
            db.session.add(Department(department_name=name, description=desc,
                                      website=web, helpline=helpline, email=email))

    if not User.query.filter_by(email="admin@judiciaryflow.in").first():
        db.session.add(User(
            full_name="System Administrator",
            email="admin@judiciaryflow.in",
            mobile="9000000000",
            password_hash=generate_password_hash("Admin@123456"),
            role="admin",
        ))

    db.session.commit()
    logger.info("Database seeded. Admin: admin@judiciaryflow.in / Admin@123456")


# ═══════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    with app.app_context():
        init_db()
    port = int(os.environ.get("PORT", 5000))
    logger.info("Starting Judiciary Flow backend on port %d …", port)
    app.run(host="0.0.0.0", port=port, debug=False)
