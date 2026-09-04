"""
test_ai.py – Tests for AI classify, recommend, and chat fallback endpoints.
"""

def test_ai_classify(client, auth_headers):
    res = client.post("/api/v1/ai/classify", headers=auth_headers, json={
        "description": "I bought a defective mobile phone from an ecommerce seller and they refused a refund."
    })
    assert res.status_code == 200
    data = res.get_json()["data"]
    assert data["category"] == "Consumer Complaint"
    assert data["confidence"] > 0


def test_ai_recommend(client, auth_headers):
    res = client.post("/api/v1/ai/recommend", headers=auth_headers, json={
        "category": "Consumer Complaint"
    })
    assert res.status_code == 200
    data = res.get_json()["data"]
    assert data["department"] == "Consumer Commission"


def test_ai_chat_fallback(client, auth_headers):
    res = client.post("/api/v1/ai/chat", headers=auth_headers, json={
        "message": "What is the compensation under Section 73 of Indian Contract Act?"
    })
    assert res.status_code == 200
    data = res.get_json()["data"]
    assert "content" in data
    assert len(data["content"]) > 0
