import os

import api.config
from flask import Flask
from logging_setup.logger import ApiLogger
from loguru import logger

def load_config(app, test_config):
    if test_config == None:
        app.config.from_object(f"api.config.{app.config['ENV']}")
    else:
        app.config.from_mapping(test_config)

@logger.catch
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    load_config(app, test_config)

    ApiLogger(app.config["LOG_FILE"])
        
    setup_db(app)
    setup_blueprints(app)
    setup_socialmedia(app)
    return app

def setup_db(app: Flask):
    from api.models.MongoEngine import dbcontext
    
    dbcontext.init_app(app)

def setup_blueprints(app: Flask):
    from api.blueprints.sentiment.sentiment_api import sentiment_bp
    from api.blueprints.application.application_api import application_bp
    
    app.register_blueprint(sentiment_bp)
    app.register_blueprint(application_bp)

def setup_socialmedia(app: Flask):
    from api.socialmedia.Users.user_bp import user_bp, login_manager
    from api.socialmedia.Posts.post_api import posts_bp
    from api.socialmedia.Followers.followers_api import followers_bp
    from api.socialmedia.Search.search_api import search_bp
    from api.socialmedia.ActivityFeed.activity_api import activity_bp

    app.register_blueprint(user_bp)
    login_manager.init_app(app)

    app.register_blueprint(posts_bp)
    app.register_blueprint(followers_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(activity_bp)
    
    