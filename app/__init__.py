"""Registers blueprints and creates different configurations
of your flask application"""
from flask import Flask
from instance.config import app_config
from app.api.v1.views import v1_bp
from app.api.v1.views.political_party_route import v1_bp as political_party_bp

flask_app = Flask(__name__)
def create_app(config_name):
    """Returns flask app based on the configuration"""
    flask_app.config.from_object(app_config[config_name])
    flask_app.register_blueprint(v1_bp)
    flask_app.register_blueprint(political_party_bp)

    return flask_app
