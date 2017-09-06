from flask import make_response, jsonify


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
