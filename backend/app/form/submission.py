from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField
from wtforms.validators import DataRequired


class FormRejudge(FlaskForm):
	sid = IntegerField('Submission ID')
	pid = IntegerField('Problem ID')
	task_id = IntegerField('Task ID')
	rejudge_type = StringField('Rejudge Type')
	rejudge_confirm = StringField('Confirm')
