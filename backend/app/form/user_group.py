from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, TextAreaField, FieldList, FormField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from app.model import User

class FormUserGroup(FlaskForm):
    gid = IntegerField('Username', render_kw = {'readonly':'expression(this.readOnly=false)'})
    group_name = StringField('Group name')
    number = IntegerField('Number of members')
    description = TextAreaField('Decription', render_kw = {'rows': 6})

class FormGroupList(FlaskForm):
    groups = FieldList(FormField(FormUserGroup))
