from flask import render_template as render
from flask import abort
from flask_login import current_user, login_required
from functools import wraps
from datetime import datetime

def render_template(template, **kwargs):
	return render(template, current_user = current_user, **kwargs)

def admin_required(f):
	@login_required
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if not current_user.is_teacher:
			abort(403)
		return f(*args, **kwargs)
	return decorated_function

def str_time(dt):
	return dt.strftime('%Y-%m-%d %H:%M:%S')

from .main import main
from .user import user
from .api import api
from .task import task
from .admin import admin
from .problem import problem
from .submission import submission

BLUEPRINTS = (
	(main, ''),
	(user, '/user'),
	(api, '/api'),
	(problem, '/problem'),
	(task, '/task'),
	(admin, '/admin'),
	(submission, '/submission'),
)

def config_blueprint(app):
	for blueprint, prefix in BLUEPRINTS:
		app.register_blueprint(blueprint, url_prefix = prefix)
