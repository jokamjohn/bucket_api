from tests.base import BaseTestCase
from app.models import User, Bucket, BucketItem
from manage import dummy
import unittest


class TestManageCase(BaseTestCase):
    def test_dummy_data_successful_creation(self):
        with self.client:
            dummy()
            user = User.query.filter_by(email="example@bucketmail.com").first()
            self.assertTrue(user.email == "example@bucketmail.com")
            self.assertEqual(User.query.count(), 1, msg="User count must be 1")
            self.assertEqual(Bucket.query.count(), 100, msg="Buckets count must be 100")
            self.assertEqual(BucketItem.query.count(), 1000, msg="BucketItems count must be 1000")


if __name__ == '__main__':
    unittest.main()
