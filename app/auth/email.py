from flask import render_template, current_app
from app.emails import send_email

def send_password_reset_email(user):
    token = user.get_password_reset_token()
    send_email('[Reset Your Password]',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template(
                   'email/verify_email.txt', user=user, token=token),
               html_body=render_template('email/verify_email.html', user=user, token=token))

