from flask import Blueprint, current_app, redirect, url_for, flash, request, render_template_string
from flask_login import current_user, login_required
from app.model import serialize, Submission
from . import render_template
from app.extension import db

main = Blueprint('main', __name__)

@main.route('/', methods = ['GET', 'POST'])
@main.route('/home', methods = ['GET', 'POST'])
@login_required
def home():
    return render_template('home.html')

@main.route('/status', methods = ['GET', 'POST'])
@login_required
def status():
    submissions = [serialize(submission) for submission in Submission.query.all()]
    sub_array = []
    for sub in submissions:
        sub_array.append(Submission.query.filter_by(sid = sub['sid']).first())
    return render_template('status.html', submissions = sub_array)
