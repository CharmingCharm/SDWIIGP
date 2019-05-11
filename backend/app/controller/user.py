from flask import Blueprint, flash, render_template, redirect, url_for, current_app, request, abort

from app.extension import db
from app.model import User
from app.form import FormLogin, FormProfile
from flask_login import login_user, logout_user, current_user, login_required

user = Blueprint('user', __name__)

from urllib.parse import urlparse, urljoin
from flask import request, url_for

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@user.route('/login', methods = ['GET', 'POST'])
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
				return abort(400)
			return redirect(next or url_for('main.home'))
	return render_template('login.html', form = form)

@user.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.home'))

@user.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
	form = FormProfile()
	if form.validate_on_submit():
		if form.password.data and current_user.verify_password(form.old_password.data) and form.password.data == form.check_password.data:
			current_user.password = form.password.data
			flash('Password change is successful!', 'success')
		else:
			flash('Fail to change password! Please check the inputs.', 'error')
	return render_template('profile.html', form = form)
