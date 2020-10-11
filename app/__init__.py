import logging
import os

import flask
from flask import Flask

from app import extensions


def _init_logging(app: Flask) -> None:
    log_basename = os.path.basename(app.config.get('ROOT_DIRECTORY'))
    log_dirname = '%s/app' % app.config.get('LOG_DIRECTORY')
    log_filename = f'{log_dirname}/{log_basename}.log'

    config = {
        'format': '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        'level': logging.DEBUG,
        'filename': log_filename,
    }

    logging.basicConfig(**config)


def _init_extensions(app: Flask) -> None:
    extensions.init_app(app)


def create_app(config: str) -> Flask:
    app = flask.Flask(__name__)
    app.config.from_object(config)
    # TODO: add middleware for checking Content-Type requests

    _init_logging(app)
    _init_extensions(app)

    return app
