from flask import Blueprint, current_app, redirect, url_for, flash, request, render_template_string
from flask_login import current_user, login_required
from app.model import serialize, Submission
from . import render_template
from app.extension import db

stat = Blueprint('status', __name__)

@stat.route('/', methods = ['GET', 'POST'])
@login_required
def status():
    submissions = [serialize(submission) for submission in Submission.query.all()]
    for sub in submissions:
        print(sub.user)
    return render_template('status.html', submissions = submissions)
