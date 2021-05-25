from datetime import datetime
from flask_mongoengine import Pagination
from flask_mongoengine.wtf import model_form
from flask_login import login_required, current_user
from flask import Blueprint, request, redirect, render_template, jsonify, abort, url_for

from .models.post_model import Post

from api.socialmedia.Users.user_auth import user_login_info
from api.blueprints.sentiment.sentiment_handlers import add_new_sentiment as sh

posts_bp = Blueprint(
    "posts", __name__,
    url_prefix='/posts',
    template_folder='templates'
)

PostForm = model_form(Post)

@posts_bp.route('/')
@login_required
@user_login_info
def home(user):
    page = int(request.args['page'] if 'page' in request.args else 1)

    posts_created_by_user = Post.objects(created_by=str(user.id)).order_by('-created_at')
    paginator = Pagination(posts_created_by_user, page, 10)
    form = PostForm(request.form)
    return render_template('post_home.html',
                           paginated_posts=paginator,
                           form=form,
                           user=user)


@posts_bp.route('/create', methods=['GET', 'POST'])
@login_required
@user_login_info
def add_post(user):
    form = PostForm(request.form)
    if request.method == 'GET':
        return redirect(url_for("activity.get_posts_to_show"))

    if not form.validate():
        return redirect(url_for("activity.get_posts_to_show"))

    input = dict()
    input["content"] = form.content.data
    sentiment = sh.get_sentiments_of_content(input, "Some flow")

    new_post = Post(
        content=form.content.data,
        created_by=str(user.id),
        sentiments=sentiment,
        created_at=datetime.utcnow())

    new_post.save()

    return redirect(url_for('activity.get_posts_to_show'))


@posts_bp.route('/delete/<tweetid>', methods=['GET'])
@login_required
@user_login_info
def delete_post(user, tweetid):
    post = Post.objects.get(id=tweetid)
    
    if post and post.created_by == str(user.id):
        post.delete()

    return redirect(request.path)
