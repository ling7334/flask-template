from flask import Blueprint

admin_blueprint = Blueprint('admin', __name__)

from .views import UserAPI
admin_blueprint.add_url_rule('/user', view_func=UserAPI.as_view('users'))