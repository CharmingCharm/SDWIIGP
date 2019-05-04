from .main import main
from .auth import auth
from .api import api

BLUEPRINTS = (
    (main, ''),
    (auth, '/auth'),
    (api, '/api')
)

def config_blueprint(app):
    for blueprint, prefix in BLUEPRINTS:
        app.register_blueprint(blueprint, url_prefix = prefix)
