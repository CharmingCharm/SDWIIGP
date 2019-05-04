from flask import Blueprint, render_template, current_app, redirect, url_for, flash, request, render_template_string
from flask_login import current_user, login_required

from app.extension import db

problem = Blueprint('problem', __name__)

@problem.route('/', methods = ['GET', 'POST'])
@login_required
def problemset():
    return render_template('problem/problemset.html')
