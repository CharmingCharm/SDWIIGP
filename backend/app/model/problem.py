from app.extension import db
from flask_login import UserMixin

class Problem(UserMixin, db.Model):
    __tablename__ = 'problem'

    pid = db.Column(db.Integer(), primary_key = True, autoincrement = True)
    testset_id = db.Column(db.Integer, db.ForeignKey('testset.testset_id'))
    level = db.Column(db.Integer, nullable = False)
    title = db.Column(db.String(64), nullable = False)
    description = db.Column(db.Text(), nullable = False)

    testset = db.relationship('TestSet', backref = 'problem')
