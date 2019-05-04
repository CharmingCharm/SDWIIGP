from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from app.model import User

class FormLogin(FlaskForm):
    userName = StringField('用户名', validators = [DataRequired(message = '用户名不能为空')])
    password = PasswordField('密码', validators = [DataRequired(message = '密码不能为空')])
    remember = BooleanField('记住我', default = False)
    submit = SubmitField('登录')
