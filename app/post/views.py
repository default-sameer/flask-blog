from app import fa, db, moment
from datetime import datetime, timedelta
from app.post import post
from flask import render_template, flash, redirect, url_for, request, abort, session, current_app
from app.post.forms import Create_Post
from app.models import User, Post
from flask_login import login_required, current_user, login_user
from app.momentjs import momentjs
from flask_moment import Moment
from app.utils import is_author


@post.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)


@post.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    return render_template('post/blog.html', title='Blog', posts=posts.items)

@post.route('/blog/posts')
def all_post():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=5)
    return render_template('post/pages/all_post.html', title='Posts', posts=posts)

@post.route('/blog/<username>')
def user_post(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.timestamp.desc()).paginate(page=page, per_page=5)
    return render_template('post/pages/user_post.html', title='Posts', posts=posts, user=user)


@post.route('/blog/<username>/create_post', methods=['GET', 'POST'])
@login_required
@is_author
def create_post(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = Create_Post()
    if form.validate_on_submit():
        post = Post(head=form.head.data, sub_head=form.sub_head.data, body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post Create Sucessfully', 'success')
        return redirect(url_for('post.all_post'))
    return render_template('post/create_post.html', username=username, title='Create Post', form=form)


@post.route('/blog/update_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
@is_author
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = Create_Post()
    if form.validate_on_submit():
        post.head = form.head.data
        post.sub_head = form.sub_head.data
        post.body = form.body.data
        db.session.commit()
        flash('Post Updated', 'success')
        return redirect(url_for('post.user_post', username=post.author.username))
    elif request.method == 'GET':
        form.head.data = post.head
        form.sub_head.data = post.sub_head
        form.body.data = post.body
    return render_template('post/update_post.html', title='Update Post', form=form)


@post.route('/blog/delete_post/<int:post_id>', methods=['POST'])
@login_required
@is_author
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post Deleted', 'danger')
    return redirect(url_for('post.all_post'))


@post.route('/blog/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post/pages/post.html', title='All Post', post=post)
