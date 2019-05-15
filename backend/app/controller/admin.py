from flask import Blueprint, current_app, redirect, url_for, flash, request, json, abort, jsonify
from flask_paginate import Pagination, get_page_parameter
from flask_login import current_user, login_required
from app.form import FormProblem, FormUserGroup, FormUsers, FormUserSingle, FormGroupList
from app.model import serialize, Problem, Tag, UserGroup, User, UserInGroup
from . import render_template
from app.extension import db

admin = Blueprint('admin', __name__)

@admin.route('/user', methods = ['GET', 'POST'])
@admin.route('/user/<int:page>', methods = ['GET', 'POST'])
@login_required
def user(page = 1):
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

	pagination = User.query.paginate(page=page,per_page=5)
	users = pagination.items
	for user in users:
		userForm = FormUserSingle()
		userForm.uid = user.uid
		userForm.user_name = user.user_name
		userForm.position = 'Teacher' if user.is_teacher else 'Student'
		form.users.append_entry(data=userForm)

	return render_template('admin/user.html', form = form, pagination = pagination)

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
	return render_template('admin/tag.html', tags = [serialize(tag) for tag in Tag.query.all()])

@admin.route('/add_tag', methods = ['POST'])
@login_required
def add_tag():
	if not current_user.is_teacher:
		return 'unauthorized'
	
	tag_name = request.values.get('tag_name')
	if Tag.query.filter(Tag.tag_name == tag_name).count() > 0:
		flash('There is already a tag with the same name!', 'error')
		return 'error'
	db.session.add(Tag(tag_name = tag_name))
	flash('Adding tag is successful!', 'success')
	return 'success'

@admin.route('/delete_tag', methods = ['POST'])
@login_required
def delete_tag():
	if not current_user.is_teacher:
		return 'unauthorized'

	tag_id = request.values.get('tag_id')
	tag = Tag.query.filter(Tag.tag_id == tag_id)
	if tag.count() == 0:
		flash('There is no tag with the same id!', 'error')
		return 'error'
	tag = tag.first()
	db.session.delete(tag)
	flash('Deleting tag is successful!', 'success')
	return 'success'

@admin.route('/change_tag', methods = ['POST'])
@login_required
def change_tag():
	if not current_user.is_teacher:
		return 'unauthorized'

	tag_id = request.values.get('tag_id')
	tag = Tag.query.filter(Tag.tag_id == tag_id)
	if tag.count() == 0:
		flash('There is no tag with the same id!', 'error')
		return 'error'
	tag = tag.first()
	tag.tag_name = request.values.get('tag_name')
	flash('Changing tag is successful!', 'success')
	return 'success'

@admin.route('/userGroup', methods = ['GET', 'POST'])
@admin.route('/userGroup/<int:page>', methods = ['GET', 'POST'])
@login_required
def userGroup(page = 1):
	form = FormGroupList()
	if form.groups.__len__():
		print(form.groups.__getitem__(0).group_name)
		while form.groups.__len__() > 0:
			groupForm = form.groups.pop_entry()
			if groupForm.deleteID.data:
				UserGroup.query.filter_by(gid = groupForm.gid.data).delete()
				flash('Delete successfully!','success')

	pagination = UserGroup.query.paginate(page=page,per_page=5)
	user_groups = pagination.items
	for group in user_groups:
		groupForm = FormUserGroup()
		groupForm.gid = group.gid
		groupForm.group_name = group.group_name
		groupForm.number = group.users.count()
		form.groups.append_entry(groupForm)
	return render_template('admin/user_group_list.html', form = form, pagination = pagination)

@admin.route('/userGroup/<int:gid>', methods = ['GET', 'POST'])
@login_required
def userGroupDetail(gid):
	form = FormUserGroup()
	user_group = UserGroup.query.filter_by(gid = gid).first()
	form.group_name.data = user_group.group_name
	form.description.data = user_group.description
	form.number.data = user_group.users.count()
	return render_template('admin/group_detail.html', user_group = user_group, form = form)

@admin.route('/search_new_user', methods = ['POST'])
@login_required
def search_new_user():
	if not current_user.is_teacher:
		return 'unauthorized'

	new_user_name = request.values.get('new_user_name')
	users = User.query.filter(User.user_name.like('%%' + new_user_name + '%%')).all()
	user_array = []
	for user in users:
		user_array.append({'uid':user.uid, 'user_name':user.user_name})
	return jsonify({'user': user_array})

@admin.route('/add_new_user', methods = ['POST'])
@login_required
def add_new_user():
	if not current_user.is_teacher:
		return 'unauthorized'

	new_uid = request.values.get('user_id')
	gid = request.values.get('group_id')
	if UserInGroup.query(uid = uid, gid = gid).count() > 0:
		flash('The user is already in the group!', 'error')
		return 'error'
	db.session.add(UserInGroup(uid = new_uid, gid = gid))
	db.session.commit()
	flash('Success!', 'success')
	return redirect("url_for('admin.userGroupDetail')")
