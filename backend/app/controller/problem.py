from flask import Blueprint, current_app, redirect, url_for, flash, request, render_template_string
from flask_login import current_user, login_required
from app.model import serialize, Problem, Tag
from app.form import FormProblem, FormNewProblem
from . import render_template, admin_required
from app.extension import db

problem = Blueprint('problem', __name__)

@problem.route('/', methods = ['GET', 'POST'])
@login_required
def problemset():
	problems = Problem.query
	filter_tag_id = request.values.get('tag_id')
	filter_title = request.values.get('title')
	if filter_tag_id:
		problems = problems.join(Problem.tags).filter(Tag.tag_id == filter_tag_id)
	if filter_title:
		problems = problems.filter(Problem.title.ilike("%{0}%".format(filter_title)))
	return render_template(
		'problem/problemset.html',
		problems = [serialize(prob) for prob in problems.all()],
		tags = [serialize(tag) for tag in Tag.query.all()],
		filter_tag_id = filter_tag_id if filter_tag_id else '',
		filter_title = filter_title if filter_title else '',
	)

@problem.route('/<int:pid>', methods = ['GET', 'POST'])
@login_required
def show(pid):
	problem = Problem.query.filter_by(pid = pid).first()
	problem_dict = serialize(problem)
	problem_dict['tags'] = [serialize(s) for s in problem.tags.all()]
	return render_template('problem/problem.html', problem = problem_dict)

@problem.route('/edit/<int:pid>', methods = ['GET', 'POST'])
@admin_required
def edit(pid):
	problem = Problem.query.filter_by(pid = pid).first()
	form = FormProblem(problem)
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
	form = FormNewProblem()
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
	if not pid:
		abort(404)
	problem = Problem.query.filter_by(pid = pid)
	if problem.count() == 0:
		flash('There is no problem with the same pid!', 'error')
		return 'error'
	db.session.delete(problem.first())
	flash('Deleting problem is successful!', 'success')
	return 'success'
