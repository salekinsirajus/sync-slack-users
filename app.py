# Syncs the user list
# Show the list of users
# Could be via a slash command or something else

from flask import Flask, jsonify, current_app

from models import create_db
from config import config_mapper


def create_app(config="development"):
    """Create an application instance

    config (str): "development"/"production"/"testing"
    """
    app = Flask(__name__)
    app.config.from_object(config_mapper.get(config)) 

    with app.app_context():
        db = create_db(app)
        import routes

    return app
