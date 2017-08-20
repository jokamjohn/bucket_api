from flask_testing import TestCase
from app import app
from flask import current_app
import unittest


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        """
        Create an app with the development configuration
        :return:
        """
        app.config.from_object('app.config.DevelopmentConfig')
        return app

    def test_app_in_development(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'john kagga')
        self.assertTrue(app.config['DEBUG'], True)
        self.assertTrue(app.config['BCRYPT_HASH_PREFIX'] == 4)
        self.assertFalse(current_app is None)
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == "postgresql://postgres:123456@localhost/api")


class TestTestingConfig(TestCase):
    def create_app(self):
        """
                Create an instance of the app with the testing configuration
                :return:
                """
        app.config.from_object('app.config.TestingConfig')
        return app

    def test_app_in_testing(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'john kagga')
        self.assertTrue(app.config['DEBUG'], True)
        self.assertTrue(app.config['TESTING'] is True)
        self.assertTrue(app.config['BCRYPT_HASH_PREFIX'] == 4)
        self.assertFalse(current_app is None)
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == "postgresql://postgres:123456@localhost/api_test")


if __name__ == '__main__':
    unittest.main()
