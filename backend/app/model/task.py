from app.extension import db
from flask_login import UserMixin

class Task(UserMixin, db.Model):
    __tablename__ = 'task'

    task_id = db.Column(db.Integer(), primary_key = True, autoincrement = True)
    task_name = db.Column(db.String(64), nullable = False)
    deadline = db.Column(db.DateTime(), nullable = False)

    problems = db.relationship(
        'Problem',
        secondary = 'problem_in_task',
        backref = db.backref('tasks', lazy = 'dynamic'),
        lazy = 'dynamic'
    )
