from flask import Blueprint
from flask.views import MethodView

auth = Blueprint('auth', __name__)


class RegisterUser(MethodView):
    pass
