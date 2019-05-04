from app.extension import db
from flask_login import UserMixin
from datetime import datetime

class Submission(UserMixin, db.Model):
    __tablename__ = 'submission'

    sid = db.Column(db.Integer(), primary_key = True, autoincrement = True)
    pid = db.Column(db.Integer(), db.ForeignKey('problem.pid'))
    uid = db.Column(db.Integer(), db.ForeignKey('user.uid'))
    score = db.Column(db.DECIMAL(6,2), nullable = True)
    code = db.Column(db.Text(), nullable = False)
    is_solution = db.Column(db.Boolean(), default = False, nullable = False)
    date_time = db.Column(db.DateTime(), nullable = False, default = datetime.now)

    problem = db.relationship('Problem', backref = db.backref('submissions', lazy = 'dynamic'))
    user = db.relationship('User', backref = db.backref('submissions', lazy = 'dynamic'))
