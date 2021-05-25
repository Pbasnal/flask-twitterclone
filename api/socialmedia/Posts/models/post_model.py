from flask_mongoengine.wtf import model_form
from api.models.MongoEngine import dbcontext
from logging_setup.logger import ApiLogger

class Post(dbcontext.Document):
    content = dbcontext.StringField(required=True)
    sentiments = dbcontext.DictField()

    created_by = dbcontext.StringField(max_length=50)
    created_at = dbcontext.DateTimeField()