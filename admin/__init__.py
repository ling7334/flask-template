from flask import Blueprint

adminBlueprint = Blueprint('admin', __name__)

from .views import UserAPI
adminBlueprint.add_url_rule('/user', view_func=UserAPI.as_view('users'))