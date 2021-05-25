from flask import Blueprint
from flask_login import LoginManager

login_manager = LoginManager()

user_bp = Blueprint(
    "user",
    __name__,
    url_prefix='/user',
    template_folder='templates'
)


from .user_auth import *
from .user_api import *