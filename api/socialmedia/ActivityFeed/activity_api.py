from flask import Blueprint, request, redirect, render_template, jsonify, abort, url_for
from flask_mongoengine import Pagination
from flask_mongoengine.wtf import model_form
from flask_login import login_required

from api.socialmedia.Users.user_auth import user_login_info
from api.socialmedia.Users.models.user_model import User
from api.socialmedia.Followers.models.follower_model import Followers
from api.socialmedia.Posts.models.post_model import Post

activity_bp = Blueprint(
    "activity",
    __name__,
    template_folder='templates'
)

PostForm = model_form(Post)


@activity_bp.route('/')
@login_required
@user_login_info
def get_posts_to_show(user: User):
    form = PostForm(request.form)

    following_list = Followers.objects(follower_id=str(user.id)).order_by('engagement_index')

    if len(following_list) == 0:
        return render_template('activity_home.html',
                               paginated_posts=following_list,
                               form=form,
                               user=user)

    users_ids = [str(following.user_id) for following in following_list]
    users_ids.insert(len(users_ids), str(user.id))
    posts_from_following = Post.objects(created_by__in=users_ids).order_by('-created_at')
    following_users = User.objects(id__in=users_ids)

    userid_userinfo_map = dict()
    for following_user in following_users:
        userid_userinfo_map[str(following_user.id)] = following_user

    page = int(request.args['page'] if 'page' in request.args else 1)
    paginator = Pagination(posts_from_following, page, 10)

    return render_template('activity_home.html',
                           paginated_posts=paginator,
                           userid_userinfo_map=userid_userinfo_map,
                           form=form,
                           user=user)
