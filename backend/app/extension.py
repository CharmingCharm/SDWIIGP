from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_uploads import configure_uploads, patch_request_class, UploadSet, IMAGES
# from flask_moment import Moment
# from flask_uploads import UploadSet,IMAGES,configure_uploads,patch_request_class
# from flask_debugtoolbar import DebugToolbarExtension

db = SQLAlchemy()
migrate = Migrate(db = db)
# moment = Moment()
login_manager = LoginManager()
# 上传
photos = UploadSet('photos',IMAGES)

# 初始化
def config_extension(app):
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app)

    # 一些图片上传的配置
    configure_uploads(app, photos)
    # 设置上传文件大小
    patch_request_class(app)

    # 指定登录的端点
    login_manager.login_view = 'user.login'

    # 需要登录时的提示信息
    login_manager.login_message = 'Please login first'
    login_manager.login_message_category = 'info'
    login_manager.session_protection = 'strong'
