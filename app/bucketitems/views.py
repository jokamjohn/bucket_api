from flask import Blueprint, request, abort
from app.auth.helper import token_required
from app.bucketitems.helper import bucket_required, response, get_user_bucket, response_with_bucket_item, \
    response_with_pagination, get_paginated_items
from sqlalchemy import exc
from app.models import BucketItem

bucketitems = Blueprint('items', __name__)


@bucketitems.route('/bucketlists/<bucket_id>/items/', methods=['GET'])
@token_required
@bucket_required
def get_items(current_user, bucket_id):
    """
    A user`s items belonging to a Bucket specified by the bucket_id are returned if the Bucket Id
    is valid and belongs to the user.
    An empty item list is returned if the bucket has no items.
    :param current_user: User
    :param bucket_id: Bucket Id
    :return: List of Items
    """
    # Get the user Bucket
    bucket = get_user_bucket(current_user, bucket_id)
    if bucket is None:
        return response('failed', 'User has no Bucket with Id ' + bucket_id, 202)

    # Get items in the bucket
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', None, type=str)
    items, nex, pagination, previous = get_paginated_items(bucket, bucket_id, page, q)

    # Make a list of items
    if items:
        result = []
        for item in items:
            result.append(item.json())
        return response_with_pagination(result, previous, nex, pagination.total)
    return response_with_pagination([], previous, nex, 0)


@bucketitems.route('/bucketlists/<bucket_id>/items/<item_id>', methods=['GET'])
@token_required
@bucket_required
def get_item(current_user, bucket_id, item_id):
    """
    An item can be returned from the Bucket if the item and Bucket exist and below to the user.
    The Bucket and Item Ids must be valid.
    :param current_user: User
    :param bucket_id: Bucket Id
    :param item_id: Item Id
    :return:
    """
    # Check item id is an integer
    try:
        int(item_id)
    except ValueError:
        return response('failed', 'Provide a valid item Id', 202)

    # Get the user Bucket
    bucket = get_user_bucket(current_user, bucket_id)
    if bucket is None:
        return response('failed', 'User has no Bucket with Id ' + bucket_id, 202)

    # Delete the item from the bucket
    item = bucket.items.filter_by(id=item_id).first()
    if not item:
        abort(404)
    return response_with_bucket_item('success', item, 200)


@bucketitems.route('/bucketlists/<bucket_id>/items', methods=['POST'])
@token_required
@bucket_required
def post(current_user, bucket_id):
    """
    Storing an item into a Bucket
    :param current_user: User
    :param bucket_id: Bucket Id
    :return: Http Response
    """
    if not request.content_type == 'application/json':
        return response('failed', 'Content-type must be application/json', 401)

    data = request.get_json()
    item_name = data.get('name')
    if not item_name:
        return response('failed', 'No name or value attribute found', 401)

    # Get the user Bucket
    bucket = get_user_bucket(current_user, bucket_id)
    if bucket is None:
        return response('failed', 'User has no Bucket with Id ' + bucket_id, 202)

    # Save the Bucket Item into the Database
    item = BucketItem(item_name.lower(), data.get('description', None), bucket.id)
    item.save()
    return response_with_bucket_item('success', item, 200)


@bucketitems.route('/bucketlists/<bucket_id>/items/<item_id>', methods=['PUT'])
@token_required
@bucket_required
def edit_item(current_user, bucket_id, item_id):
    """
    Edit an item with a valid Id. The request content-type must be json and also the Bucket
    in which the item belongs must be among the user`s Buckets.
    The name of the item must be present in the payload but the description is optional.
    :param current_user: User
    :param bucket_id: Bucket Id
    :param item_id: Item Id
    :return: Response of Edit Item
    """
    if not request.content_type == 'application/json':
        return response('failed', 'Content-type must be application/json', 401)

    try:
        int(item_id)
    except ValueError:
        return response('failed', 'Provide a valid item Id', 202)

    # Get the user Bucket
    bucket = get_user_bucket(current_user, bucket_id)
    if bucket is None:
        return response('failed', 'User has no Bucket with Id ' + bucket_id, 202)

    # Get the item
    item = bucket.items.filter_by(id=item_id).first()
    if not item:
        abort(404)

    # Check for Json data
    request_json_data = request.get_json()
    item_new_name = request_json_data.get('name')
    item_new_description = request_json_data.get('description', None)

    if not request_json_data:
        return response('failed', 'No attributes specified in the request', 401)

    if not item_new_name:
        return response('failed', 'No name or value attribute found', 401)

    # Update the item record
    item.update(item_new_name, item_new_description)
    return response_with_bucket_item('success', item, 200)


@bucketitems.route('/bucketlists/<bucket_id>/items/<item_id>', methods=['DELETE'])
@token_required
@bucket_required
def delete(current_user, bucket_id, item_id):
    """
    Delete an item from the user's Bucket.
    :param current_user: User
    :param bucket_id: Bucket Id
    :param item_id: Item Id
    :return: Http Response
    """
    # Check item id is an integer
    try:
        int(item_id)
    except ValueError:
        return response('failed', 'Provide a valid item Id', 202)

    # Get the user Bucket
    bucket = get_user_bucket(current_user, bucket_id)
    if bucket is None:
        return response('failed', 'User has no Bucket with Id ' + bucket_id, 202)

    # Delete the item from the bucket
    item = bucket.items.filter_by(id=item_id).first()
    if not item:
        abort(404)
    item.delete()
    return response('success', 'Successfully deleted the item from bucket with Id ' + bucket_id, 200)


@bucketitems.errorhandler(404)
def item_not_found(e):
    """
    Custom response to 404 errors.
    :param e:
    :return:
    """
    return response('failed', 'Item not found', 404)


@bucketitems.errorhandler(400)
def bad_method(e):
    """
    Custom response to 400 errors.
    :param e:
    :return:
    """
    return response('failed', 'Bad request', 400)
