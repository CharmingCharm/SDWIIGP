from .user import User
from .problem import Problem
from .submission import Submission
from .usergroup import UserGroup
from app.extension import db

UserInGroup = db.Table(
	'user_in_group',
	db.Column('uid', db.Integer, db.ForeignKey('user.uid'), primary_key = True),
	db.Column('gid', db.Integer, db.ForeignKey('user_group.gid'), primary_key = True)
)
