from tests.base import BaseTestCase
import unittest
import json


class TestAuthBluePrint(BaseTestCase):
    def test_user_registration(self):
        """
        Test a user is successfully created through the api
        :return:
        """
        with self.client:
            response = self.client.post(
                'auth/register',
                data=json.dumps(dict(email='example@gmail.com', password='123456')),
                content_type='application/json'
            )
            data = json.load(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)


if __name__ == '__main__':
    unittest.main()
