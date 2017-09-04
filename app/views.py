from app import app
from app.bucketitems.helper import response


@app.errorhandler(404)
def route_not_found(e):
    """
    Return a custom 404 Http response message for missing or not found routes.
    :param e: Exception
    :return: Http Response
    """
    return response('failed', 'Endpoint not found', 404)
