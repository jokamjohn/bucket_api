from flask import Blueprint, request, make_response, jsonify
from app.auth.helper import token_required
from app.models import Bucket

# Initialize blueprint
bucket = Blueprint('bucket', __name__)


@bucket.route('/bucketlists', methods=['GET'])
@token_required
def bucketlist(current_user):
    return make_response(jsonify({'message': current_user.email}))


@bucket.route('/bucketlists', methods=['POST'])
@token_required
def create_bucketlist(current_user):
    """
    Create a Bucket from the sent json data.
    :param current_user: Current User
    :return:
    """
    if request.content_type == 'application/json':
        data = request.get_json()
        name = data.get('name')
        if name:
            try:
                user_bucket = Bucket(name, current_user.id)
                user_bucket.save()
            except Exception as e:
                return response('failed', 'Operation failed, try again', 202)
            return response_create_bucket(user_bucket)
        return response('failed', 'Missing name attribute', 400)
    return response('failed', 'Content-type must be json', 202)


def response_create_bucket(user_bucket):
    """
    Method returning the response when a bucket has been successfully created.
    :param user_bucket: Bucket
    :return: Http Response
    """
    return make_response(jsonify({
        'status': 'success',
        'id': user_bucket.id,
        'name': user_bucket.name,
        'createdAt': user_bucket.create_at,
        'modifiedAt': user_bucket.modified_at
    })), 201


def response(status, message, code):
    """
    Helper method to make a http response
    :param status: Status message
    :param message: Response message
    :param code: Response status code
    :return: Http Response
    """
    return make_response(jsonify({
        'status': status,
        'message': message
    })), code
