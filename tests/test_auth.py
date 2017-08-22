from tests.base import BaseTestCase
from app.models import User
from app import db
import unittest
import json


class TestAuthBluePrint(BaseTestCase):
    def test_user_registration(self):
        """
        Test a user is successfully created through the api
        :return:
        """
        with self.client:
            response = self.register_user()
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_user_registration_fails_if_content_type_not_json(self):
        """
        Test the content type is application/json
        :return:
        """
        response = self.client.post(
            '/auth/register',
            content_type='application/javascript',
            data=json.dumps(dict(email='sdfsd@gmail.com', password='123456')))
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'failed', msg='Should return failed')
        self.assertTrue(data['message'] == 'Content-type must be json')
        self.assertEqual(response.status_code, 202)

    def test_user_registration_missing_email_or_and_password(self):
        """
        Test that the email and password are set when sending the request
        :return:
        """
        response = self.client.post(
            '/auth/register',
            content_type='application/json',
            data=json.dumps(dict(email='', password='')))
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'failed', msg='Should return failed')
        self.assertTrue(data['message'] == 'Missing or wrong email format or password is less than four characters')

    def test_user_email_validity(self):
        """
        Check that the user has supplied a valid email address.
        :return:
        """
        response = self.client.post(
            '/auth/register',
            content_type='application/json',
            data=json.dumps(dict(email='john', password='123456')))
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'failed', msg='Should return failed')
        self.assertTrue(data['message'] == 'Missing or wrong email format or password is less than four characters')

    def test_user_password_length_is_greater_than_four_characters(self):
        response = self.client.post(
            '/auth/register',
            content_type='application/json',
            data=json.dumps(dict(email='john@gmail.com', password='123')))
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'failed', msg='Should return failed')
        self.assertTrue(data['message'] == 'Missing or wrong email format or password is less than four characters')

    def test_user_is_already_registered(self):
        """
        Test that the user already exists.
        :return:
        """
        user = User('example@gmail.com', '123456')
        db.session.add(user)
        db.session.commit()

        response = self.register_user()
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'failed')
        self.assertTrue(data['message'] == 'Failed, User already exists, Please sign In')
        self.assertEqual(response.status_code, 202)

    def register_user(self):
        """
        Helper method for registering a user with dummy data
        :return:
        """
        return self.client.post(
            '/auth/register',
            content_type='application/json',
            data=json.dumps(dict(email='example@gmail.com', password='123456')))


if __name__ == '__main__':
    unittest.main()
