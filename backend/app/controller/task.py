from flask import Blueprint, render_template, current_app, redirect, url_for, flash, request, render_template_string
from flask_login import current_user, login_required
from app.model import serialize, Problem, Tag

from app.extension import db

tasks = Blueprint('task', __name__)

@tasks.route('/', methods = ['GET', 'POST'])
@login_required
def task():
    return render_template('task.html')