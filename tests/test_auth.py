from tests.base import BaseTestCase
from app.models import User
from app import db
import unittest
import json
import time


class TestAuthBluePrint(BaseTestCase):
    def test_user_registration(self):
        """
        Test a user is successfully created through the api
        :return:
        """
        with self.client:
            response = self.register_user('example@gmail.com', '123456')
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
        with self.client:
            response = self.register_user_with_wrong_request_content_type('example@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed', msg='Should return failed')
            self.assertTrue(data['message'] == 'Content-type must be json')
            self.assertEqual(response.status_code, 202)

    def test_user_registration_missing_email_or_and_password(self):
        """
        Test that the email and password are set when sending the request
        :return:
        """
        with self.client:
            response = self.register_user("", "")
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed', msg='Should return failed')
            self.assertTrue(data['message'] == 'Missing or wrong email format or password is less than four characters')

    def test_user_email_validity(self):
        """
        Check that the user has supplied a valid email address.
        :return:
        """
        with self.client:
            response = self.register_user('john', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed', msg='Should return failed')
            self.assertTrue(data['message'] == 'Missing or wrong email format or password is less than four characters')

    def test_user_password_length_is_greater_than_four_characters(self):
        with self.client:
            response = self.register_user('john@gmail.com', '123')
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

        with self.client:
            response = self.register_user('example@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Failed, User already exists, Please sign In')
            self.assertEqual(response.status_code, 202)

    def test_user_can_login(self):
        """
        Register and login in a user
        :return:
        """
        with self.client:
            self.register_and_login_in_user()

    def test_login_request_payload_is_json(self):
        """
        Test that the content type is application/json
        :return:
        """
        with self.client:
            response = self.client.post(
                '/auth/login',
                content_type='application/javascript',
                data=json.dumps(dict(email='example@gmail.com', password='123456')))
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json',
                            msg='The content type must be application/json')
            self.assertTrue(response.status_code, 202)
            self.assertTrue(data['status'] == 'failed', msg='failed must be returned')
            self.assertTrue(data['message'] == 'Content-type must be json', msg='Check the returned message')

    def test_login_has_correct_email_and_valid_length_password(self):
        """
        Test the email of the user trying to login is valid and the password length is greater than 4 characters
        :return:
        """
        with self.client:
            response = self.login_user('johngmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.content_type == 'application/json')
            self.assertTrue(data['status'] == 'failed', msg='Status should be failed')
            self.assertTrue(data['message'] == 'Missing or wrong email format or password is less than four characters')

    def test_user_trying_to_login_does_not_exist_or_passwords_do_not_much(self):
        """
        Test that the user does not exist or the password is incorrect
        :return:
        """
        with self.client:
            response = self.login_user('john@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'User does not exist or password is incorrect')

    def test_valid_user_log_out(self):
        """
        Test that s user is logged out with a valid auth token
        :return:
        """
        with self.client:
            # Register and login user
            login_data = self.register_and_login_in_user()
            # Logout user
            logout_response = self.logout_user(login_data['auth_token'])
            logout_data = json.loads(logout_response.data.decode())
            self.assertEqual(logout_response.status_code, 200)
            self.assertTrue(logout_data['status'] == 'success')
            self.assertTrue(logout_data['message'] == 'Successfully logged out')

    def test_expired_user_token_user_log_out(self):
        """
        Try to log out a user whose auth token has expired.
        :return:
        """
        with self.client:
            login_data = self.register_and_login_in_user()
            # Pause for 10 seconds
            time.sleep(8)
            # Logout user
            logout_response = self.logout_user(login_data['auth_token'])
            logout_data = json.loads(logout_response.data.decode())
            self.assertTrue(logout_data['status'] == 'failed')
            self.assertTrue(logout_data['message'] == 'Signature expired, Please sign in again')
            self.assertEqual(logout_response.status_code, 401)

    def test_log_out_request_contains_an_authorization_header(self):
        """
        Test that the authorization header is set
        :return:
        """
        with self.client:
            response = self.client.post(
                'auth/logout',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Provide an authorization header')
            self.assertEqual(response.status_code, 403)

    def test_log_out_has_a_valid_token(self):
        """
        Test that a valid authorization token has been sent within the header
        :return:
        """
        with self.client:
            response = self.client.post(
                'auth/logout',
                headers=dict(Authorization='Bearersdfsdvfj.bvdfvbdfxcvxcxcv')
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Provide a valid auth token')
            self.assertEqual(response.status_code, 403)

    def logout_user(self, token):
        """
        Helper method to log out a user
        :param token: Auth token
        :return:
        """
        logout_response = self.client.post(
            'auth/logout',
            headers=dict(Authorization='Bearer ' + token)
        )
        return logout_response

    def register_and_login_in_user(self):
        """
        Helper method to sign up and login a user
        :return:
        """
        reg_response = self.register_user('john@gmail.com', '123456')
        data = json.loads(reg_response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully registered')
        self.assertTrue(data['auth_token'])
        self.assertTrue(reg_response.content_type == 'application/json')
        self.assertEqual(reg_response.status_code, 201)
        # Login the user
        login_response = self.client.post(
            'auth/login',
            data=json.dumps(dict(email='john@gmail.com', password='123456')),
            content_type='application/json'
        )
        login_data = json.loads(login_response.data.decode())
        self.assertEqual(login_response.status_code, 200)
        self.assertTrue(login_data['auth_token'])
        self.assertTrue(login_data['status'] == 'success')
        self.assertTrue(login_data['message'] == 'Successfully logged In')
        self.assertTrue(login_response.content_type == 'application/json')
        return login_data

    def register_user(self, email, password):
        """
        Helper method for registering a user with dummy data
        :return:
        """
        return self.client.post(
            '/auth/register',
            content_type='application/json',
            data=json.dumps(dict(email=email, password=password)))

    def register_user_with_wrong_request_content_type(self, email, password):
        """
        Helper method to register a user using a wrong content-type
        :param email: Email
        :param password: Password
        :return:
        """
        return self.client.post(
            '/auth/register',
            content_type='application/javascript',
            data=json.dumps(dict(email=email, password=password)))

    def login_user(self, email, password):
        """
        Helper method to login a user
        :param email: Email
        :param password: Password
        :return:
        """
        return self.client.post(
            '/auth/login',
            content_type='application/json',
            data=json.dumps(dict(email=email, password=password)))


if __name__ == '__main__':
    unittest.main()
