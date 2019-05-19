from app.extension import db
from datetime import datetime
from flask import json
from flask_login import current_user

class Submission(db.Model):
	__tablename__ = 'submission'

	sid = db.Column(db.Integer(), primary_key = True, autoincrement = True)
	pid = db.Column(db.Integer(), db.ForeignKey('problem.pid'))
	uid = db.Column(db.Integer(), db.ForeignKey('user.uid'))
	testset_id = db.Column(db.Integer, db.ForeignKey('testset.testset_id'))
	task_id = db.Column(db.Integer, db.ForeignKey('task.task_id'))
	result = db.Column(db.Text, nullable = True)
	score = db.Column(db.DECIMAL(6,2), nullable = True)
	code = db.Column(db.Text, nullable = False)
	is_solution = db.Column(db.Boolean(), default = False, nullable = False)
	date_time = db.Column(db.DateTime(), nullable = False, default = datetime.now)

	problem = db.relationship('Problem', backref = db.backref('submissions', lazy = 'dynamic'))
	user = db.relationship('User', backref = db.backref('submissions', lazy = 'dynamic'))
	task = db.relationship('Task', backref = db.backref('submissions', lazy = 'dynamic'))

	@property
	def full_score(self):
		return self.testset.full_score if self.testset else None

	@property
	def status(self):
		if (not current_user.is_teacher) and self.task and self.task.deadline > datetime.now():
			return 'hidden'
		if self.result is None:
			return 'pending'
		if self.result == 'running':
			return 'running'
		if self.result == 'system_error':
			return 'system_error'
		if self.full_score == self.score:
			return 'accepted'
		if self.full_score > self.score:
			return 'wrong_answer'
		return 'other'
