import unittest

from app import app

JOHN_DOE = {"id": 1, "name": "John Doe"}
NEW_JOHN_DOE = {"name": "John Doe"}


class ApiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()

    def test1_new_user(self):
        response = self.app.post("/users", json=NEW_JOHN_DOE)
        self.assertEqual(response.status_code, 204)

    def test1_new_user_broken(self):
        response = self.app.post("/users", json={"id": 2, "name": "Foo Bar"})
        self.assertEqual(response.status_code, 400)

    def test2_get_users(self):
        response = self.app.get("/users")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data, [JOHN_DOE])

    def test2_get_user(self):
        response = self.app.get("/users/1")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data, JOHN_DOE)

    def test2_404(self):
        response = self.app.get("/users/2")
        self.assertEqual(response.status_code, 404)
