from functools import wraps
from flask import Blueprint, url_for, redirect, render_template, request, flash
from flask_login import login_user, logout_user, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mongoengine import DoesNotExist

from .models.user_model import User
from .user_bp import user_bp, login_manager
from logging_setup.logger import ApiLogger

login_manager.login_view = 'user.login'


def user_login_info(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            return function(current_user, *args, **kwargs)

        if request.method == 'GET':
            return function({}, *args, **kwargs)

        email = request.form.get('email')
        password = request.form.get('password')
        remeber_me = True if request.form.get('remember') else False

        try:
            user = User.objects(email__iexact=email).get()
        except DoesNotExist:
            user = None

        return function(user, *args, **kwargs)
    return wrapper


@user_bp.route('/login', methods=['GET', 'POST'])
@user_login_info
def login(user):
    ApiLogger.log_debug("Login", "Login", "log ja in")
    if request.method == 'GET':
        return render_template('login.html', name='New User')

    # For POST
    if not user \
            or not check_password_hash(user.password, request.form.get('password')):
        flash('Invalid Credentials')
        return redirect(url_for('user.login'))

    login_user(user)

    return redirect(url_for('activity.get_posts_to_show'))


@user_bp.route('/signup', methods=['GET', 'POST'])
@user_login_info
def signup(user):
    if request.method == 'GET':
        return render_template('signup.html')

    # POST
    if user:
        flash('Email already registered')
        return redirect(url_for('user.signup'))

    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('name')

    new_user = User(email=email,
                    first_name=name,
                    password=generate_password_hash(password, method='sha256'))
    new_user.save()

    return redirect(url_for('user.login'))


@user_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user.login'))


@login_manager.user_loader
def load_user(user_id):
    return User.objects.get(id=user_id)
