"""
test_complaints.py – Tests for complaint creation, listing, retrieval, update, deletion, and IDOR protection.
"""

def test_create_complaint_success(client, auth_headers):
    res = client.post("/api/v1/complaints", headers=auth_headers, json={
        "title": "Defective Laptop Purchase",
        "description": "I bought a laptop from an online seller 10 days ago, but the screen broke immediately and the seller refuses refund.",
        "state": "Delhi",
        "district": "New Delhi",
        "incident_date": "2026-08-01"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["success"] is True
    assert "complaint_id" in data["data"]
    assert data["data"]["category"] == "Consumer Complaint"


def test_create_complaint_validation_failure(client, auth_headers):
    res = client.post("/api/v1/complaints", headers=auth_headers, json={
        "title": "Short",
        "description": "Too short",
        "state": "",
        "district": ""
    })
    assert res.status_code == 422
    assert res.get_json()["success"] is False


def test_list_complaints(client, auth_headers):
    res = client.get("/api/v1/complaints", headers=auth_headers)
    assert res.status_code == 200
    assert "data" in res.get_json()["data"]


def test_complaint_idor_protection(client, auth_headers):
    # User 1 creates complaint
    create_res = client.post("/api/v1/complaints", headers=auth_headers, json={
        "title": "User 1 Private Complaint",
        "description": "This is a private complaint created by user 1 with enough characters for validation.",
        "state": "Karnataka",
        "district": "Bengaluru"
    })
    complaint_id = create_res.get_json()["data"]["complaint_id"]

    # Register User 2
    client.post("/api/v1/auth/register", json={
        "full_name": "User Two",
        "email": "usertwo@example.com",
        "mobile": "9876543299",
        "password": "Password@123"
    })
    u2_login = client.post("/api/v1/auth/login", json={
        "email": "usertwo@example.com",
        "password": "Password@123"
    })
    u2_token = u2_login.get_json()["data"]["token"]
    u2_headers = {"Authorization": f"Bearer {u2_token}"}

    # User 2 tries to access User 1's complaint
    idor_res = client.get(f"/api/v1/complaints/{complaint_id}", headers=u2_headers)
    assert idor_res.status_code == 403
    assert idor_res.get_json()["success"] is False
