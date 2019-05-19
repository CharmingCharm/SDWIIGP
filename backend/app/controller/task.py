from flask import Blueprint, current_app, redirect, url_for, flash, request, abort, json
from flask_login import current_user, login_required
from app.model import serialize, Task, Problem, UserGroup, User
from app.form import FormTask
from . import render_template, admin_required
from app.extension import db
from sqlalchemy import or_
from datetime import datetime

task = Blueprint('task', __name__)

@task.route('/', methods = ['GET', 'POST'])
@task.route('/<int:page>', methods = ['GET', 'POST'])
@login_required
def tasklist(page = 1):
	if not current_user.is_teacher:
		tasks = Task.query.join(Task.groups, UserGroup.users).filter(User.uid == current_user.uid)
	else:
		tasks = Task.query
	pagination = tasks.paginate(page = page, per_page = current_user.item_per_page)
	tasks = pagination.items
	return render_template('tasklist.html', tasks = tasks, now = datetime.now(), pagination = pagination)

@task.route('/show/<int:task_id>', methods = ['GET', 'POST'])
@login_required
def show(task_id):
	available = current_user.groups.join(UserGroup.tasks).filter(Task.task_id == task_id).count() > 0
	if not (available or current_user.is_teacher):
		abort(403)
	task = Task.query.filter_by(task_id = task_id).first()
	problems = task.problems.all()
	for problem in problems:
		problem.sub = problem.get_user_sub()
	return render_template('task.html', task = task, problems = problems)

@task.route('/edit/<int:task_id>', methods = ['GET', 'POST'])
@admin_required
def edit(task_id):
	task = Task.query.filter_by(task_id = task_id).first()
	form = FormTask(task_id)
	if form.validate_on_submit():
		task.task_name = form.task_name.data
		task.description = form.description.data
		task.deadline = form.deadline.data
		task.problems = form.problems.data
		task.groups = form.groups.data
		flash('Task editing is successful!', 'success')
		return redirect(url_for('task.tasklist'))
	return render_template(
		'task_edit.html',
		form = form,
		task = task,
	)

@task.route('/new', methods = ['GET', 'POST'])
@admin_required
def new():
	form = FormTask(0)
	if form.validate_on_submit():
		db.session.add(Task(
			task_name = form.task_name.data,
			description = form.description.data,
			deadline = form.deadline.data,
			problems = form.problems.data,
			groups = form.groups.data,
		))
		flash('Adding task is successful!', 'success')
		return redirect(url_for('task.tasklist'))
	return render_template('task_edit.html', form = form)

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

@task.route('/search_problem', methods = ['POST'])
@admin_required
def search_problem():
	search = request.values.get('search')
	filter_search = "%{0}%".format(search)
	problems = Problem.query.filter(or_(Problem.title.ilike(filter_search), Problem.pid == search)).all()
	return json.jsonify({
		'problems': [serialize(problem, 'pid', 'title') for problem in problems]
	})

@task.route('/search_group', methods = ['POST'])
@admin_required
def search_group():
	search = request.values.get('search')
	filter_search = "%{0}%".format(search)
	groups = UserGroup.query.filter(or_(UserGroup.group_name.ilike(filter_search), UserGroup.gid == search)).all()
	return json.jsonify({
		'groups': [serialize(group, 'gid', 'group_name') for group in groups]
	})
