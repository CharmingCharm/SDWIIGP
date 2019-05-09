from flask import Blueprint, flash, render_template, redirect, url_for, current_app, request

from app.extension import db
from app.model import User
from app.form import FormLogin
from app.form import FormProfile
from flask_login import login_user, logout_user, current_user, login_required

auth = Blueprint('auth', __name__)

from urllib.parse import urlparse, urljoin
from flask import request, url_for

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@auth.route('/login', methods = ['GET', 'POST'])
def login():
	form = FormLogin()
	if form.validate_on_submit():
		name = form.user_name.data
		user = User.query.filter(User.user_name == name).first()
		if not user:
			flash('Wrong username or password', 'error')
		elif not user.verify_password(form.password.data):
			flash('Wrong username or password', 'error')
		else:
			login_user(user, remember = form.remember.data)
			next = request.values.get('next')
			if not is_safe_url(next):
				return flask.abort(400)
			return redirect(next or url_for('main.home'))
	return render_template('login.html', form = form)

@auth.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.home'))

@auth.route('/profile')
@login_required
def profile():
	form = FormProfile()
	if form:
		if form.validate_on_submit():
			uid = form.uid.data
			user_name = form.user_name.data
			user = User.query.filter(User.uid == uid).first()
			user.user_name = user_name
			if form.password.data and user.verify_password(form.oldPassword.data) and form.password.data == form.checkPassword.data:
				user.password = form.password.data
	return render_template('profile.html')
