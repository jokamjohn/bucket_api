from tests.base import BaseTestCase
import unittest
import json


class TestBucketBluePrint(BaseTestCase):
    def test_creating_a_bucket(self):
        with self.client:
            response = self.client.post(
                '/bucketlists',
                data=json.dumps(dict(name='Travel')),
                headers=dict(Authorization='Bearer ' + self.get_user_token()),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['name'], 'Travel')
            self.assertIsInstance(data['id'], int, msg='Value should be a string')

    def test_name_attribute_is_set_in_bucket_creation_request(self):
        """
        Test that the name attribute is present in the json request.
        :return:
        """
        with self.client:
            response = self.client.post(
                '/bucketlists',
                headers=dict(Authorization='Bearer ' + self.get_user_token()),
                data=json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertTrue(data['status'], 'failed')
            self.assertTrue(data['message'], 'Missing name attribute')

    def test_bucket_post_content_type_is_json(self):
        """
        Test that the request content type is application/json
        :return:
        """
        with self.client:
            response = self.client.post(
                '/bucketlists',
                headers=dict(Authorization='Bearer ' + self.get_user_token()),
                data=json.dumps(dict(name='Travel'))
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 202)
            self.assertTrue(data['status'], 'failed')
            self.assertTrue(data['message'], 'Content-type must be json')


if __name__ == '__main__':
    unittest.main()
