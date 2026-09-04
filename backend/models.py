from typing import Any
from datetime import datetime

try:
    from .extensions import db
except ImportError:
    from extensions import db
# Database models shared by the Flask application.\r\n\r\n# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

class ModelBase(db.Model):
    __abstract__ = True

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)


class User(ModelBase):
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


class LawyerProfile(ModelBase):
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


class ComplaintCategory(ModelBase):
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


class Department(ModelBase):
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


class Complaint(ModelBase):
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


class Evidence(ModelBase):
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


class GeneratedDocument(ModelBase):
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


class ActivityLog(ModelBase):
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


class Appointment(ModelBase):
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


class ChatMessage(ModelBase):
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


class Notification(ModelBase):
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


class Feedback(ModelBase):
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


class Report(ModelBase):
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


class Case(ModelBase):
    __tablename__ = "cases"

    id          = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    user_id     = db.Column(db.Integer,     db.ForeignKey("users.user_id", ondelete="CASCADE"),
                              nullable=False, index=True)
    title       = db.Column(db.String(255), nullable=False)
    category    = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text,        nullable=True)
    status      = db.Column(db.String(50),  nullable=False, default="Draft", index=True)
    priority    = db.Column(db.String(50),  nullable=False, default="Medium", index=True)
    created_at  = db.Column(db.DateTime,    nullable=False, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime,    nullable=False, default=datetime.utcnow,
                              onupdate=datetime.utcnow)

    user = db.relationship("User", foreign_keys=[user_id])

    def to_dict(self):
        return {
            "id":          self.id,
            "user_id":     self.user_id,
            "title":       self.title,
            "category":    self.category,
            "description": self.description,
            "status":      self.status,
            "priority":    self.priority,
            "created_at":  self.created_at.isoformat() if self.created_at else None,
            "updated_at":  self.updated_at.isoformat() if self.updated_at else None,
        }


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

