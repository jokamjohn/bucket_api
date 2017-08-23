from tests.base import BaseTestCase
import unittest
import json


class TestBucketBluePrint(BaseTestCase):
    def test_creating_a_bucket(self):
        """
        Test that a user can add a bucket
        :return:
        """
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

    def test_user_can_get_list_of_buckets(self):
        """
        Test that a user gets back a list of their buckets or an empty dictionary if they do not have any yet
        :return:
        """
        with self.client:
            response = self.client.get(
                '/bucketlists',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['status'] == 'success')
            self.assertIsInstance(data['buckets'], dict)

    def test_request_for_a_bucket_has_integer_id(self):
        """
        Test that only integer bucket Ids are allowed
        :return:
        """
        with self.client:
            response = self.client.get(
                '/bucketlists/dsfgsdsg',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Please provide a valid Bucket Id')

    def test_bucket_is_returned(self):
        """
        Test that a user bucket is returned when a specific Id is specified
        :return:
        """
        with self.client:
            response = self.client.get(
                '/bucketlists/1',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['status'] == 'success')
            self.assertIsInstance(data['bucket'], dict)


if __name__ == '__main__':
    unittest.main()
