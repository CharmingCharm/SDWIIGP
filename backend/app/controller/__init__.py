from flask import render_template as render
from flask_login import current_user
def render_template(template, **kwargs):
    return render(template, current_user = current_user, **kwargs)

from .main import main
from .user import user
from .api import api
from .task import tasks
from .admin import admin
from .problem import problem

BLUEPRINTS = (
    (main, ''),
    (user, '/user'),
    (api, '/api'),
    (problem, '/problem'),
    (tasks, '/task'),
    (admin, '/admin'),
)

def config_blueprint(app):
    for blueprint, prefix in BLUEPRINTS:
        app.register_blueprint(blueprint, url_prefix = prefix)
