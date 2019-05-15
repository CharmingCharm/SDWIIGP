from flask import Blueprint, current_app, redirect, url_for, flash, request, render_template_string
from flask_login import current_user, login_required
from app.model import serialize, Task
from . import render_template
from app.extension import db
from datetime import datetime

tasks = Blueprint('task', __name__)

@tasks.route('/', methods = ['GET', 'POST'])
@tasks.route('/<int:page>', methods = ['GET', 'POST'])
@login_required
def task(page = 1):
    pagination = Task.query.paginate(page=page,per_page=5)
    tasks = pagination.items
    return render_template('task.html',tasks = tasks,now = datetime.now(), pagination = pagination)

@tasks.route('/show/<task_id>', methods = ['GET', 'POST'])
@login_required
def show(task_id):
    task = Task.query.filter_by(task_id = task_id).first()
    return render_template('problem/task_problem.html', task = task)
