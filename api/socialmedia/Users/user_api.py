import os

from flask import Blueprint, request, redirect, render_template, jsonify, abort, url_for
from flask_login import login_required, logout_user
from flask_mongoengine.wtf import model_form
from werkzeug.security import check_password_hash, generate_password_hash

from .models.user_model import User
from .user_bp import user_bp, login_manager
from .user_auth import user_login_info

UserForm = model_form(User)

@user_bp.route('/profile')
@login_required
@user_login_info
def profile(user: User):
    return render_template('profile.html', user=user)

@user_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
@user_login_info
def profile_edit(user: User):
    form = UserForm(request.form)
    
    url = url_for('static', filename='avatars/' + str(user.id))


    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.save()

    return render_template('profile_edit_basic_info.html', 
            form=form,
            user=user)

@user_bp.route('/profile/upload_pic', methods=['GET', 'POST'])
@login_required
@user_login_info
def update_pic(user: User):
    uploaded_file = request.files['Profile Picture']

    if not uploaded_file.filename or uploaded_file.filename.strip() == "":
        return redirect(url_for('profile.profile_edit'))
    
    file_path = os.path.join('api/static/avatars', str(user.id))
    uploaded_file.save(file_path)

    user.profile_picture_path = file_path
    user.save()

    return redirect(url_for('user.profile'))

@user_bp.route('/profile/resetpwd', methods=['GET', 'POST'])
@login_required
@user_login_info
def reset_password(user: User):
    form = UserForm(request.form)

    if request.method == 'GET':
        return redirect(url_for('user.profile_edit'))

    if not check_password_hash(user.password, form.password.data):
        return redirect(url_for('user.profile_edit'))
    
    if request.form['new_password'].strip() == "":
        return redirect(url_for('user.profile_edit'))

    if request.form['new_password'] != request.form['confirm_password']:
        return redirect(url_for('user.profile_edit'))

    user.password = generate_password_hash(request.form['new_password'] , method='sha256')
    user.save()

    if request.form.get('logout') :
        logout_user()
    
    return redirect(url_for('user.profile_edit'))