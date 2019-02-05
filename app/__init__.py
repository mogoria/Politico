"""Registers blueprints and creates different configurations
of your flask application"""
from flask import Flask
from instance.config import app_config
from app.api.v1.views import v1_bp


def create_app(config_name):
    """Returns flask app based on the configuration"""
    flask_app = Flask(__name__)
    flask_app.config.from_object(app_config[config_name])
    flask_app.register_blueprint(v1_bp)

    return flask_app
