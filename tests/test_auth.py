import unittest
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from app import app, db, init_db

class TestAuthAndProfile(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()
            init_db()

    def test_user_registration_and_login(self):
        reg = self.client.post('/api/v1/auth/register', json={
            "full_name": "Alice Smith",
            "email": "alice@example.com",
            "mobile": "9876543210",
            "password": "Password123!",
            "role": "citizen"
        })
        self.assertEqual(reg.status_code, 201)

        login = self.client.post('/api/v1/auth/login', json={
            "email": "alice@example.com",
            "password": "Password123!"
        })
        self.assertEqual(login.status_code, 200)
        token = login.get_json()['data']['token']

        # Profile fetch
        profile = self.client.get('/api/v1/profile', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(profile.status_code, 200)
        self.assertEqual(profile.get_json()['data']['full_name'], "Alice Smith")

        # Update profile
        upd = self.client.put('/api/v1/profile', json={
            "full_name": "Alice Johnson",
            "mobile": "9876543211"
        }, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(upd.status_code, 200)

        # Logout
        logout = self.client.post('/api/v1/auth/logout', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(logout.status_code, 200)

if __name__ == '__main__':
    unittest.main()
