from app.extension import db
from datetime import datetime

class Task(db.Model):
	__tablename__ = 'task'

	task_id = db.Column(db.Integer(), primary_key = True, autoincrement = True)
	task_name = db.Column(db.String(64), nullable = False)
	description = db.Column(db.Text, nullable = False, default = '')
	deadline = db.Column(db.DateTime(), nullable = False)

	problems = db.relationship(
		'Problem',
		secondary = 'problem_in_task',
		backref = db.backref('tasks', lazy = 'dynamic'),
		lazy = 'dynamic'
	)

	groups = db.relationship(
		'UserGroup',
		secondary = 'task_for_usergroup',
		backref = db.backref('tasks', lazy = 'dynamic'),
		lazy = 'dynamic'
	)
	
	@property
	def available(self):
		return self.deadline > datetime.now()
