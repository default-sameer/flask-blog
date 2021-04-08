from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message='Password Too Short')],render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],render_kw={"placeholder": "Username"})
    email = StringField('Email', validators=[DataRequired(), Email()],render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message='Password Too Short')],render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, message='Password Too Short'), EqualTo('password')],render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid !')],render_kw={"placeholder": "Email"})
    submit = SubmitField('Reset')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Email Doesnot Exists')
        
class ResetPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message='Password Too Short')],render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, message='Password Too Short'), EqualTo('password', message='Password Donot Match')],render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Reset Password')
