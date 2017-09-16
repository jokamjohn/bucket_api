from flask import Blueprint, request, abort
from app.auth.helper import token_required
from app.bucket.helper import response, response_for_created_bucket, response_for_user_bucket, response_with_pagination, \
    get_user_bucket_json_list, paginate_buckets
from app.models import User, Bucket

# Initialize blueprint
bucket = Blueprint('bucket', __name__)


@bucket.route('/bucketlists/', methods=['GET'])
@token_required
def bucketlist(current_user):
    """
    Return all the buckets owned by the user or limit them to 10.
    Return an empty buckets object if user has no buckets
    :param current_user:
    :return:
    """
    user = User.get_by_id(current_user.id)
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', None, type=str)

    items, nex, pagination, previous = paginate_buckets(current_user.id, page, q, user)

    if items:
        return response_with_pagination(get_user_bucket_json_list(items), previous, nex, pagination.total)
    return response_with_pagination([], previous, nex, 0)


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
            user_bucket = Bucket(name.lower(), current_user.id)
            user_bucket.save()
            return response_for_created_bucket(user_bucket, 201)
        return response('failed', 'Missing name attribute', 400)
    return response('failed', 'Content-type must be json', 202)


@bucket.route('/bucketlists/<bucket_id>', methods=['GET'])
@token_required
def get_bucket(current_user, bucket_id):
    """
    Return a user bucket with the supplied user Id.
    :param current_user: User
    :param bucket_id: Bucket Id
    :return:
    """
    try:
        int(bucket_id)
    except ValueError:
        return response('failed', 'Please provide a valid Bucket Id', 400)
    else:
        user_bucket = User.get_by_id(current_user.id).buckets.filter_by(id=bucket_id).first()
        if user_bucket:
            return response_for_user_bucket(user_bucket.json())
        return response_for_user_bucket([])


@bucket.route('/bucketlists/<bucket_id>', methods=['PUT'])
@token_required
def edit_bucket(current_user, bucket_id):
    """
    Validate the bucket Id. Also check for the name attribute in the json payload.
    If the name exists update the bucket with the new name.
    :param current_user: Current User
    :param bucket_id: Bucket Id
    :return: Http Json response
    """
    if request.content_type == 'application/json':
        data = request.get_json()
        name = data.get('name')
        if name:
            try:
                int(bucket_id)
            except ValueError:
                return response('failed', 'Please provide a valid Bucket Id', 400)
            user_bucket = User.get_by_id(current_user.id).buckets.filter_by(id=bucket_id).first()
            if user_bucket:
                user_bucket.update(name)
                return response_for_created_bucket(user_bucket, 201)
            return response('failed', 'The Bucket with Id ' + bucket_id + ' does not exist', 404)
        return response('failed', 'No attribute or value was specified, nothing was changed', 400)
    return response('failed', 'Content-type must be json', 202)


@bucket.route('/bucketlists/<bucket_id>', methods=['DELETE'])
@token_required
def delete_bucket(current_user, bucket_id):
    """
    Deleting a User Bucket from the database if it exists.
    :param current_user:
    :param bucket_id:
    :return:
    """
    try:
        int(bucket_id)
    except ValueError:
        return response('failed', 'Please provide a valid Bucket Id', 400)
    user_bucket = User.get_by_id(current_user.id).buckets.filter_by(id=bucket_id).first()
    if not user_bucket:
        abort(404)
    user_bucket.delete()
    return response('success', 'Bucket Deleted successfully', 200)


@bucket.errorhandler(404)
def handle_404_error(e):
    """
    Return a custom message for 404 errors.
    :param e:
    :return:
    """
    return response('failed', 'Bucket resource cannot be found', 404)


@bucket.errorhandler(400)
def handle_400_errors(e):
    """
    Return a custom response for 400 errors.
    :param e:
    :return:
    """
    return response('failed', 'Bad Request', 400)
