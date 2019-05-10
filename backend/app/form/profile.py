from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from app.model import User

class FormProfile(FlaskForm):
    uid = IntegerField('User ID', render_kw = {'disabled':''})
    user_name = StringField('Username', render_kw = {'disabled':''})
    position = StringField('User\'s position', render_kw = {'disabled':''})
    # position = SelectField('User\'s position', choices = [("Teacher", "Teacher"), ("Student", "Student")], render_kw = {'disabled':''})
    password = PasswordField('New Password')
    check_password = PasswordField('Double check the new password')
    old_password = PasswordField('Check the old password')
    submit = SubmitField('Update Profile')
