from flask import Blueprint, render_template, current_app, redirect, url_for, flash, request, render_template_string
from flask_login import current_user, login_required
from app.form import FormProblem
from app.model import serialize, Problem, Tag

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
    
    form = FormProblem()
    problem = Problem.query.filter_by(pid = pid).first()
    problem_dict = serialize(problem)
    problem_dict['tags'] = [serialize(s) for s in problem.tags.all()]
    return render_template('problem/edit.html', form = form, problem = problem_dict, tags = [serialize(t) for t in Tag.query.all()])
