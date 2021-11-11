from flask import Flask, Blueprint

from app.api.routes import BLUEPRINT
from app.instance.config import APP_CONFIG
from app.db_con import create_tables, super_user, destroy_tables


def create_app(config_name):
    """
    The create_app function wraps the creation of a new Flask object,
    and returns it after it's loaded up with configuration settings using
    app.config
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(APP_CONFIG[config_name])
    app.url_map.strict_slashes = False

    # destroy_tables()
    create_tables()
    super_user()

    app.register_blueprint(BLUEPRINT)

    return app