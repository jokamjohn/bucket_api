from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db, models
from app.models import User, Bucket, BucketItem
import unittest
import coverage
import os
import forgery_py as faker
from random import randint
from sqlalchemy.exc import IntegrityError

# Initializing the manager
manager = Manager(app)

# Initialize Flask Migrate
migrate = Migrate(app, db)

# Add the flask migrate
manager.add_command('db', MigrateCommand)

# Test coverage configuration
COV = coverage.coverage(
    branch=True,
    include='app/*',
    omit=[
        'app/auth/__init__.py',
        'app/bucket/__init__.py',
        'app/bucketitems/__init__.py'
    ]
)
COV.start()


# Add test command
@manager.command
def test():
    """
    Run tests without coverage
    :return:
    """
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def dummy():
    # Create a user if they do not exist.
    user = User.query.filter_by(email="example@bucketmail.com").first()
    if not user:
        user = User("example@bucketmail.com", "123456")
        user.save()

    for i in range(100):
        # Add buckets to the database
        bucket = Bucket(faker.name.industry(), user.id)
        bucket.save()

    for buck in range(1000):
        # Add items to the bucket
        buckt = Bucket.query.filter_by(id=randint(1, Bucket.query.count() - 1)).first()
        item = BucketItem(faker.name.company_name(), faker.lorem_ipsum.word(), buckt.id)
        db.session.add(item)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


# Run the manager
if __name__ == '__main__':
    manager.run()
