"""
test_auth.py – Tests for authentication, registration, login, refresh, logout, token revocation.
"""

def test_health_check(client):
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["data"]["status"] == "healthy"


def test_register_success(client):
    res = client.post("/api/v1/auth/register", json={
        "full_name": "John Doe",
        "email": "john@example.com",
        "mobile": "9876543211",
        "password": "Password@123",
        "role": "citizen"
    })
    assert res.status_code == 201
    assert res.get_json()["success"] is True


def test_register_validation_failure(client):
    res = client.post("/api/v1/auth/register", json={
        "full_name": "",
        "email": "invalid-email",
        "mobile": "123",
        "password": "short"
    })
    assert res.status_code == 422
    assert res.get_json()["success"] is False
    assert "errors" in res.get_json()


def test_login_success(client):
    # Register first
    client.post("/api/v1/auth/register", json={
        "full_name": "Login User",
        "email": "loginuser@example.com",
        "mobile": "9876543212",
        "password": "Password@123"
    })

    res = client.post("/api/v1/auth/login", json={
        "email": "loginuser@example.com",
        "password": "Password@123"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "token" in data["data"]
    assert "refresh_token" in data["data"]


def test_login_invalid_credentials(client):
    res = client.post("/api/v1/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    })
    assert res.status_code == 401
    assert res.get_json()["success"] is False


def test_logout_and_token_revocation(client):
    # Register & Login
    client.post("/api/v1/auth/register", json={
        "full_name": "Logout User",
        "email": "logoutuser@example.com",
        "mobile": "9876543213",
        "password": "Password@123"
    })
    login_res = client.post("/api/v1/auth/login", json={
        "email": "logoutuser@example.com",
        "password": "Password@123"
    })
    token = login_res.get_json()["data"]["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Verify protected route works
    profile_res = client.get("/api/v1/profile", headers=headers)
    assert profile_res.status_code == 200

    # Logout
    logout_res = client.post("/api/v1/auth/logout", headers=headers)
    assert logout_res.status_code == 200

    # Verify revoked token is rejected
    after_logout = client.get("/api/v1/profile", headers=headers)
    assert after_logout.status_code == 401
    assert "revoked" in after_logout.get_json()["message"].lower()
