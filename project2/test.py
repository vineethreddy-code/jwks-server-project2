import unittest
from main import app  # Now importing the Flask app
import json


class TestJWKSAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_get_jwks(self):
        response = self.client.get('/.well-known/jwks.json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('keys', json.loads(response.data))

    def test_auth_valid_jwt(self):
        response = self.client.post('/auth', json={'username': 'valid_user', 'password': 'valid_pass'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', json.loads(response.data))

    def test_auth_invalid_jwt(self):
        response = self.client.post('/auth', json={'username': 'invalid_user', 'password': 'invalid_pass'})
        self.assertEqual(response.status_code, 401)

    def test_internal_error(self):
        # Simulating an internal error by hitting a non-existent endpoint
        response = self.client.get('/non-existent-endpoint')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
