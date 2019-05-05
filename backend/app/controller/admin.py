from flask import Blueprint, render_template, current_app, redirect, url_for, flash, request, render_template_string
from flask_login import current_user, login_required

from app.extension import db

admin = Blueprint('admin', __name__)

@admin.route('/user')
@login_required
def user():
    return render_template('admin/user.html')

@admin.route('/problem')
@login_required
def problem():
    return render_template('admin/problem.html')