from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import login_required

from api.socialmedia.Users.user_auth import user_login_info
from api.socialmedia.Users.models.user_model import User
from api.socialmedia.Followers.models.follower_model import Followers

search_bp = Blueprint(
    "search",
    __name__,
    url_prefix='/search',
    template_folder='templates'
)


@search_bp.route('/', methods=['POST'])
@login_required
@user_login_info
def search(user):
    query_str = request.form.get('query_str')
    searched_users = User.objects(first_name__icontains=query_str)
    
    user_ids = [str(user.id) for user in searched_users]
    users_being_followed = Followers.objects(follower_id=str(user.id), user_id__in=user_ids)

    if users_being_followed:
        userids_being_followed = [str(user.user_id) for user in users_being_followed]
    else:
        userids_being_followed = None

    return render_template('search_users.html', user=user, searched_users=searched_users, userids_being_followed=userids_being_followed)