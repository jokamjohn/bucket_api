from flask import Blueprint, request, abort
from app.auth.helper import token_required
from app.bucketitems.helper import bucket_required, response, get_user_bucket, response_with_bucket_item, \
    response_with_bucket_items
from sqlalchemy import exc
from app.models import BucketItem

bucketitems = Blueprint('items', __name__)


@bucketitems.route('/bucketlists/<bucket_id>/items', methods=['GET'])
@token_required
@bucket_required
def get_items(current_user, bucket_id):
    # Get the user Bucket
    try:
        bucket = get_user_bucket(current_user, bucket_id)
    except exc.DatabaseError:
        return response('failed', 'Operation failed, try again', 202)

    if bucket is None:
        return response('failed', 'User has no Bucket with Id ' + bucket_id, 202)

    # Get items in the bucket
    try:
        items = bucket.items.limit(10).all()
    except exc.DatabaseError:
        return response('failed', 'Operation failed, try again', 202)

    if items:
        # Make a list of items
        result = []
        for item in items:
            result.append(item.json())
        return response_with_bucket_items('success', result, 200)
    return response_with_bucket_items('success', [], 200)


@bucketitems.route('/bucketlists/<bucket_id>/items/<item_id>', methods=['GET'])
@token_required
@bucket_required
def get_item(current_user, bucket_id, item_id):
    # Check item id is an integer
    try:
        int(item_id)
    except ValueError:
        return response('failed', 'Provide a valid item Id', 202)

    # Get the user Bucket
    try:
        bucket = get_user_bucket(current_user, bucket_id)
    except exc.DatabaseError:
        return response('failed', 'Operation failed, try again', 202)

    if bucket is None:
        return response('failed', 'User has no Bucket with Id ' + bucket_id, 202)

    # Delete the item from the bucket
    try:
        item = bucket.items.filter_by(id=item_id).first()
        if not item:
            abort(404)
    except exc.DatabaseError:
        return response('failed', 'Operation failed, try again', 202)
    return response_with_bucket_item('success', item, 200)


@bucketitems.route('/bucketlists/<bucket_id>/items', methods=['POST'])
@token_required
@bucket_required
def post(current_user, bucket_id):
    """
    Storing an item into a Bucket
    :param current_user: User
    :param bucket_id: Bucket Id
    :return:
    """
    if not request.content_type == 'application/json':
        return response('failed', 'Content-type must be application/json', 401)

    data = request.get_json()
    item_name = data.get('name')
    if not item_name:
        return response('failed', 'No name or value attribute found', 401)

    # Get the user Bucket
    try:
        bucket = get_user_bucket(current_user, bucket_id)
    except exc.DatabaseError:
        return response('failed', 'Operation failed, try again', 202)

    if bucket is None:
        return response('failed', 'User has no Bucket with Id ' + bucket_id, 202)

    # Save the Bucket Item into the Database
    item = BucketItem(item_name, data.get('description', None), bucket.id)
    try:
        item.save()
    except exc.DatabaseError:
        return response('failed', 'Operation failed, try again', 202)
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
    :return:
    """
    # Check item id is an integer
    try:
        int(item_id)
    except ValueError:
        return response('failed', 'Provide a valid item Id', 202)

    # Get the user Bucket
    try:
        bucket = get_user_bucket(current_user, bucket_id)
    except exc.DatabaseError:
        return response('failed', 'Operation failed, try again', 202)

    if bucket is None:
        return response('failed', 'User has no Bucket with Id ' + bucket_id, 202)

    # Delete the item from the bucket
    try:
        item = bucket.items.filter_by(id=item_id).first()
        if not item:
            abort(404)
        item.delete()
    except exc.DatabaseError:
        return response('failed', 'Operation failed, try again', 202)
    return response('success', 'Successfully deleted the item from bucket with Id ' + bucket_id, 200)


@bucketitems.errorhandler(404)
def item_not_found(e):
    """
    Custom response to 404 errors.
    :param e:
    :return:
    """
    return response('failed', 'Item not found', 404)
