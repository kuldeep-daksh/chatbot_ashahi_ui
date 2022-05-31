import os
import json

basedir = os.path.abspath(os.path.dirname(__file__))

with open("/etc/config.json") as config_file:
    config = json.load(config_file)
    print(config.get('SECRET_KEY'))


class Config:
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SECRET_KEY = config.get('SECRET_KEY') or 'hard to guess string'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    PORT = 5000
    pass


class TestingConfig(Config):
    TESTING = True
    pass


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}


class UnixConfig(DevelopmentConfig):

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to syslog
        import logging
        from logging.handlers import SysLogHandler

        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.info)
        app.logger.addHandler(syslog_handler)
