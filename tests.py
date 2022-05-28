import unittest
from flask_testing import TestCase
from main import app
from json import dumps, loads
from main.models import User, Templates



class BaseTest(TestCase):

    def create_app(self):
        app.config["TESTING"] = True
        app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] = False
        return app



class AppTests(BaseTest):
    token = None

    # test register route
    def test_register(self):
        route = self.client.post("/register", data=dumps({
            "email": "johnsmith@gmail.com",
            "first_name": "James",
            "last_name": "Wellbeck",
            "password": "123456"
        }), content_type='application/json')

        self.assertEqual(route.status_code, 200)


    # test register route with same email to make sure it doesn't store
    def test_register_email_already_exists(self):
        route = self.client.post("/register", data=dumps({
            "email": "johnsmith@gmail.com",
            "first_name": "John",
            "last_name": "Smith",
            "password": "123456"
        }), content_type='application/json')

        self.assertEqual(route.status_code, 401)

        self.assertTrue(b"message" in route.data)


    # test login route
    def test_login(self):
        route = self.client.post("/login", data=dumps({
            "email": "johnsmith@gmail.com",
            "password": "123456"
        }), content_type='application/json')

        self.assertEqual(route.status_code, 200)

        token = loads(route.data.decode("UTF-8"))
        AppTests.token = token.get("access_token")
        self.assertTrue(b"access_token" in route.data)

        user = User.objects(email="johnsmith@gmail.com").first()
        user.delete()

        user_check = User.objects(email="johnsmith@gmail.com").first()
        self.assertEqual(user_check, None)


    # test template route to determine the content type
    def test_content_type(self):
        route = self.client.get("/template",
            headers={
            "Authorization": f"Bearer {AppTests.token}"
            }
        )
        content_type = route.content_type
        self.assertEqual(content_type, "application/json")
    


if __name__ == "__main__":
    unittest.main()