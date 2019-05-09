from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from app.model import User

class FormProfile(FlaskForm):
    uid = IntegerField('user id', validators = [DataRequired(message = 'no empty uid')])
    user_name = StringField('new username', validators = [DataRequired(message = 'no empty username')])
    password = PasswordField('new password')
    checkPassword = PasswordField('double check the new password')
    oldPassword = PasswordField('check the old password')
    submit = SubmitField('update profile')
