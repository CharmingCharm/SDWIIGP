from flask import Blueprint, current_app, redirect, url_for, flash, request, render_template_string
from flask_login import current_user, login_required
from app.form import FormProblem, FormUserGroup, FormUsers, FormUserSingle, FormGroupList
from app.model import serialize, Problem, Tag, UserGroup, User
from . import render_template
from app.extension import db

admin = Blueprint('admin', __name__)

@admin.route('/user', methods = ['GET', 'POST'])
@login_required
def user():
	form = FormUsers()
	if form.addID.data and form.new_user_name.data and form.new_position.data:
		if User.query.filter_by(user_name = form.new_user_name.data).first():
			flash(form.new_user_name.data + ' is exist, change your name!','error')
		else:
			db.session.add(User(user_name=form.new_user_name.data,
								password=form.new_user_name.data,
								is_teacher=True if form.new_position.data == 'Teacher' else False))
			db.session.commit()
			flash('Success!','success')
	
	if form.users.__len__():
		while form.users.__len__() > 0:
			userForm = form.users.pop_entry()
			if userForm.changeID.data:
				user = User.query.filter_by(uid = userForm.uid.data).first()
				user.user_name = userForm.user_name.data
				user.is_teacher = True if userForm.position.data == 'Teacher' else False
				flash('Success!','success')
			elif userForm.deleteID.data:
				User.query.filter_by(uid = userForm.uid.data).delete()
				flash('Delete successfully!','success')

	users = User.query.all()
	for user in users:
		userForm = FormUserSingle()
		userForm.uid = user.uid
		userForm.user_name = user.user_name
		userForm.position = 'Teacher' if user.is_teacher else 'Student'
		form.users.append_entry(data=userForm)

	return render_template('admin/user.html', form = form)

@admin.route('/problem/<int:pid>', methods = ['GET', 'POST'])
@login_required
def problem(pid):
	if not current_user.is_teacher:
		return 'You are not allowed to edit!'
	
	problem = Problem.query.filter_by(pid = pid).first()
	form = FormProblem(problem)
	if form.validate_on_submit():
		problem.title = form.title.data
		problem.description = form.description.data
		problem.level = form.level.data
		problem.tags = form.tags.data
		flash('Problem editing is successful', 'success')
		return redirect(url_for('problem.problemset'))
	
	return render_template(
		'problem/edit.html',
		form = form,
		problem = serialize(problem, 'pid', 'title')
	)

@admin.route('/tag', methods = ['GET', 'POST'])
@login_required
def tag():
	return render_template('admin/tag.html')

@admin.route('/userGroup', methods = ['GET', 'POST'])
@login_required
def userGroup():
	form = FormGroupList()
	if form.groups.__len__():
		print(form.groups.__getitem__(0).group_name)
		while form.groups.__len__() > 0:
			groupForm = form.groups.pop_entry()
			print(groupForm.deleteID.data)
			if groupForm.deleteID.data:
				UserGroup.query.filter_by(gid = groupForm.gid.data).delete()
				flash('Delete successfully!','success')

	user_groups = UserGroup.query.all()
	for group in user_groups:
		groupForm = FormUserGroup()
		groupForm.gid = group.gid
		groupForm.group_name = group.group_name
		groupForm.number = group.users.count()
		form.groups.append_entry(groupForm)
	return render_template('admin/user_group_list.html', form = form)

@admin.route('/userGroup/<int:gid>', methods = ['GET', 'POST'])
@login_required
def userGroupDetail(gid):
	form = FormUserGroup()
	user_group = UserGroup.query.filter_by(gid = gid).first()
	form.group_name.data = user_group.group_name
	form.description.data = user_group.description

	# if form.addID.data:
	# 	User.query.filter(User.user_name.like('%%' + form.new_user_name.data + '%%')).all()
	return render_template('admin/group_detail.html', user_group = user_group, form = form)
