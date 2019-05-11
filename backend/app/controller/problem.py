from flask import Blueprint, current_app, redirect, url_for, flash, request, render_template_string
from flask_login import current_user, login_required
from app.model import serialize, Problem, Tag
from app.form import FormProblem
from . import render_template
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
