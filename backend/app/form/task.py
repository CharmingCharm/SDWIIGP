from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateTimeField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from flask import request
from app.model import Problem, Task, UserGroup


class FormTask(FlaskForm):
	def problem_query():
		return Problem.query.all()

	def group_query():
		return UserGroup.query.all()
	
	task_name = StringField('Task name', validators=[DataRequired(message='Title is required')])
	description = TextAreaField('Description', validators=[DataRequired(message='Description is required')])
	deadline = DateTimeField(
		'Deadline',
		validators=[DataRequired(message='Deadline is required')],
		render_kw = {'data-date-format': 'YYYY-MM-DD HH:mm:ss'}
	)
	problems = QuerySelectMultipleField('Problem set', query_factory=problem_query)
	groups = QuerySelectMultipleField('Related groups', query_factory=group_query)
	submit = SubmitField('Save')

	def __init__(self, task_id, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if request.method == 'GET' and task_id :
			task = Task.query.filter_by(task_id = task_id).first()
			self.task_name.data = task.task_name
			self.description.data = task.description
			self.deadline.data = task.deadline
			self.problems.data = task.problems.all()
			self.groups.data = task.groups.all()
