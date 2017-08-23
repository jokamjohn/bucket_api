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

    def test_bucket_by_id_is_returned_on_get_request(self):
        """
        Test that a user bucket is returned when a specific Id is specified
        :return:
        """
        with self.client:
            token = self.get_user_token()
            # Create a Bucket
            response = self.client.post(
                '/bucketlists',
                data=json.dumps(dict(name='Travel')),
                headers=dict(Authorization='Bearer ' + token),
                content_type='application/json'
            )
            # Test Bucket creation
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['name'], 'Travel')
            response = self.client.get(
                '/bucketlists/1',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['bucket']['name'] == 'Travel')
            self.assertIsInstance(data['bucket'], dict)
            self.assertTrue(response.content_type == 'application/json')

    def test_deletion_handles_no_bucket_found_by_id(self):
        """
        Show tha a 404 response is returned when an un existing bucket is being deleted.
        :return:
        """
        with self.client:
            response = self.client.delete(
                '/bucketlists/1',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Bucket resource cannot be found')
            self.assertTrue(response.content_type == 'application/json')

    def test_request_for_deleting_bucket_has_integer_id(self):
        """
        Test that only integer bucket Ids are allowed
        :return:
        """
        with self.client:
            response = self.client.delete(
                '/bucketlists/dsfgsdsg',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Please provide a valid Bucket Id')

    def test_bucket_is_deleted(self):
        """
        Test that a Bucket is deleted successfully
        :return:
        """
        with self.client:
            # Get an auth token
            token = self.get_user_token()
            # Create a Bucket
            response = self.client.post(
                '/bucketlists',
                data=json.dumps(dict(name='Travel')),
                headers=dict(Authorization='Bearer ' + token),
                content_type='application/json'
            )
            # Test Bucket creation
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['name'], 'Travel')
            # Delete the created Bucket
            res = self.client.delete(
                '/bucketlists/1',
                headers=dict(Authorization='Bearer ' + token)
            )
            print(res.data)
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Bucket Deleted successfully')
            self.assertTrue(res.content_type == 'application/json')


if __name__ == '__main__':
    unittest.main()
