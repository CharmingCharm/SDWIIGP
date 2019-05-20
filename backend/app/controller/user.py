from flask import Blueprint, flash, render_template, redirect, url_for, current_app, request, abort
from flask import render_template as render_template_origin
from app.extension import db, photos
from app.model import User
from app.form import FormLogin, FormProfile, FormUsers, FormUserSingle, FormIcon
from flask_login import login_user, logout_user, current_user, login_required
from . import render_template, admin_required
from app.helper import random_string
from PIL import Image
import os

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
	return render_template_origin('login.html', form = form)

@user.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.home'))

@user.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
	form = FormProfile()
	if form.item_per_page.data:
		current_user.item_per_page = form.item_per_page.data
	else:
		form.item_per_page.data = current_user.item_per_page		

	if form.validate_on_submit():
		if form.password.data and current_user.verify_password(form.old_password.data) and form.password.data == form.check_password.data:
			current_user.password = form.password.data
			flash('Password change is successful!', 'success')
		else:
			flash('Fail to change password! Please check the inputs.', 'error')
	return render_template('profile.html', form = form)

@user.route('/change_avatar', methods = ['POST'])
@login_required
def change_avatar():
	form = FormIcon()
	if form.validate_on_submit():
		suffix = form.avatar.data.filename
		filename = random_string() + suffix
		photos.save(form.avatar.data, name = filename)

		fullpath = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], filename)
		img = Image.open(fullpath)
		width, height = img.size
		print(width, height)
		if width > height:
			diff = (width - height) / 2.0
			print((diff, 0, width - diff, height))
			img = img.crop((diff, 0, width - diff, height))
		else:
			diff = (height - width) / 2.0
			img = img.crop((0, diff, width, height - diff))
		img.save(fullpath)
		
		current_user.avatar = filename
		flash('Upload avatar successfully!', 'success')
		return redirect(url_for('user.profile'))
	for error in form.avatar.errors:
		flash(error, 'error')
	return redirect(url_for('user.profile'))

@user.route('/admin', methods = ['GET', 'POST'])
@user.route('/admin/<int:page>', methods = ['GET', 'POST'])
@admin_required
def admin(page = 1):
	form = FormUsers()
	if form.addID.data and form.new_user_name.data and form.new_position.data:
		if User.query.filter_by(user_name = form.new_user_name.data).first():
			flash(form.new_user_name.data + ' is exist, change your name!','error')
		else:
			db.session.add(User(user_name=form.new_user_name.data,
								password=form.new_user_name.data,
								position=form.new_position.data))
			db.session.commit()
			flash('Success!','success')
	
	if form.users.__len__():
		while form.users.__len__() > 0:
			userForm = form.users.pop_entry()
			if userForm.changeID.data:
				user = User.query.filter_by(uid = userForm.uid.data).first()
				user.user_name = userForm.user_name.data
				user.position = userForm.position.data
				flash('Success!','success')
			elif userForm.deleteID.data:
				User.query.filter_by(uid = userForm.uid.data).delete()
				flash('Delete successfully!','success')

	pagination = User.query.paginate(page=page,per_page=current_user.item_per_page)
	users = pagination.items
	for user in users:
		userForm = FormUserSingle()
		userForm.uid = user.uid
		userForm.user_name = user.user_name
		userForm.position = 'Teacher' if user.is_teacher else 'Student'
		form.users.append_entry(data=userForm)

	return render_template('admin/user.html', form = form, pagination = pagination)