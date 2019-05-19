from flask import Blueprint, current_app, redirect, url_for, flash, request, render_template_string
from flask_login import current_user, login_required
from app.model import serialize, Submission, Announcement, User
from . import render_template
from app.extension import db
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/', methods = ['GET', 'POST'])
@main.route('/home', methods = ['GET', 'POST'])
@login_required
def home():
    announcements = Announcement.query.join(Announcement.user).filter(Announcement.uid == User.uid).order_by(Announcement.date_time.desc()).limit(2).all()
    return render_template('home.html', annos = announcements)

@main.route('/change_status', methods = ['POST'])
@login_required
def change_status():
    sid = int(request.values.get('sid'))
    submission = Submission.query.filter_by(sid = sid).first()
    submission.is_solution = False if submission.is_solution else True
    flash('Success!','success')
    return 'success'

@main.route('/anno_edition', methods = ['POST'])
@login_required
def anno_edition():
    new_title = request.values.get('new_title')
    new_descr = request.values.get('new_descr')
    aid = request.values.get('aid')
    anno = Announcement.query.filter_by(aid = aid).first()
    if not anno:
        flash('No that announcement', 'error')
        return 'error'
    anno.title = new_title
    anno.description = new_descr
    flash('Success!', 'success')
    return 'success'

@main.route('/anno_deletion', methods = ['POST'])
@login_required
def anno_deletion():
    aid = request.values.get('aid')
    anno = Announcement.query.filter_by(aid = aid).first()
    if not anno:
        flash('No that announcement', 'error')
        return 'error'
    db.session.delete(anno)
    flash('Success!', 'success')
    return 'success'

@main.route('/anno_addition', methods = ['POST'])
@login_required
def anno_addition():
    new_title = request.values.get('new_title')
    new_descr = request.values.get('new_descr')
    uid = request.values.get('uid')
    date_time = datetime.now()
    db.session.add(Announcement( uid = uid, title = new_title, description = new_descr, date_time = date_time))
    flash('Success!', 'success')
    return 'success'
