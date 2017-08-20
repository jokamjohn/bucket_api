from app import app, db
from flask_testing import TestCase


class BaseTestCase(TestCase):
    def create_app(self):
        """
        Create an instance of the app with the testing configuration
        :return:
        """
        app.config.from_object('app.config.TestingConfig')
        return app

    def setUp(self):
        """
        Create the database
        :return:
        """
        db.create_all()
        db.session.commit()

    def tearDown(self):
        """
        Drop the database tables and also remove the session
        :return:
        """
        db.session.remove()
        db.drop_all()
