import unittest
from flask_testing import TestCase
from main import app
from json import dumps
from main.models import User, Templates



class BaseTest(TestCase):

    def create_app(self):
        app.config["TESTING"] = True
        app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] = False
        return app


class AppTests(BaseTest):

    def test_content_type(self):
        route = self.client.get("/template")
        content_type = route.content_type
        self.assertEqual(content_type, "application/json")


    def test_register(self):
        route = self.client.post("/register", data=dumps({
            "email": "johnsmith@gmail.com",
            "first_name": "James",
            "last_name": "Wellbeck",
            "password": "123456"
        }), content_type='application/json')
        print(route.data)

        self.assertEqual(route.status_code, 200)


    def test_register_mail_already_exists(self):
        route = self.client.post("/register", data=dumps({
            "email": "johnsmith@gmail.com",
            "first_name": "John",
            "last_name": "Smith",
            "password": "123456"
        }), content_type='application/json')

        self.assertEqual(route.status_code, 401)

        self.assertTrue(b"message" in route.data)


    def test_login(self):
        pass




if __name__ == "__main__":
    unittest.main()