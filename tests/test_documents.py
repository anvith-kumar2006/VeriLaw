import unittest
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from app import app, db, init_db

class TestDocumentGeneration(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()
            init_db()

        self.client.post('/api/v1/auth/register', json={
            "full_name": "Eve Adams",
            "email": "eve@example.com",
            "mobile": "9776655443",
            "password": "Password123!",
            "role": "citizen"
        })
        login = self.client.post('/api/v1/auth/login', json={
            "email": "eve@example.com",
            "password": "Password123!"
        })
        self.token = login.get_json()['data']['token']
        self.headers = {'Authorization': f'Bearer {self.token}'}

        res = self.client.post('/api/v1/complaints', json={
            "title": "Defective Washing Machine Purchase",
            "description": "Appliance stopped spinning after 3 days. Service center refuses replacement.",
            "state": "Maharashtra",
            "district": "Pune",
            "incident_date": "2026-04-10"
        }, headers=self.headers)
        self.complaint_id = res.get_json()['data']['complaint_id']

    def test_document_generation_download_history_delete(self):
        # Generate PDF Document
        res = self.client.post('/api/v1/documents/generate', json={
            "complaint_id": self.complaint_id,
            "document_type": "PDF"
        }, headers=self.headers)
        self.assertEqual(res.status_code, 201)
        doc_id = res.get_json()['data']['document_id']

        # List Documents History
        res = self.client.get('/api/v1/documents', headers=self.headers)
        self.assertEqual(res.status_code, 200)
        docs = res.get_json()['data']
        self.assertTrue(len(docs) > 0)

        # Download Document
        res = self.client.get(f'/api/v1/documents/download/{doc_id}', headers=self.headers)
        self.assertEqual(res.status_code, 200)

        # Delete Document
        res = self.client.delete(f'/api/v1/documents/{doc_id}', headers=self.headers)
        self.assertEqual(res.status_code, 200)

if __name__ == '__main__':
    unittest.main()
