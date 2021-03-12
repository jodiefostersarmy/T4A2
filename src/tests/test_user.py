import os
import unittest
from main import create_app, db
from models.User import User

class TestUsers(unittest.TestCase):

    @classmethod
    def setUp(cls):
        if os.environ.get("FLASK_ENV") != "testing":
            raise EnvironmentError("FLASK_ENV not set to testing")
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()
        db.create_all()
        runner = cls.app.test_cli_runner()
        runner.invoke(args=["db-custom", "seed"])

    @classmethod
    def tearDown(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_user_index(self):
        "returns all users in the database"
        response = self.client.get("/user/")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 3)

    def test_single_user(self):
        "return first user in database -> id=1"
        user = User.query.first()
        response = self.client.get(f"/user/{user.id}")
        data = response.get_json()

        # check status is OK
        self.assertEqual(response.status_code, 200)
        # check response data is dictionary
        self.assertIsInstance(data, dict)
        # check value of response is a string
        self.assertIsInstance(data['name'], str)

    def test_saved_word(self):
        "return list of saved words"
        user = User.query.first()
        response = self.client.get(f"/user/{user.id}/words")
        data = response.get_json()

        #check status is ok
        self.assertEqual(response.status_code, 200)
        # check response data is a list
        self.assertIsInstance(data, list)
        # check value of response is a string
        self.assertIsInstance(data[0]['word'], str)



