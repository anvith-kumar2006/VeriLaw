"""Application configuration loaded from the project .env file."""

import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def _database_url():
    """Use DATABASE_URL, or construct a MySQL URL from DB_* settings."""
    database_url = os.environ.get("DATABASE_URL", "").strip()
    if database_url:
        return database_url

    host = os.environ.get("DB_HOST", "").strip()
    name = os.environ.get("DB_NAME", "").strip()
    user = os.environ.get("DB_USER", "").strip()
    password = os.environ.get("DB_PASSWORD", "")
    port = os.environ.get("DB_PORT", "3306").strip()
    if host and name and user:
        return (
            f"mysql+pymysql://{quote_plus(user)}:{quote_plus(password)}"
            f"@{host}:{port}/{quote_plus(name)}"
        )
    return ""


class Config:
    """Default application configuration."""

    DATABASE_URL = _database_url()
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "")
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
    GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")
    UPLOAD_FOLDER = str(BASE_DIR / "uploads")
    GENERATED_DOCS_FOLDER = str(BASE_DIR / "generated_documents")
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024
    PORT = int(os.environ.get("PORT", "3000"))
