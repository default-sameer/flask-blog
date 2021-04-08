from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_ckeditor import CKEditorField

class Create_Post(FlaskForm):
    head = StringField('Head', validators=[DataRequired(), Length(min=10, message="Head Too Short")])
    sub_head = StringField('Sub Heading', validators=[DataRequired(), Length(min=10, message="Too Short")])
    body = CKEditorField('Body', validators=[DataRequired(), Length(min=10, message="Body Too Short")])
    submit = SubmitField('Post')
    submit_1 = SubmitField('Update')
