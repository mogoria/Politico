"""Registers blueprints and creates different configurations
of your flask application"""
from flask import Flask
from instance.config import app_config
from app.api.v1.views import v1_bp
from app.api.v1.views.political_party_route import v1_bp as political_party_bp


def create_app(config_name='development'):
    """Returns flask app based on the configuration"""
    flask_app = Flask(__name__)
    flask_app.config.from_object(app_config[config_name])
    flask_app.url_map.strict_slashes = False
    flask_app.register_blueprint(v1_bp)
    flask_app.register_blueprint(political_party_bp)

    return flask_app
