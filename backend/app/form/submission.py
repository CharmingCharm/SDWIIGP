from flask_login import current_user
from flask_wtf import FlaskForm
from flask import request
from wtforms import IntegerField, SelectField, StringField
from wtforms.validators import DataRequired


class FormRejudge(FlaskForm):
	sid = IntegerField('Submission ID')
	pid = IntegerField('Problem ID')
	task_id = IntegerField('Task ID')
	rejudge_type = StringField('Rejudge Type')
	rejudge_confirm = StringField('Confirm')

class FormSubmissionFilter(FlaskForm):
	pid = IntegerField('Problem ID')
	uid = StringField('User ID')
	page = StringField('page')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.pid.data = request.values.get('pid')
		self.uid.data = request.values.get('uid')
		self.page.data = request.values.get('page') or 1

	@property
	def collapsed(self):
		return (not self.pid.data) and (not self.uid.data)
