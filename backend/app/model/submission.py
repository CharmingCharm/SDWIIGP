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
	code = db.Column(db.Text, nullable = False)
	is_solution = db.Column(db.Boolean(), default = False, nullable = False)
	date_time = db.Column(db.DateTime(), nullable = False, default = datetime.now)

	problem = db.relationship('Problem', backref = db.backref('submissions', lazy = 'dynamic'))
	user = db.relationship('User', backref = db.backref('submissions', lazy = 'dynamic'))
	task = db.relationship('Task', backref = db.backref('submissions', lazy = 'dynamic'))

	@property
	def score(self):
		if (not self.result) or (self.result == 'running'):
			return None
		result = json.loads(self.result)
		score = float(0)
		for test in result:
			score = score + test['score']
		return score

	@property
	def full_score(self):
		if not self.testset:
			return None
		score = float(0)
		for test in self.testset.tests.all():
			score = score + float(str(test.score))
		return score

	@property
	def status(self):
		if (not current_user.is_teacher) and self.task and self.task.deadline > datetime.now():
			return 'hidden'
		if self.score is None:
			return 'pending'
		if self.score == 'running':
			return 'running'
		full_score = self.full_score
		if full_score == self.score:
			return 'accepted'
		if full_score > self.score:
			return 'wrong_answer'
		return 'other'
