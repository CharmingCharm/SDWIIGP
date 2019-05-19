from flask import Flask, render_template
from app.config import config
from app.extension import config_extension
from app.controller import config_blueprint

def config_errorhandler(app):
    '''
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error/404.html', e = e)
    '''

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name) or 'default')
    config.get(config_name).init_app(app)

    app.debug=True

    config_extension(app)
    config_blueprint(app)
    config_errorhandler(app)

    return app
