from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_uploads import configure_uploads, patch_request_class, UploadSet, IMAGES
from flask_rq2 import RQ
# from flask_moment import Moment
# from flask_uploads import UploadSet,IMAGES,configure_uploads,patch_request_class
# from flask_debugtoolbar import DebugToolbarExtension

db = SQLAlchemy()
migrate = Migrate(db = db)
login_manager = LoginManager()
photos = UploadSet('photos',IMAGES)
rq = RQ()

# 初始化
def config_extension(app):
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
    rq.init_app(app)

    configure_uploads(app, photos)
    patch_request_class(app)

    login_manager.login_view = 'user.login'

    login_manager.session_protection = 'strong'
    login_manager.login_message = 'Please login first'
    login_manager.login_message_category = 'info'
    login_manager.needs_refresh_message = 'Session expired. Please re-login'
    login_manager.needs_refresh_message_category = 'info'
