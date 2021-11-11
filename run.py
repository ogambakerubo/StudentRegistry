"""Run docstring"""

import os
from flask import jsonify, make_response


from app import create_app


config_name = os.getenv("FLASK_CONFIG") or "default"

APP = create_app(config_name)


@APP.errorhandler(404)
def page_not_found(e):
    """error handler default method for error 404"""

    return make_response(
        jsonify(
            {
                "message": "Oops! Something went wrong. Please check your url or input type.",
                "status": 404,
            }
        ),
        404,
    )
