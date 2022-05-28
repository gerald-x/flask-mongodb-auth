import unittest
from flask_testing import TestCase
from main import app
from main.models import User, Templates



class BaseTest(TestCase):

    def create_app(self):
        app.config["TESTING"] = True
        return app


class AppTests(BaseTest):

    def test_register(self):
        tester = self.client.get("")

if __name__ == "__main__":
    unittest.main()