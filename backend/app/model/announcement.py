from app.extension import db
from datetime import datetime

class Announcement(db.Model):
    __tablename__ = 'announcement'

    aid = db.Column(db.Integer(), primary_key = True, autoincrement = True)
    uid = db.Column(db.Integer, db.ForeignKey('user.uid'))
    title = db.Column(db.String(64), nullable = False)
    description = db.Column(db.Text(), nullable = False)
    date_time = db.Column(db.DateTime(), nullable = False, default = datetime.now)

    user = db.relationship('User', backref = 'announcements')
