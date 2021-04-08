from app import fa, db, login
from datetime import datetime
from app.admin import admin
from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import current_user, login_required
from app.admin.forms import RegisterForm, UserForm
from app.models import User, Post 
from app.utils import is_admin

@admin.route('/')
@login_required
@is_admin
def index():
    return render_template('admin/index.html')

@admin.route('/setting')
@login_required
@is_admin
def setting():
    return render_template('admin/setting.html')

@admin.route('/setting/register_user', methods=['GET', 'POST'])
@login_required
@is_admin
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, author=form.author.data, admin=form.admin.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User Created Sucessfully')
        return redirect(url_for('admin.users'))
    return render_template('admin/register.html',title='Register', form=form)

@admin.route('/setting/delete_user/<username>', methods=['POST'])
@login_required
@is_admin
def delete_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    db.session.delete(user)
    db.session.commit()
    flash('User Wiped Sucessfully', 'success')
    return redirect(url_for('admin.users'))

@admin.route('/setting/<username>', methods=['GET', 'POST'])
@login_required
@is_admin
def user_settings(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = UserForm()
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.author = form.author.data
        user.admin = form.admin.data
        db.session.commit()
        flash('User Settings Updated', 'success')
        return redirect(url_for('admin.users'))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.author.data = user.author
        form.admin.data = user.admin
    return render_template('admin/user_setting.html', form=form, user=user)

@admin.route('/users')
@login_required
@is_admin
def users():
    user = User.query.all()
    return render_template('admin/users.html', user=user, title='All Users')
