import unittest
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from app import app, db, init_db

class TestJudiciaryFlowAPI(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()
            init_db()

    def test_health(self):
        res = self.client.get('/api/v1/health')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])

    def test_auth_flow(self):
        # Register
        reg_payload = {
            "full_name": "Test User",
            "email": "test@example.com",
            "mobile": "9876543210",
            "password": "password123",
            "role": "citizen"
        }
        res = self.client.post('/api/v1/auth/register', json=reg_payload)
        self.assertEqual(res.status_code, 201)

        # Login
        login_payload = {
            "email": "test@example.com",
            "password": "password123"
        }
        res = self.client.post('/api/v1/auth/login', json=login_payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        token = data['data']['token']

        # Profile
        res = self.client.get('/api/v1/profile', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(res.status_code, 200)

    def test_complaint_flow(self):
        # Register & Login
        self.client.post('/api/v1/auth/register', json={
            "full_name": "Citizen User",
            "email": "citizen@example.com",
            "mobile": "9876543211",
            "password": "password123"
        })
        res = self.client.post('/api/v1/auth/login', json={
            "email": "citizen@example.com",
            "password": "password123"
        })
        token = res.get_json()['data']['token']
        headers = {'Authorization': f'Bearer {token}'}

        # Create Complaint
        complaint_payload = {
            "title": "Defective TV Purchase",
            "description": "I purchased a smart TV which stopped working after two days and the seller is refusing refund.",
            "state": "Delhi",
            "district": "New Delhi",
            "incident_date": "2026-07-01"
        }
        res = self.client.post('/api/v1/complaints', json=complaint_payload, headers=headers)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        complaint_id = data['data']['complaint_id']

        # List Complaints
        res = self.client.get('/api/v1/complaints', headers=headers)
        self.assertEqual(res.status_code, 200)

        # AI Classify
        res = self.client.post('/api/v1/ai/classify', json={"description": "Defective TV purchased from seller"}, headers=headers)
        self.assertEqual(res.status_code, 200)

        # Document Generation
        res = self.client.post('/api/v1/documents/generate', json={"complaint_id": complaint_id, "document_type": "PDF"}, headers=headers)
        self.assertEqual(res.status_code, 201)

if __name__ == '__main__':
    unittest.main()
