"""
test_evidence.py – Tests for evidence file handling and documents generation.
"""

import io

def test_evidence_upload_and_list(client, auth_headers):
    # Create complaint first
    c_res = client.post("/api/v1/complaints", headers=auth_headers, json={
        "title": "Complaint for Evidence Upload",
        "description": "Valid complaint description with enough length for testing upload.",
        "state": "Maharashtra",
        "district": "Mumbai"
    })
    complaint_id = c_res.get_json()["data"]["complaint_id"]

    # Upload evidence file
    data = {
        "complaint_id": str(complaint_id),
        "files": (io.BytesIO(b"Dummy PDF content for testing"), "agreement.pdf")
    }
    up_res = client.post("/api/v1/evidence/upload", headers=auth_headers, data=data, content_type="multipart/form-data")
    assert up_res.status_code == 201
    assert up_res.get_json()["data"]["uploaded_files"] == 1

    # List evidence
    list_res = client.get(f"/api/v1/evidence/{complaint_id}", headers=auth_headers)
    assert list_res.status_code == 200
    assert len(list_res.get_json()["data"]) == 1
    assert list_res.get_json()["data"][0]["original_name"] == "agreement.pdf"


def test_document_generate(client, auth_headers):
    c_res = client.post("/api/v1/complaints", headers=auth_headers, json={
        "title": "Complaint for Document Generation",
        "description": "Valid complaint description with enough length for document generation.",
        "state": "Delhi",
        "district": "New Delhi"
    })
    complaint_id = c_res.get_json()["data"]["complaint_id"]

    gen_res = client.post("/api/v1/documents/generate", headers=auth_headers, json={
        "complaint_id": complaint_id,
        "document_type": "HTML"
    })
    assert gen_res.status_code == 201
    data = gen_res.get_json()["data"]
    assert "document_id" in data
    assert "download_url" in data
