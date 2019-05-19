from app.extension import db
from .submission import Submission
from flask_login import current_user

class Problem(db.Model):
	__tablename__ = 'problem'

	pid = db.Column(db.Integer(), primary_key = True, autoincrement = True)
	testset_id = db.Column(db.Integer, db.ForeignKey('testset.testset_id'))
	level = db.Column(db.Integer, nullable = False)
	title = db.Column(db.String(64), nullable = False)
	description = db.Column(db.Text(), nullable = False)
	visible = db.Column(db.Boolean, nullable = False, server_default = "1")

	testset = db.relationship('TestSet', backref = 'problem')

	def get_user_sub(self):
		return self.submissions.filter_by(uid = current_user.uid).order_by(Submission.score.desc()).first()

	@property
	def ac_rate(self):
		total = self.submissions.count()
		ac = self.submissions.filter(Submission.score == Submission.full_score).count()
		return '%.2f%%' % (ac / total)
