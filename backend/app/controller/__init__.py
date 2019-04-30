from .main import main
from .auth import auth

BLUEPRINTS = (
    (main, ''),
    (auth, '/auth')
)

def config_blueprint(app):
    for blueprint, prefix in BLUEPRINTS:
        app.register_blueprint(blueprint, url_prefix = prefix)
