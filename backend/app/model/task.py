from app.extension import db

class Task(db.Model):
    __tablename__ = 'task'

    task_id = db.Column(db.Integer(), primary_key = True, autoincrement = True)
    task_name = db.Column(db.String(64), nullable = False)
    description = db.Column(db.Text, nullable = False, default = '')
    deadline = db.Column(db.DateTime(), nullable = False)

    problems = db.relationship(
        'Problem',
        secondary = 'problem_in_task',
        backref = db.backref('tasks', lazy = 'dynamic'),
        lazy = 'dynamic'
    )

    groups = db.relationship(
        'UserGroup',
        secondary = 'task_for_user_group',
        backref = db.backref('tasks', lazy = 'dynamic'),
        lazy = 'dynamic'
    )
