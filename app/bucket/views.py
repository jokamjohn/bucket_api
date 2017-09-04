from flask import Blueprint, request, abort
from app.auth.helper import token_required
from app.bucket.helper import response, response_for_created_bucket, response_for_user_bucket, get_response, \
    get_user_bucket_json_list
from app.models import User, Bucket
from app import db
from sqlalchemy import exc

# Initialize blueprint
bucket = Blueprint('bucket', __name__)


@bucket.route('/bucketlists', methods=['GET'])
@token_required
def bucketlist(current_user):
    """
    Return all the buckets owned by the user or limit them to 10.
    Return an empty buckets object if user has no buckets
    :param current_user:
    :return:
    """
    try:
        user = User.query.filter_by(id=current_user.id).first()
        user_buckets = user.buckets.limit(10).all()
    except exc.DatabaseError as error:
        return response('failed', 'Operation failed try again', 202)
    else:
        if user_buckets:
            return get_response(get_user_bucket_json_list(user_buckets))
        return get_response({})


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
                db.session.add(user_bucket)
                db.session.commit()
            except exc.DatabaseError as error:
                return response('failed', 'Operation failed, try again', 202)
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
        try:
            user = User.query.filter_by(id=current_user.id).first()
            user_bucket = user.buckets.filter_by(id=bucket_id).first()
        except exc.DatabaseError:
            return response('failed', 'Operation Failed, try again', 202)
        else:
            if user_bucket:
                return response_for_user_bucket(user_bucket.json())
            return response_for_user_bucket([])
    except ValueError:
        return response('failed', 'Please provide a valid Bucket Id', 400)


@bucket.route('/bucketlists/<bucket_id>', methods=['PUT'])
@token_required
def edit_bucket(current_user, bucket_id):
    if request.content_type == 'application/json':
        data = request.get_json()
        name = data.get('name')
        if name:
            try:
                int(bucket_id)
            except ValueError:
                return response('failed', 'Please provide a valid Bucket Id', 400)
            try:
                user = User.query.filter_by(id=current_user.id).first()
                user_bucket = user.buckets.filter_by(id=bucket_id).first()
                user_bucket.update(name)
            except exc.DatabaseError as error:
                return response('failed', 'Operation failed, try again', 202)
            return response_for_created_bucket(user_bucket, 201)
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
        try:
            user = User.query.filter_by(id=current_user.id).first()
            user_bucket = user.buckets.filter_by(id=bucket_id).first()
            if not user_bucket:
                abort(404)
            user_bucket.delete()
        except exc.DatabaseError:
            return response('failed', 'Operation Failed, try again', 202)
        return response('success', 'Bucket Deleted successfully', 200)
    except ValueError:
        return response('failed', 'Please provide a valid Bucket Id', 400)


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
