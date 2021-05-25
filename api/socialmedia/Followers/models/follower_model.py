from flask_mongoengine.wtf import model_form
from flask_login import UserMixin
from api.models.MongoEngine import dbcontext
from logging_setup.logger import ApiLogger

class Followers(dbcontext.Document, UserMixin):
    user_id = dbcontext.StringField(required=True)
    follower_id = dbcontext.StringField(required=True)
    engagement_index = dbcontext.DecimalField(required=True)

