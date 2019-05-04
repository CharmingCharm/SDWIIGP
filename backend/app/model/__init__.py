from .user import User
from .problem import Problem
from .submission import Submission
from .usergroup import UserGroup
from app.extension import db

UserInGroup = db.Table(
	'UserInGroup',
	db.Column('uid', db.Integer, db.ForeignKey('User.uid'), primary_key = True),
	db.Column('gid', db.Integer, db.ForeignKey('UserGroup.gid'), primary_key = True)
)
