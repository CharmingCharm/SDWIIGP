from app.extension import db
from flask_login import UserMixin

class Problem(UserMixin, db.Model):
    __tablename__ = 'problem'

    pid = db.Column(db.Integer(), primary_key = True, autoincrement = True)
    # testset_id = db.Column(db.Integer(), db.ForeignKey('test_set.testset_id'))
    level = db.Column(db.DECIMAL(6,2), nullable = False)
    title = db.Column(db.String(64), nullable = False)
    description = db.Column(db.Text(), nullable = False)
