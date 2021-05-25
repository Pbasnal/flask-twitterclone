from flask import Blueprint, request, redirect, render_template, jsonify, abort, url_for
from flask_mongoengine.wtf import model_form
from flask_login import login_required

from .models.follower_model import Followers
from api.socialmedia.Users.user_auth import user_login_info
from api.socialmedia.Users.models.user_model import User

followers_bp = Blueprint(
    "followers",
    __name__,
    url_prefix='/followers',
    template_folder='templates'
)

@followers_bp.route('/<userid_to_follow>', methods=['POST'])
@login_required
@user_login_info
def follow(user: User, userid_to_follow):
    if not userid_to_follow:
        return abort(400, "Provide a user id which you want to follow")

    user_to_follow = User.objects.get(id=userid_to_follow)

    if not user_to_follow:
        return abort(400, "Provided user doesn't exists")
    
    follower = Followers()
    follower.user_id = userid_to_follow
    follower.follower_id = str(user.id)
    follower.engagement_index = 0.5

    follower.save()

    return redirect(url_for('activity.get_posts_to_show'))

@followers_bp.route('/unfollow/<userid_to_unfollow>', methods=['POST'])
@login_required
@user_login_info
def unfollow(user: User, userid_to_unfollow):
    follower = Followers.objects.get({
        'user_id': userid_to_unfollow,
        'follower_id': user.id
    })
    if not follower:
        return abort(400, "You don't follow the provided user")

    follower.remove()
    return redirect(url_for('activity.get_posts_to_show'))