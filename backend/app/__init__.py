from flask import Flask, render_template, session
from app.config import config
from app.extension import config_extension
from app.controller import config_blueprint
from datetime import timedelta

def config_api(app):
	@app.errorhandler(400)
	def page_bad_request(e):
		return render_template('error/400.html'), 400

	@app.errorhandler(403)
	def page_forbidden(e):
		return render_template('error/403.html'), 403

	@app.errorhandler(404)
	def page_not_found(e):
		return render_template('error/404.html'), 404

	@app.errorhandler(500)
	def internal_server_error(e):
		return render_template('error/500.html'), 500


def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config.get(config_name) or 'default')
	config.get(config_name).init_app(app)

	# Set to be in debug mode
	app.debug=True

	config_extension(app)
	config_blueprint(app)
	config_api(app)

	return app
