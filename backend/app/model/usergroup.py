from app.extension import db

class UserGroup(db.Model):
	__tablename__ = 'user_group'

	gid = db.Column(db.Integer, primary_key = True, autoincrement = True)
	group_name = db.Column(db.String(64), nullable = False)
	description = db.Column(db.Text, nullable = False, default = '')

	users = db.relationship(
		'User',
		secondary = 'user_in_group',
		backref = db.backref('groups', lazy = 'dynamic', cascade = 'all, delete', passive_deletes = True),
		lazy = 'dynamic',
		cascade = 'all, delete',
		passive_deletes = True
	)
