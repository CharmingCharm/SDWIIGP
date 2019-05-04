from .main import main
from .auth import auth
from .api import api
from .problem import problem

BLUEPRINTS = (
    (main, ''),
    (auth, '/auth'),
    (api, '/api'),
    (problem, '/problem'),
)

def config_blueprint(app):
    for blueprint, prefix in BLUEPRINTS:
        app.register_blueprint(blueprint, url_prefix = prefix)
