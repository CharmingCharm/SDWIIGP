from .user import User
from .problem import Problem
from .submission import Submission
from .usergroup import UserGroup
from .task import Task
from .tag import Tag
from .test import Test
from .testset import TestSet
from app.extension import db

UserInGroup = db.Table(
    'user_in_group',
    db.Column('uid', db.Integer, db.ForeignKey('user.uid'), primary_key = True),
    db.Column('gid', db.Integer, db.ForeignKey('user_group.gid'), primary_key = True)
)

TagOfProblem = db.Table(
    'tag_of_problem',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.tag_id'), primary_key = True),
    db.Column('pid', db.Integer, db.ForeignKey('problem.pid'), primary_key = True)
)

TestInTestSet = db.Table(
    'test_in_testset',
    db.Column('testset_id', db.Integer, db.ForeignKey('testset.testset_id'), primary_key = True),
    db.Column('test_id', db.Integer, db.ForeignKey('test.test_id'), primary_key = True)
)

ProblemInTask = db.Table(
    'problem_in_task',
    db.Column('task_id', db.Integer, db.ForeignKey('task.task_id'), primary_key = True),
    db.Column('pid', db.Integer, db.ForeignKey('problem.pid'), primary_key = True)
)
