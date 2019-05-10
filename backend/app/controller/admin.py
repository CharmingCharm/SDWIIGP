from flask import Blueprint, current_app, redirect, url_for, flash, request, render_template_string
from flask_login import current_user, login_required
from app.form import FormProblem
from app.model import serialize, Problem, Tag
from . import render_template
from app.extension import db

admin = Blueprint('admin', __name__)

@admin.route('/user')
@login_required
def user():
	return render_template('admin/user.html')

@admin.route('/problem/<pid>', methods = ['GET', 'POST'])
@login_required
def problem(pid):
	if not current_user.is_teacher:
		return 'You are not allowed to edit!'
	
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


@admin.route('/tag', methods = ['GET', 'POST'])
@login_required
def tag():
	return render_template('admin/tag.html')
