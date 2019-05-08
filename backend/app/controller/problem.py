from flask import Blueprint, render_template, current_app, redirect, url_for, flash, request, render_template_string
from flask_login import current_user, login_required
from app.model import serialize, Problem, Tag
from app.form import FormProblem

from app.extension import db

problem = Blueprint('problem', __name__)

@problem.route('/', methods = ['GET', 'POST'])
@login_required
def problemset():
    return render_template(
        'problem/problemset.html',
        problems = [serialize(prob) for prob in Problem.query.all()],
        tags = [serialize(tag) for tag in Tag.query.all()]
    )

@problem.route('/<pid>', methods = ['GET', 'POST'])
@login_required
def show(pid):
    problem = Problem.query.filter_by(pid = pid).first()
    problem_dict = serialize(problem)
    problem_dict['tags'] = [serialize(s) for s in problem.tags.all()]
    return render_template('problem/problem.html', problem = problem_dict)
