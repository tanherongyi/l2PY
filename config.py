import os
# 定义项目根目录
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'this my blog app golb ym siht'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    GITHUB_AUTHORIZE_URL = 'https://github.com/login/oauth/authorize'
    GITHUB_CLIENT_ID = 'dd76d0ffa77c39b29d70'
    GITHUB_CLIENT_SECRET = 'a7029e8bda916de767caadf03e85d320f9f26d0f'
    GITHUB_CLIENT_ID1 = '8ed071840ddef477baef'
    GITHUB_CLIENT_SECRET1 = 'be12c9dcdb56b0213456b5dae4c16bf13e5d20df'
    GITHUB_CLIENT_ID2 = '037a57bccbc6fcbe0f90'
    GITHUB_CLIENT_SECRET2 = '093d1913f01d27bb5f17937d3e2829caa8e87903'
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
    QINIU_ACCESS_KEY = 'yFZl4V8ZlCg8j4-EDV_KLfx1JEi8mMTcvfQnGfBo'
    QINIU_SECRET_KEY = 'wooC5JykXfoKIEhYdxQYsNV1FjZ2EFttes_NR83l'
    #存放索引的文件夹,Flask-WhooshAlchemyPlus是只依赖于flask,whoosh还有sqlalchemy的，所以sqlalchemy支持的数据库这个插件都支持
    WHOOSH_BASE = os.path.abspath('./whoosh_index')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    # 连接mysql数据库，SQLAlchemy连接数据库的一般格式为database_type+driver://user:password@sql_server_ip:port/database_name
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:8114193@localhost/flaskblogdb'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:ms8114193@120.79.182.246:3306/blogdb'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}