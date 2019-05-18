from app.extension import db
from datetime import datetime

class Submission(db.Model):
    __tablename__ = 'submission'

    sid = db.Column(db.Integer(), primary_key = True, autoincrement = True)
    pid = db.Column(db.Integer(), db.ForeignKey('problem.pid'))
    uid = db.Column(db.Integer(), db.ForeignKey('user.uid'))
    testset_id = db.Column(db.Integer, db.ForeignKey('testset.testset_id'))
    score = db.Column(db.Text, nullable = True)
    code = db.Column(db.Text, nullable = False)
    is_solution = db.Column(db.Boolean(), default = False, nullable = False)
    date_time = db.Column(db.DateTime(), nullable = False, default = datetime.now)

    problem = db.relationship('Problem', backref = db.backref('submissions', lazy = 'dynamic'))
    user = db.relationship('User', backref = db.backref('submissions', lazy = 'dynamic'))
