from flask import Blueprint, current_app, redirect, url_for, flash, request, abort
from flask_login import current_user, login_required
from app.model import serialize, Task
from . import render_template, admin_required
from app.extension import db
from datetime import datetime

task = Blueprint('task', __name__)

@task.route('/', methods = ['GET', 'POST'])
@task.route('/<int:page>', methods = ['GET', 'POST'])
@login_required
def tasklist(page = 1):
	pagination = Task.query.paginate(page=page,per_page=5)
	tasks = pagination.items
	return render_template('tasklist.html',tasks = tasks,now = datetime.now(), pagination = pagination)

@task.route('/show/<int:task_id>', methods = ['GET', 'POST'])
@login_required
def show(task_id):
	task = Task.query.filter_by(task_id = task_id).first()
	return render_template('task.html', task = task)

@task.route('/edit/<int:task_id>', methods = ['GET', 'POST'])
@admin_required
def edit(task_id):
	pass

@task.route('/new', methods = ['GET', 'POST'])
@admin_required
def new():
	pass

@task.route('/delete', methods = ['GET', 'POST'])
@admin_required
def delete():
	task_id = request.values.get('task_id')
	if not task_id:
		abort(404)
	task = Task.query.filter_by(task_id = task_id)
	if task.count() == 0:
		flash('There is no task with the same id!', 'error')
		return 'error'
	db.session.delete(task.first())
	flash('Deleting task is successful!', 'success')
	return 'success'
