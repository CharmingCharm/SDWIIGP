from flask import Blueprint, current_app, redirect, url_for, flash, request, abort, json
from flask_login import current_user, login_required
from app.model import serialize, Problem, Tag, Test, TestSet, Submission, Task, UserGroup
from . import render_template, admin_required, str_time
from app.extension import db
from app.daemon import judge
from datetime import datetime

submission = Blueprint('submission', __name__)

@submission.route('/', methods = ['GET', 'POST'])
@submission.route('/<int:page>', methods = ['GET', 'POST'])
@login_required
def status(page = 1):
	pagination = Submission.query.paginate(page=page,per_page=5)
	submissions = pagination.items
	return render_template('status.html', submissions = submissions, pagination = pagination)

@submission.route('/new/<int:pid>', methods = ['POST'])
@login_required
def new(pid):
	if not request.values.get('code'):
		flash('Your code is required!', 'error')
		return 'empty code'
	sub = Submission(
		pid = pid,
		uid = current_user.uid,
		code = request.values.get('code'),
	)

	related_task = Task.query.filter(Task.deadline > str_time(datetime.now())) \
		.join(Task.problems).filter(Problem.pid == pid) \
		.join(Task.groups).filter(UserGroup.gid.in_(current_user.groups.with_entities(UserGroup.gid)))
	if related_task.count() > 1:
		flash('This problem is in multiple active tasks. Please contact teachers.', 'warning')
		return 'problem in multiple tasks'
	related_task = related_task.first()
	if related_task:
		sub.task = related_task
	
	db.session.add(sub)
	db.session.commit()
	judge.queue(sub.sid)
	flash('Success!', 'success')
	return 'success'
