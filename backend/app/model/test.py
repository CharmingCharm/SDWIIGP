from flask_login import UserMixin
from app.extension import db

class Test(UserMixin, db.Model):
    __tablename__ = 'test'

    test_id = db.Column(db.Integer(), primary_key = True, autoincrement = True)
    score = db.Column(db.DECIMAL(6,2), nullable = False)
    code = db.Column(db.Text(), nullable = False)
