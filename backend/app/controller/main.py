from flask import Blueprint, render_template, current_app, redirect, url_for, flash, request, render_template_string
from flask_login import current_user, login_required

from app.extension import db

main = Blueprint('main', __name__)

@main.route('/', methods = ['GET', 'POST'])
@main.route('/home', methods = ['GET', 'POST'])
@login_required
def home():
    return render_template('index.html', username = current_user.name, isTeacher = current_user.isTeacher)
