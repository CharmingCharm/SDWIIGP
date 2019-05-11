from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from app.model import User

class FormGroupList(FlaskForm):
    gid = IntegerField('Username')

class FormUserGroup(FlaskForm):
    group_name = StringField('Group name')
    description = TextAreaField('Decription', render_kw = {'rows': 6})
