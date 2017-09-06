from flask import make_response, jsonify, url_for
from app import app
from app.models import User


def response_for_user_bucket(user_bucket):
    """
    Return the response for when a single bucket when requested by the user.
    :param user_bucket:
    :return:
    """
    return make_response(jsonify({
        'status': 'success',
        'bucket': user_bucket
    }))


def response_for_created_bucket(user_bucket, status_code):
    """
    Method returning the response when a bucket has been successfully created.
    :param status_code:
    :param user_bucket: Bucket
    :return: Http Response
    """
    return make_response(jsonify({
        'status': 'success',
        'id': user_bucket.id,
        'name': user_bucket.name,
        'createdAt': user_bucket.create_at,
        'modifiedAt': user_bucket.modified_at
    })), status_code


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


def get_user_bucket_json_list(user_buckets):
    """
    Make json objects of the user buckets and add them to a list.
    :param user_buckets: Bucket
    :return:
    """
    buckets = []
    for user_bucket in user_buckets:
        buckets.append(user_bucket.json())
    return buckets


def response_with_pagination(buckets, previous, nex, count):
    """
    Make a http response for BucketList get requests.
    :param count: Pagination Total
    :param nex: Next page Url if it exists
    :param previous: Previous page Url if it exists
    :param buckets: Bucket
    :return: Http Json response
    """
    return make_response(jsonify({
        'status': 'success',
        'previous': previous,
        'next': nex,
        'count': count,
        'buckets': buckets
    })), 200


def paginate_buckets(current_user, page):
    """
    Get a user by Id, then get hold of their buckets and also paginate the results.
    Generate previous and next pagination urls
    :param current_user: Current User
    :param page: Page number
    :return: Pagination next url, previous url and the user buckets.
    """
    user = User.get_by_id(current_user.id)
    pagination = user.buckets.paginate(page=page, per_page=app.config['BUCKET_AND_ITEMS_PER_PAGE'],
                                       error_out=False)
    previous = None
    if pagination.has_prev:
        previous = url_for('bucket.bucketlist', page=page - 1, _external=True)

    nex = None
    if pagination.has_next:
        nex = url_for('bucket.bucketlist', page=page + 1, _external=True)
    return nex, pagination, previous, pagination.items
