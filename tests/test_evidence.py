import unittest
import json
import sys
import os
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from app import app, db, init_db

class TestEvidenceOCRTimeline(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()
            init_db()

        self.client.post('/api/v1/auth/register', json={
            "full_name": "Dave Miller",
            "email": "dave@example.com",
            "mobile": "9811223344",
            "password": "Password123!",
            "role": "citizen"
        })
        login = self.client.post('/api/v1/auth/login', json={
            "email": "dave@example.com",
            "password": "Password123!"
        })
        self.token = login.get_json()['data']['token']
        self.headers = {'Authorization': f'Bearer {self.token}'}

        # Create Complaint
        res = self.client.post('/api/v1/complaints', json={
            "title": "Online Shopping Refund Dispute",
            "description": "Item was never delivered and payment was processed via UPI on 12/05/2026 for amount INR 4,500.",
            "state": "Karnataka",
            "district": "Bengaluru",
            "incident_date": "2026-05-12"
        }, headers=self.headers)
        self.complaint_id = res.get_json()['data']['complaint_id']

    def test_evidence_ocr_timeline_flow(self):
        # Upload Evidence File
        file_data = (io.BytesIO(b"Payment Receipt INR 4500 Date 12/05/2026"), "receipt.png")
        upload_res = self.client.post('/api/v1/evidence/upload', data={
            "complaint_id": self.complaint_id,
            "files": file_data
        }, headers=self.headers, content_type='multipart/form-data')
        self.assertEqual(upload_res.status_code, 201)

        # List Evidence
        list_res = self.client.get(f'/api/v1/evidence/{self.complaint_id}', headers=self.headers)
        self.assertEqual(list_res.status_code, 200)
        evidence_items = list_res.get_json()['data']
        self.assertTrue(len(evidence_items) > 0)
        ev_id = evidence_items[0]['evidence_id']

        # OCR Extract
        ocr_res = self.client.post('/api/v1/ocr/extract', json={
            "evidence_id": ev_id
        }, headers=self.headers)
        self.assertEqual(ocr_res.status_code, 200)

        # Entity Extract
        entity_res = self.client.post('/api/v1/ocr/entities', json={
            "evidence_id": ev_id
        }, headers=self.headers)
        self.assertEqual(entity_res.status_code, 200)

        # Timeline Generate
        timeline_res = self.client.post('/api/v1/timeline/generate', json={
            "complaint_id": self.complaint_id
        }, headers=self.headers)
        self.assertEqual(timeline_res.status_code, 200)
        self.assertIn("timeline", timeline_res.get_json()['data'])

        # Delete Evidence
        del_res = self.client.delete(f'/api/v1/evidence/{ev_id}', headers=self.headers)
        self.assertEqual(del_res.status_code, 200)

if __name__ == '__main__':
    unittest.main()
