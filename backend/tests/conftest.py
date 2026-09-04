"""
conftest.py – Pytest fixtures for isolated backend testing using SQLite in-memory DB.
"""

import pytest
import os
import sys

# Ensure backend directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))

from app import create_app, init_db
from extensions import db
from models import User
from werkzeug.security import generate_password_hash


@pytest.fixture(scope="session")
def app():
    """Create application configured for testing with in-memory SQLite."""
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test-secret-key-for-pytest",
        "PRESERVE_CONTEXT_ON_EXCEPTION": False,
        "RATELIMIT_ENABLED": False,
    }
    _app = create_app(test_config)

    with _app.app_context():
        init_db()
        yield _app


@pytest.fixture(scope="function")
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture(scope="function")
def db_session(app):
    """Provide a clean database session for tests."""
    with app.app_context():
        yield db.session


@pytest.fixture
def auth_headers(client):
    """Create a standard citizen user and return authorization headers."""
    email = "testcitizen@verilaw.in"
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(
            full_name="Test Citizen",
            email=email,
            mobile="9876543210",
            password_hash=generate_password_hash("Password@123"),
            role="citizen",
        )
        db.session.add(user)
        db.session.commit()

    res = client.post("/api/v1/auth/login", json={
        "email": email,
        "password": "Password@123",
    })
    token = res.get_json()["data"]["token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(client):
    """Create an admin user and return authorization headers."""
    email = "admin@judiciaryflow.in"
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(
            full_name="System Administrator",
            email=email,
            mobile="9000000000",
            password_hash=generate_password_hash("Admin@123456"),
            role="admin",
        )
        db.session.add(user)
        db.session.commit()

    res = client.post("/api/v1/auth/login", json={
        "email": email,
        "password": "Admin@123456",
    })
    token = res.get_json()["data"]["token"]
    return {"Authorization": f"Bearer {token}"}
