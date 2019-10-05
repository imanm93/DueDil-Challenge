import os

from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from . import config as Config
from .common import constants as COMMON_CONSTANTS
from .api import user

# For import
__all__ = ['create_app']

DEFAULT_BLUEPRINTS = [
    user
]

def create_app(config=None, app_name=None, blueprints=None):
    """ Create a Flask app """

    if app_name is None:
        app_name = Config.DefaultConfig.PROJECT

    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(app_name, instance_path=COMMON_CONSTANTS.INSTANCE_FOLDER_PATH, instance_relative_config=True)
    configure_app(app, config)
    configure_blueprints(app, blueprints)
    configure_error_handlers(app)

    return app


def configure_app(app, config=None):
    """ Configure app for dev/prod/testing/staging """

    app.config.from_object(Config.DefaultConfig)

    if config:
        application_mode = config
    else:
        application_mode = os.getenv('APPLICATION_MODE', 'DEV')
    app.config.from_object(Config.get_config(application_mode))


def configure_blueprints(app, blueprints):
    # Register blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_error_handlers(app):

    @app.errorhandler(404)
    def not_found_page(error):
        return "404 - API endpoint not found"

    @app.errorhandler(500)
    def server_error_page(error):
        return "500 - Internal server error"
