from flask import Blueprint, request, make_response, jsonify
from app.auth.helper import token_required

# Initialize blueprint
bucket = Blueprint('bucket', __name__)


@bucket.route('/bucketlists', methods=['GET'])
@token_required
def bucketlist(current_user):
    return make_response(jsonify({'message': current_user.email}))
