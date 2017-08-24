from flask import Blueprint
from flask.views import MethodView

bucketitems = Blueprint('items', __name__)


class GetPostItems(MethodView):
    pass
