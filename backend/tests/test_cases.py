"""
test_cases.py – Tests for case management system endpoints.
"""

def test_create_case_success(client, auth_headers):
    res = client.post("/api/v1/cases", headers=auth_headers, json={
        "title": "Property Dispute Settlement",
        "category": "Property Dispute",
        "description": "Boundary dispute regarding plot 402 in Dwarka sector 4.",
        "priority": "High"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["success"] is True
    assert "case_id" in data


def test_list_cases(client, auth_headers):
    res = client.get("/api/v1/cases", headers=auth_headers)
    assert res.status_code == 200
    assert isinstance(res.get_json()["data"], list)


def test_update_case(client, auth_headers):
    create_res = client.post("/api/v1/cases", headers=auth_headers, json={
        "title": "Case To Update",
        "category": "Consumer Complaint",
        "description": "Initial description."
    })
    case_id = create_res.get_json()["case_id"]

    update_res = client.put(f"/api/v1/cases/{case_id}", headers=auth_headers, json={
        "title": "Case Updated Title",
        "status": "Active"
    })
    assert update_res.status_code == 200
    assert update_res.get_json()["data"]["title"] == "Case Updated Title"
    assert update_res.get_json()["data"]["status"] == "Active"


def test_archive_case(client, auth_headers):
    create_res = client.post("/api/v1/cases", headers=auth_headers, json={
        "title": "Case To Archive",
        "category": "Labour Complaint"
    })
    case_id = create_res.get_json()["case_id"]

    del_res = client.delete(f"/api/v1/cases/{case_id}", headers=auth_headers)
    assert del_res.status_code == 200
    assert del_res.get_json()["data"]["status"] == "Archived"
