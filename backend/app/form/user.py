from flask_login import current_user
from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, FormField, FieldList, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.extension import photos

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
    item_per_page = IntegerField('Items per page')
    password = PasswordField('New Password')
    check_password = PasswordField('Confirm New Password')
    old_password = PasswordField('Old Password')
    submit = SubmitField('Update Profile')

class FormUserSingle(FlaskForm):
    uid = StringField('User ID', render_kw = {'readonly':'expression(this.readOnly=false)'})
    user_name = StringField('Username')
    position = SelectField('User\'s position', choices = [("Teacher", "Teacher"), ("Student", "Student")])
    changeID = SubmitField()
    deleteID = SubmitField()

class FormUsers(FlaskForm):
    users = FieldList(FormField(FormUserSingle))
    new_user_name = StringField('Username', render_kw = {'value':'new user'})
    new_position = SelectField('User\'s position', choices = [("Teacher", "Teacher"), ("Student", "Student")], render_kw = {'value':'Teacher'})
    addID = SubmitField()

class FormIcon(FlaskForm):
    avatar = FileField('Avatar', validators=[FileRequired(), FileAllowed(photos, message='You are only allowed to upload images!')])
    submit = SubmitField('submit')
