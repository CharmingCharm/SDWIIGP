from flask import Blueprint, current_app, redirect, url_for, flash, request, render_template_string
from flask_login import current_user, login_required
from app.model import serialize, Submission, Announcement, User
from . import render_template
from app.extension import db

main = Blueprint('main', __name__)

@main.route('/', methods = ['GET', 'POST'])
@main.route('/home', methods = ['GET', 'POST'])
@login_required
def home():
    announcements = Announcement.query.join(Announcement.user).filter(Announcement.uid == User.uid).all()
    return render_template('home.html', annos = announcements)

@main.route('/status', methods = ['GET', 'POST'])
@main.route('/status/<int:page>', methods = ['GET', 'POST'])
@login_required
def status(page = 1):
    pagination = Submission.query.paginate(page=page,per_page=5)
    submissions = pagination.items
    return render_template('status.html', submissions = submissions, pagination = pagination)
