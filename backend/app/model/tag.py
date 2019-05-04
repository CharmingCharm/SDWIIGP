from flask_login import UserMixin
from app.extension import db

class Tag(UserMixin, db.Model):
    __tablename__ = 'tag'

    tag_id = db.Column(db.Integer(), primary_key = True, autoincrement = True)
    tag_name = db.Column(db.String(64), nullable = False)

    problems = db.relationship(
        'Problem',
        secondary = 'tag_of_problem',
        backref = db.backref('tags', lazy = 'dynamic'),
        lazy = 'dynamic'
    )

    def __repr__(self):
        return self.tag_name
