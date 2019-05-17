from flask import Blueprint, current_app, redirect, url_for, flash, request, json, abort, jsonify
from flask_paginate import Pagination, get_page_parameter
from flask_login import current_user, login_required
from app.form import FormProblem, FormNewProblem, FormUserGroup, FormUsers, FormUserSingle, FormGroupList
from app.model import serialize, Problem, Tag, UserGroup, User, UserInGroup
from . import render_template, admin_required
from app.extension import db

admin = Blueprint('admin', __name__)

@admin.route('/tag', methods = ['GET', 'POST'])
@admin_required
def tag():
	return render_template('admin/tag.html', tags = [serialize(tag) for tag in Tag.query.all()])

@admin.route('/add_tag', methods = ['POST'])
@admin_required
def add_tag():
	tag_name = request.values.get('tag_name')
	if Tag.query.filter(Tag.tag_name == tag_name).count() > 0:
		flash('There is already a tag with the same name!', 'error')
		return 'error'
	db.session.add(Tag(tag_name = tag_name))
	flash('Adding tag is successful!', 'success')
	return 'success'

@admin.route('/delete_tag', methods = ['POST'])
@admin_required
def delete_tag():
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
@admin_required
def change_tag():
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
@admin_required
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

@admin.route('/userGroup/show/<int:gid>', methods = ['GET', 'POST'])
@admin_required
def userGroupDetail(gid):
	form = FormUserGroup()
	user_group = UserGroup.query.filter_by(gid = gid).first()
	form.group_name.data = user_group.group_name
	form.description.data = user_group.description
	form.number.data = user_group.users.count()
	return render_template('admin/group_detail.html', user_group = user_group, form = form)

@admin.route('/search_new_user', methods = ['POST'])
@admin_required
def search_new_user():
	new_user_name = request.values.get('new_user_name')
	users = User.query.filter(User.user_name.like('%%' + new_user_name + '%%')).all()
	user_array = []
	for user in users:
		user_array.append({'uid':user.uid, 'user_name':user.user_name})
	return jsonify({'user': user_array})

@admin.route('/add_new_user', methods = ['POST'])
@admin_required
def add_new_user():
	new_uid = request.values.get('user_id')
	new_user = User.query.filter_by(uid = new_uid).first()
	gid = request.values.get('group_id')
	if new_user.groups.filter_by(gid = gid).count() > 0:
		flash('The user is already in the group!', 'error')
		return 'error'
	new_user.groups.append(UserGroup.query.filter_by(gid = gid).first())
	flash('Success!', 'success')
	return redirect(url_for('admin.userGroupDetail', gid = gid))
