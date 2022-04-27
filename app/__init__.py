from flask import Flask
from flask_bootstrap import Bootstrap

from config import config
import logging
bootstrap = Bootstrap()
logger = logging.getLogger()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    logging.basicConfig(filename='record.log', level=logging.DEBUG,
                        format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

    config[config_name].init_app(app)
    bootstrap.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
