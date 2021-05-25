from flask_mongoengine.wtf import model_form
from flask_login import UserMixin
from api.models.MongoEngine import dbcontext
from logging_setup.logger import ApiLogger

class User(dbcontext.Document, UserMixin):
    email = dbcontext.StringField(required=True)
    first_name = dbcontext.StringField(max_length=50)
    last_name = dbcontext.StringField(max_length=50)
    profile_picture_path = dbcontext.StringField(max_length=100)

    password = dbcontext.StringField(max_length=255)
