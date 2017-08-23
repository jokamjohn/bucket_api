from flask import Blueprint
from flask.views import MethodView

# Initialize blueprint
bucket = Blueprint('bucket', __name__)


class BucketLists(MethodView):
    def post(self):
        pass

    def get(self):
        pass


# Register view functions
bucketlists_view = BucketLists.as_view('bucketlists')

# Add rule for the endpoint
bucket.add_url_rule('/bucketlists', view_func=bucketlists_view, methods=['POST', 'GET'])
