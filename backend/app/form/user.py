from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from app.model import User

class FormLogin(FlaskForm):
    user_name = StringField('Username', validators = [DataRequired(message='Username is required')])
    password = PasswordField('Password', validators = [DataRequired(message='Password is required')])
    remember = BooleanField('Remember me', default = False)
    submit = SubmitField('Login')
