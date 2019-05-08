from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, EqualTo, ValidationError

class FormProblem(FlaskForm):
    title = StringField('Title', validators = [DataRequired(message = '标题不能为空')])
    description = StringField('Description', validators = [DataRequired(message = '题目描述不能为空')])
    level = SelectField('Level', coerce = int, choices = [(k, k) for k in range(1, 4)])
    remember = BooleanField('记住我', default = False)
    submit = SubmitField('登录')
