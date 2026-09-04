"""
Judiciary Flow (VeriLaw) — Modular Flask Backend Application Factory
Stack: Flask + Flask-SQLAlchemy + Flask-JWT-Extended + Flask-CORS + Flask-Limiter
"""

import os
import logging
from datetime import timedelta

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash
from sqlalchemy import text

from extensions import db, jwt
from config import Config
from utils.helpers import ok, err

# ──────────────────────────────────────────────────────────────────────
# LOGGING SETUP
# ──────────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("verilaw")


# ──────────────────────────────────────────────────────────────────────
# APPLICATION FACTORY
# ──────────────────────────────────────────────────────────────────────

def create_app(config_override=None):
    app = Flask(
        __name__,
        static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend")),
        static_url_path="/",
    )

    # ── Database Config ───────────────────────────────────────────────
    database_url = Config.DATABASE_URL
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    if not database_url:
        database_url = "sqlite:///verilaw.db"
        logger.warning("DATABASE_URL not set — falling back to SQLite (dev only).")

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ── JWT Config ───────────────────────────────────────────────────
    flask_env = os.environ.get("FLASK_ENV", "development").lower()
    jwt_secret = Config.JWT_SECRET_KEY or os.environ.get("SESSION_SECRET")

    if not jwt_secret:
        if flask_env == "production":
            raise RuntimeError("JWT_SECRET_KEY environment variable MUST be set in production!")
        jwt_secret = "judiciary-flow-jwt-secret-dev-only-change-in-prod"
        logger.warning("Using default dev JWT_SECRET_KEY. DO NOT USE IN PRODUCTION.")

    app.config["JWT_SECRET_KEY"] = jwt_secret
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_HEADER_NAME"] = "Authorization"
    app.config["JWT_HEADER_TYPE"] = "Bearer"

    # ── Upload Folders ────────────────────────────────────────────────
    upload_folder = Config.UPLOAD_FOLDER
    generated_docs_folder = Config.GENERATED_DOCS_FOLDER
    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(generated_docs_folder, exist_ok=True)

    app.config["MAX_CONTENT_LENGTH"] = Config.MAX_CONTENT_LENGTH

    if config_override:
        app.config.update(config_override)

    # Adjust SQLAlchemy pool options per dialect — MUST happen AFTER config_override
    # so test fixtures overriding DATABASE_URI to sqlite are respected.
    final_db_url = app.config["SQLALCHEMY_DATABASE_URI"]
    if final_db_url.startswith("sqlite"):
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "connect_args": {"timeout": 30, "check_same_thread": False},
        }
    else:
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "pool_recycle": 300,
            "pool_pre_ping": True,
            "pool_size": 5,
            "max_overflow": 10,
        }

    # ── Initialize Extensions ─────────────────────────────────────────
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # ── Rate Limiter ──────────────────────────────────────────────────
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://",
    )

    # ── Register Blueprints ───────────────────────────────────────────
    from routes.auth import auth_bp
    from routes.users import users_bp
    from routes.complaints import complaints_bp
    from routes.cases import cases_bp
    from routes.ai import ai_bp
    from routes.evidence import evidence_bp
    from routes.documents import documents_bp
    from routes.appointments import appointments_bp
    from routes.chat import chat_bp
    from routes.notifications import notifications_bp
    from routes.reports import reports_bp
    from routes.admin import admin_bp
    from routes.ocr import ocr_bp
    from routes.timeline import timeline_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(complaints_bp)
    app.register_blueprint(cases_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(evidence_bp)
    app.register_blueprint(documents_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(ocr_bp)
    app.register_blueprint(timeline_bp)

    # ── Health Check ──────────────────────────────────────────────────
    @app.route("/api/v1/health", methods=["GET"])
    def health_check():
        try:
            db.session.execute(text("SELECT 1"))
            return ok({"status": "healthy", "database": "connected", "version": "1.0.0"})
        except Exception as exc:
            return err(f"Database error: {exc}", 503)

    # ── Global Error Handlers ─────────────────────────────────────────
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

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return err("Rate limit exceeded. Please try again later.", 429)

    @app.errorhandler(500)
    def internal_error(e):
        logger.error("Internal server error: %s", e, exc_info=True)
        db.session.rollback()
        return err("Internal server error.", 500)

    # ── JWT Error Loaders ─────────────────────────────────────────────
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        if hasattr(user, 'user_id'):
            return str(user.user_id)
        return str(user)

    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_payload):
        return err("Token has expired.", 401)

    @jwt.invalid_token_loader
    def invalid_token(error):
        logger.error("JWT validation error: %s", error)
        return err(f"Invalid token: {error}", 401)

    @jwt.unauthorized_loader
    def missing_token(error):
        return err("Authorization token is missing.", 401)

    # ── Static Frontend Serving ───────────────────────────────────────
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve(path):
        static_folder = app.static_folder
        if static_folder is None:
            return err("Frontend folder is not configured.", 500)
        if path.startswith("api/"):
            return jsonify({"success": False, "message": "API endpoint not found"}), 404
        if path != "" and os.path.exists(os.path.join(static_folder, path)):
            return send_from_directory(static_folder, path)
        else:
            return send_from_directory(static_folder, "index.html")

    return app


# ──────────────────────────────────────────────────────────────────────
# SEEDING & DATABASE INITIALIZATION
# ──────────────────────────────────────────────────────────────────────

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
    from models import User, ComplaintCategory, Department

    db.create_all()
    logger.info("Tables created (if not existing).")

    for name, desc, kw in _CATEGORIES:
        if not ComplaintCategory.query.filter_by(category_name=name).first():
            db.session.add(ComplaintCategory(category_name=name, description=desc, keywords=kw))

    for name, desc, web, helpline, email in _DEPARTMENTS:
        if not Department.query.filter_by(department_name=name).first():
            db.session.add(Department(department_name=name, description=desc,
                                      website=web, helpline=helpline, email=email))

    # Secure Admin Initialisation: Read password from env var with safe fallback for dev
    admin_email = os.environ.get("ADMIN_EMAIL", "admin@judiciaryflow.in")
    admin_pass = os.environ.get("ADMIN_PASSWORD", "Admin@123456")

    if not User.query.filter_by(email=admin_email).first():
        db.session.add(User(
            full_name="System Administrator",
            email=admin_email,
            mobile="9000000000",
            password_hash=generate_password_hash(admin_pass),
            role="admin",
        ))

    db.session.commit()
    logger.info("Database seeded.")


# Create application instance
app = create_app()

if __name__ == "__main__":
    with app.app_context():
        init_db()
    port = Config.PORT
    logger.info("Starting Judiciary Flow backend on port %d …", port)
    app.run(host="0.0.0.0", port=port, debug=False)
