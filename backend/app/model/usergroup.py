from app.extension import db
from flask_login import UserMixin

class UserGroup(UserMixin, db.Model):
	__tablename__ = 'UserGroup'

	gid = db.Column(db.Integer, primary_key = True, autoincrement = True)
	group_name = db.Column(db.String(64), nullable = False)
	description = db.Column(db.Text, nullable = False, default = '')

	users = db.relationship(
		'User',
		secondary = 'UserInGroup',
		backref = db.backref('groups', lazy = 'dynamic'),
		lazy = 'dynamic'
	)
