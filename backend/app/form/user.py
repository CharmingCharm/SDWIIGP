from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, FormField, FieldList, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from app.model import User

class FormLogin(FlaskForm):
    user_name = StringField('Username', validators = [DataRequired(message='Username is required')])
    password = PasswordField('Password', validators = [DataRequired(message='Password is required')])
    remember = BooleanField('Remember me', default = False)
    submit = SubmitField('Login')

class FormProfile(FlaskForm):
    # uid = IntegerField('User ID', render_kw = {'disabled':''})
    # user_name = StringField('Username', render_kw = {'disabled':''})
    # position = StringField('User\'s Position', render_kw = {'disabled':''})
    # position = SelectField('User\'s Position', choices = [("Teacher", "Teacher"), ("Student", "Student")], render_kw = {'disabled':''})
    password = PasswordField('New Password')
    check_password = PasswordField('Confirm New Password')
    old_password = PasswordField('Old Password')
    submit = SubmitField('Update Profile')

class FormUserSingle(FlaskForm):
    uid = StringField('User ID', render_kw = {'readonly':'expression(this.readOnly=false)'})
    user_name = StringField('Username')
    position = SelectField('User\'s position', choices = [("Teacher", "Teacher"), ("Student", "Student")])
    changeID = SubmitField()

class FormUsers(FlaskForm):
    users = FieldList(FormField(FormUserSingle))
