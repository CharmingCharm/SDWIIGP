from app.extension import db
from flask_login import UserMixin
from datetime import datetime

class Submission(UserMixin, db.Model):
    __tablename__ = 'Submission'

    sID = db.Column(db.Integer(), primary_key = True, autoincrement = True)
    score = db.Column(db.DECIMAL(6,2))
    isSolution = db.Column(db.Boolean(), default = False, nullable = False)
    code = db.Column(db.Text(), nullable = False)
    dateAndTime = db.Column(db.DateTime(), nullable = False, default = datetime.now)
