"""
test_admin.py – Tests for admin role restrictions and endpoints.
"""

def test_admin_access_denied_for_citizen(client, auth_headers):
    res = client.get("/api/v1/admin/stats", headers=auth_headers)
    assert res.status_code == 403
    assert res.get_json()["success"] is False


def test_admin_access_allowed_for_admin(client, admin_headers):
    res = client.get("/api/v1/admin/stats", headers=admin_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "total_users" in data["data"]


def test_admin_list_users(client, admin_headers):
    res = client.get("/api/v1/admin/users", headers=admin_headers)
    assert res.status_code == 200
    assert "data" in res.get_json()["data"]


def test_notifications_and_read_all(client, auth_headers):
    # Fetch notifications
    n_res = client.get("/api/v1/notifications", headers=auth_headers)
    assert n_res.status_code == 200

    # Mark all read
    read_all = client.put("/api/v1/notifications/read-all", headers=auth_headers)
    assert read_all.status_code == 200
    assert read_all.get_json()["success"] is True
