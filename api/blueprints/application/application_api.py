import json
import uuid
from functools import wraps
from datetime import datetime, timedelta
from flask import Blueprint, request, redirect, render_template, jsonify, abort
from flask_mongoengine.wtf import model_form
from wtforms import Form, BooleanField, StringField, PasswordField, validators

from .models.application import Application
from helpers.passwords.password_generator import password_generator
from logging_setup.logger import ApiLogger

application_bp = Blueprint(
    "application",
    __name__,
    url_prefix='/application',
    template_folder='templates/application'
)

class ApplicationForm(Form): #= model_form(Application)
    ApplicationName = StringField('Application Name', [validators.Length(min=4, max=50)])

def get_argument_from_form_or_json(request, arg):

    value = ""
    if arg in request.form:
        value = request.form[arg]
    elif arg in request.json:
        value = request.json[arg]
    
    if value.strip() == "":
        abort(400, f"Proper arguments not provided: {arg}")
        return

def app_secret_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        ApiLogger.log_debug("CHECKING_APP_SECRET", "REQUEST", f"request: {request}")
        
        if "application_id" not in kwargs \
            or kwargs.get("application_id").strip() == "":
            abort(400, "Provide AppId in URL and secret in the body or form")
        
        appid = kwargs.get("application_id")        
        secret = get_argument_from_form_or_json('secret')
        app_details = Application.get(appid)

        if app_details.application_secret != secret:
            abort(400, "Provide AppId and secret combinations do not match")

        return function(app_details, *args, **kwargs)
    return wrapper


def app_token_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        ApiLogger.log_debug("CHECKING_APP_TOKEN", "TOKEN", f"request: {request}")
        
        if "application_id" not in kwargs \
            or kwargs.get("application_id").strip() == "":
            abort(400, "Provide AppId in URL and secret in the body or form")
        
        appid = kwargs.get("application_id")
        token = get_argument_from_form_or_json('token')
        app_details = Application.get_application_for_token(token)
        
        if app_details.token_expiration < datetime.utcnow():
            abort("Token has expired")

        return function(app_details, *args, **kwargs)
    return wrapper


@application_bp.route('/<application_id>', methods=['GET'])
def home(application_id):
    app_details = Application.get(application_id)
    if app_details == None:
        return "Requested application doesn't exists"
    
    return jsonify(app_details)

@app_secret_required
@application_bp.route('/<application_id>/token', methods=['POST'])
def get_token(application_id):

    app_details = Application.get(application_id)
    if app_details == None:
        return "Requested application doesn't exists"
    
    if app_details.application_token == None \
        or app_details.token_expiration == None \
        or app_details.token_expiration < datetime.utcnow():
        
        app_details.application_token = str(uuid.uuid1())
        app_details.token_expiration = datetime.utcnow() + timedelta(days=1)
        app_details = Application.update_token(app_details)

    app_details.application_secret = ""
    return jsonify(app_details)

@application_bp.route('/register', methods=['GET', 'POST'])
def register():
    FLOW_ID = "REGISTERING_NEW_APPLICATION"

    ApiLogger.log_debug(FLOW_ID, "INSERTING_NEW_APPLICATION", 
        f"{{ \
            request_method: {request.method}, \
            message: \"Registering new application.\", \
            form_data: {json.dumps(request.form)} \
        }}")

    form = ApplicationForm(request.form)
    if request.method == 'GET':
        ApiLogger.log_debug(FLOW_ID, 
            "INSERTING_NEW_APPLICATION", 
            "Returning registration form")
            
        return render_template('add_application.html', form=form)
        
    if not form.validate():
        ApiLogger.log_debug(FLOW_ID, 
            "INSERTING_NEW_APPLICATION", 
            f"Form validation failed. Returning registration form \
            - Errors: {json.dumps(form.errors)}")
        
        return render_template('add_application.html', form=form)

    added_new_application = False
    application_secret = password_generator()
    while added_new_application == False:
        application_id = str(uuid.uuid1())

        # do something
        ApiLogger.log_debug(FLOW_ID, "INSERTING_NEW_APPLICATION", f"{{ \
                request_data: {form}, \
                application_name: {form.ApplicationName.data}, \
                application_id: {application_id}, \
                application_secret: {application_secret} \
            }}")
        
        added_new_application = Application.add_new_application(
            form.ApplicationName.data,
            application_id,
            application_secret)

    return redirect(f"/application/{application_id}")




@application_bp.route("/<application_id>/test", methods=['POST'])
@app_token_required
#@app_secret_required
def test_application(application, application_id):
    return "test application"



