from flask import Flask, Blueprint

from app.api.routes import BLUEPRINT
from app.instance.config import APP_CONFIG
from app.commands import commands


def create_app(config_name):
    """
    The create_app function wraps the creation of a new Flask object,
    and returns it after it's loaded up with configuration settings using
    app.config
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(APP_CONFIG[config_name])
    app.url_map.strict_slashes = False

    app.register_blueprint(BLUEPRINT)
    app.register_blueprint(commands)

    return app
