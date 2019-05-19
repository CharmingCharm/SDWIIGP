import os
from dotenv import load_dotenv
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, 'private.env'))

# 定义配置基类
class Config:
    # 密钥
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # 数据库配置
    # 数据库迁移追踪
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 自动提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # 邮件配置
    # MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.qq.com'
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '1825514258@qq.com'
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'lhyjeyaywqfdegeg'
    # MAIL_USE_SSL = True
    # MAIL_SUPPRESS_SEND = False
    # MAIL_PORT = 465
    # MAIL_USE_TLS = False

    # 文件上传相关设置
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
    UPLOADED_PHOTOS_DEST = os.path.join(BASE_DIR, 'static/avatars')

    RQ_REDIS_URL = 'redis://localhost:6379/0'
    JUDGER_DIR = os.path.join(BASE_DIR, 'judger_dir')

    # 额外的初始化操作
    @staticmethod
    def init_app(app):
        pass

# 开发环境配置
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_DEVELOP')

# 生产环境
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_PRODUCTION')

# 生成一个字典，用来根据字符串找到对应的配置类。
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
