from flask import Blueprint, current_app, redirect, url_for, flash, request, render_template_string
from flask_login import current_user, login_required
from app.model import serialize, Task
from . import render_template
from app.extension import db
from datetime import datetime

tasks = Blueprint('task', __name__)

@tasks.route('/', methods = ['GET', 'POST'])
@login_required
def task():
    tasks = [serialize(task) for task in Task.query.all()]
    print("ooooo")
    for task in tasks:
        task['deadline'] = datetime.strptime(task['deadline'], '%Y-%m-%d %H:%M:%S')
    return render_template('task.html',tasks = tasks,now = datetime.now())

@tasks.route('/<task_id>', methods = ['GET', 'POST'])
@login_required
def show(task_id):
    task = Task.query.filter_by(task_id = task_id).first()
    return render_template('problem/task_problem.html', task = task)
