from flask import Blueprint, current_app, redirect, url_for, flash, request, abort, json
from flask_login import current_user, login_required
from app.model import serialize, Problem, Tag, Test, TestSet, Submission, Task, UserGroup
from . import render_template, admin_required, str_time
from app.extension import db
from app.daemon import judge
from app.form import FormRejudge
from datetime import datetime

submission = Blueprint('submission', __name__)

@submission.route('/', methods = ['GET', 'POST'])
@submission.route('/<int:page>', methods = ['GET', 'POST'])
@login_required
def status(page = 1):
	pagination = Submission.query.order_by(Submission.sid.desc()).paginate(page=page,per_page=current_user.item_per_page)
	submissions = pagination.items
	return render_template('status.html', submissions = submissions, pagination = pagination)

@submission.route('/show/<int:sid>', methods = ["GET"])
@login_required
def show(sid):
	sub = Submission.query.filter_by(sid = sid)
	if sub.count() == 0:
		abort(404)
	sub = sub.first()
	if (not current_user.is_teacher) and (not sub.is_solution) and (sub.uid != current_user.uid or sub.status == 'hidden'):
		abort(403)
	if sub.status == 'pending' or sub.status == 'running' or sub.status == 'system_error':
		result_tests = []
	else:
		result_tests = json.loads(sub.result)
		show_first_wrong = True
		for test in result_tests:
			test['full_score'] = float(str(Test.query.filter_by(test_id = test['test_id']).first().score))
			test['is_show'] = current_user.is_teacher or (show_first_wrong and test['score'] == 0.0)
			show_first_wrong = show_first_wrong and (not test['is_show'])
	return render_template('submission.html', submission = sub, result_tests = result_tests)

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
	try:
		judge.queue(sub.sid)
		print('[Info] Submitted #%d to judger' % sub.sid)
	except:
		print('[Error] Failed to submit #%d to judger!' % sub.sid)
	flash('Your code is submitted!', 'success')
	return 'success'

@submission.route('/rejudge', methods = ['GET', 'POST'])
@admin_required
def rejudge():
	form = FormRejudge()
	rejudge_list = []
	if request.method == 'POST':
		if form.rejudge_type.data == 'sid':
			rejudge_list = Submission.query.filter(Submission.sid == form.sid.data).all()
		elif form.rejudge_type.data == 'pid':
			rejudge_list = Submission.query.filter(Submission.pid == form.pid.data).all()
		elif form.rejudge_type.data == 'task_id':
			rejudge_list = Submission.query.filter(Submission.task_id == form.task_id.data).all()
		elif form.rejudge_type.data == 'pending':
			rejudge_list = Submission.query.filter(Submission.result == None).all()
		
		if not form.rejudge_confirm.data:
			return str(len(rejudge_list))
		else:
			for sub in rejudge_list:
				try:
					sub.score = None
					sub.result = None
					db.session.commit()
					judge.queue(sub.sid)
					print('[Info] Submitted #%d to judger' % sub.sid)
				except:
					print('[Error] Failed to submit #%d to judger!' % sub.sid)
			flash('Submitting rejudge successfully!', 'success')
			return redirect(url_for('submission.status'))
	return render_template('rejudge.html', form = form)
