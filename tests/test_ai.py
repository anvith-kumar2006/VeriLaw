import unittest
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from app import app, db, init_db

class TestAIModule(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()
            init_db()

        self.client.post('/api/v1/auth/register', json={
            "full_name": "Charlie Brown",
            "email": "charlie@example.com",
            "mobile": "9988776655",
            "password": "Password123!",
            "role": "citizen"
        })
        login = self.client.post('/api/v1/auth/login', json={
            "email": "charlie@example.com",
            "password": "Password123!"
        })
        self.token = login.get_json()['data']['token']
        self.headers = {'Authorization': f'Bearer {self.token}'}

    def test_ai_classify_and_recommend(self):
        # AI Classify
        res = self.client.post('/api/v1/ai/classify', json={
            "description": "My landlord has illegally evicted me and kept my security deposit."
        }, headers=self.headers)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()['data']
        self.assertIn("category", data)
        self.assertIn("confidence", data)

        # AI Recommend
        res = self.client.post('/api/v1/ai/recommend', json={
            "category": "Consumer Complaint"
        }, headers=self.headers)
        self.assertEqual(res.status_code, 200)
        self.assertIn("department", res.get_json()['data'])

    def test_category_override(self):
        # Create complaint
        res = self.client.post('/api/v1/complaints', json={
            "title": "Property Encroachment Dispute",
            "description": "Neighbor built a wall encroaching onto my registered land plot.",
            "state": "Uttar Pradesh",
            "district": "Noida",
            "incident_date": "2026-05-10"
        }, headers=self.headers)
        self.assertEqual(res.status_code, 201)
        c_id = res.get_json()['data']['complaint_id']

        # Get category id for Property Dispute
        res = self.client.get('/api/v1/categories')
        categories = res.get_json()['data']
        prop_cat = next(c for c in categories if c['category_name'] == 'Property Dispute')

        # Manual Override
        res = self.client.put(f'/api/v1/complaints/{c_id}/category', json={
            "category_id": prop_cat['category_id']
        }, headers=self.headers)
        self.assertEqual(res.status_code, 200)

if __name__ == '__main__':
    unittest.main()
