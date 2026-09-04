import unittest
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from app import app, db, init_db

class TestComplaintAndCaseManagement(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()
            init_db()

        # Register & login
        self.client.post('/api/v1/auth/register', json={
            "full_name": "Bob Builder",
            "email": "bob@example.com",
            "mobile": "9123456789",
            "password": "Password123!",
            "role": "citizen"
        })
        login = self.client.post('/api/v1/auth/login', json={
            "email": "bob@example.com",
            "password": "Password123!"
        })
        self.token = login.get_json()['data']['token']
        self.headers = {'Authorization': f'Bearer {self.token}'}

    def test_categories_and_departments(self):
        res = self.client.get('/api/v1/categories')
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(res.get_json()['data']) > 0)

        res = self.client.get('/api/v1/departments')
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(res.get_json()['data']) > 0)

    def test_complaint_crud_and_status(self):
        # Create
        res = self.client.post('/api/v1/complaints', json={
            "title": "Unfair Bank Penalty Fee",
            "description": "The bank deducted penalty fees without prior notice or valid reason from my savings account.",
            "state": "Maharashtra",
            "district": "Mumbai",
            "incident_date": "2026-06-15"
        }, headers=self.headers)
        self.assertEqual(res.status_code, 201)
        c_id = res.get_json()['data']['complaint_id']

        # Get by ID
        res = self.client.get(f'/api/v1/complaints/{c_id}', headers=self.headers)
        self.assertEqual(res.status_code, 200)

        # Update
        res = self.client.put(f'/api/v1/complaints/{c_id}', json={
            "title": "Unfair Bank Penalty Fee Updated"
        }, headers=self.headers)
        self.assertEqual(res.status_code, 200)

        # Reports Summary
        res = self.client.get('/api/v1/reports/summary', headers=self.headers)
        self.assertEqual(res.status_code, 200)

        # Delete
        res = self.client.delete(f'/api/v1/complaints/{c_id}', headers=self.headers)
        self.assertEqual(res.status_code, 200)

    def test_case_management(self):
        # Create case
        res = self.client.post('/api/v1/cases', json={
            "title": "Land Title Verification Case",
            "category": "Property Dispute",
            "description": "Verification of property documents for plot in Delhi.",
            "priority": "High"
        }, headers=self.headers)
        self.assertEqual(res.status_code, 201)
        case_id = res.get_json()['case_id']

        # List cases
        res = self.client.get('/api/v1/cases', headers=self.headers)
        self.assertEqual(res.status_code, 200)

        # Get case
        res = self.client.get(f'/api/v1/cases/{case_id}', headers=self.headers)
        self.assertEqual(res.status_code, 200)

        # Update case
        res = self.client.put(f'/api/v1/cases/{case_id}', json={
            "status": "Active"
        }, headers=self.headers)
        self.assertEqual(res.status_code, 200)

if __name__ == '__main__':
    unittest.main()
