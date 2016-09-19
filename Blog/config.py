import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIT_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIT_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass
class DevelopementConfig(Config):
    DEBUG = True
    MAIT_SERVER = 'smtp.outlook.com'
    MAIT_PORT = 587
    MAIT_USE_TLS = True
    MAIT_USERNAME = os.environ.get('MAIT_USERNAME')
    MAIT_PASSWORD = os.environ.get('MAIT_PASSWORD')
    SQLALCHMY_COMMIT_ON_TEARDOWN = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,'data-dev.sqlite')
class TestingConfig(Config):
    TESTING = True
    SQLALCHMY_COMMIT_ON_TEARDOWN = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,'data-test.sqlite')
class ProductionConfig(Config):
    SQLALCHMY_COMMIT_ON_TEARDOWN = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,'data.sqlite')
config = {
    'development':DevelopementConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    'default':DevelopementConfig
}