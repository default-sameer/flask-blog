from app import fa, db
from app.auth import auth
from flask import render_template, flash, redirect, url_for, request, session
from app.auth.forms import LoginForm, RequestResetForm, ResetPassword
from app.models import User
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.urls import url_parse
from app.auth.email import send_password_reset_email


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password','danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('post.blog')
        return redirect(next_page)
    return render_template('auth/login.html', title='Login', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.index'))

@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_password_reset_email(user)
        flash('Email Sent with Instruction To Reset Password', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_request.html', title='Reset Password', form=form)

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    user = User.verify_password_reset_token(token)
    if user is None:
        flash('Token Invalid Or Expired', 'warning')
        return redirect(url_for('auth.reset_request'))
    form = ResetPassword()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been Updated.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_token.html', title='Reset Password', form=form)
