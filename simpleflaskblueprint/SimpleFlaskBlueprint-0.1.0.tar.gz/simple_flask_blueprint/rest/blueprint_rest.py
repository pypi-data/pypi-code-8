from flask import Blueprint
from simple_flask_blueprint.core.blueprint_core import say_hallo


bp = Blueprint('simple_flask_blueprint', __name__)


@bp.route('/')
def say_hallo_service():
    return say_hallo()

@bp.route('/<name>/')
def say_hallo_to_guest_service(name):
    return say_hallo(name)
