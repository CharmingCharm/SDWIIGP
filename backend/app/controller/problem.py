from flask import Blueprint, current_app, redirect, url_for, flash, request, abort, json
from flask_login import current_user, login_required
from app.model import serialize, Problem, Tag, Test, TestSet, Submission
from app.form import FormProblem, FormProblemFilter
from . import render_template, admin_required
from app.extension import db
from decimal import Decimal
import re

problem = Blueprint('problem', __name__)

@problem.route('/', methods = ['GET', 'POST'])
@login_required
def problemset():
	problems = Problem.query
	form = FormProblemFilter()
	if form.title.data:
		problems = problems.filter(Problem.title.ilike("%{0}%".format(form.title.data)))
	if form.level.data and (form.level.data != "0"):
		problems = problems.filter(Problem.level == form.level.data)
	if form.tag_id.data:
		problems = problems.join(Problem.tags).filter(Tag.tag_id == form.tag_id.data)
	if not current_user.is_teacher:
		problems = problems.filter(Problem.visible == True)
	pagination = problems.paginate(page = int(form.page.data), per_page = current_user.item_per_page)
	problems = pagination.items
	for problem in problems:
		problem.sub = problem.get_user_sub()
	return render_template(
		'problem/problemset.html',
		problems = problems,
		tags = Tag.query.all(),
		form = form,
		pagination = pagination,
	)

@problem.route('/<int:pid>', methods = ['GET', 'POST'])
@login_required
def show(pid):
	problem = Problem.query.filter_by(pid = pid).first()
	if (not problem) or (not (current_user.is_teacher or problem.visible)):
		abort(404)
	problem.sub = problem.get_user_sub()
	problem.last_sub = current_user.submissions.filter_by(pid = pid).order_by(Submission.sid.desc()).first()
	return render_template('problem/problem.html', problem = problem)

@problem.route('/edit/<int:pid>', methods = ['GET', 'POST'])
@admin_required
def edit(pid):
	problem = Problem.query.filter_by(pid = pid).first()
	form = FormProblem(pid)
	if form.validate_on_submit():
		problem.title = form.title.data
		problem.description = form.description.data
		problem.level = form.level.data
		problem.tags = form.tags.data
		flash('Problem editing is successful', 'success')
		return redirect(url_for('problem.problemset'))
	
	return render_template(
		'problem/edit.html',
		form = form,
		problem = serialize(problem, 'pid', 'title')
	)

@problem.route('/new', methods = ['GET', 'POST'])
@admin_required
def new():
	form = FormProblem(0)
	if form.validate_on_submit():
		db.session.add(Problem(
			title = form.title.data,
			description = form.description.data,
			level = form.level.data,
			tags = form.tags.data))
		flash('Adding problem is successful!', 'success')
		return redirect(url_for('problem.problemset'))
	return render_template('problem/edit.html', form = form)

@problem.route('/delete', methods = ['GET', 'POST'])
@admin_required
def delete():
	pid = request.values.get('pid')
	problem = Problem.query.filter(Problem.pid == pid)
	if problem.count() == 0:
		flash('There is no problem with the same pid!', 'error')
		return 'error'
	db.session.delete(problem.first())
	flash('Deleting problem is successful!', 'success')
	return 'success'

@problem.route('/change_visible', methods = ['GET', 'POST'])
@admin_required
def change_visible():
	pid = request.values.get('pid')
	problem = Problem.query.filter(Problem.pid == pid)
	if problem.count() == 0:
		flash('There is no problem with the same pid!', 'error')
		return 'error'
	problem = problem.first()
	problem.visible = not problem.visible
	flash('Setting visible is successful!', 'success')
	return 'success'

@problem.route('/testset/<int:pid>', methods = ['GET', 'POST'])
@admin_required
def testset(pid):
	problem = Problem.query.filter_by(pid = pid).first()
	if request.method == 'POST':
		tests = json.loads(request.values.get('tests'))
		old_tests = problem.testset.tests.all() if problem.testset else []
		add_tests = []
		new_tests = []
		full_score = 0.0
		for test_upload in tests:
			if not re.match(re.compile(r"^(-?\d+)(\.\d*)?$"), test_upload['score']):
				flash('Score "' + test_upload['score'] + '" are not decimals!', 'error')
				return 'score error'
			test_upload['score'] = Decimal(test_upload['score']).quantize(Decimal('0.00'))
			full_score = full_score + float(test_upload['score'])
			test = Test.query.filter(Test.test_id == test_upload['test_id']).first()
			if (not test) or test.score != test_upload['score'] or test.code != test_upload['code']:
				add_tests.append(Test(score = test_upload['score'], code = test_upload['code']))
			else:
				old_tests.remove(test)
				new_tests.append(test)
		if old_tests or add_tests:
			new_tests.extend(add_tests)
			testset = problem.testset
			new_testset = TestSet(tests = new_tests, full_score = full_score)
			db.session.add(new_testset)
			problem.testset = new_testset
			if testset and (not testset.submissions.count()):
				db.session.delete(testset)
		flash('Setting testset is successful!', 'success')
		return 'success'
	return render_template('problem/testset.html', problem = problem)
