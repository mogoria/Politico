"""Registers blueprints and creates different configurations
of your flask application"""
from flask import Flask
from instance.config import app_config
from app.api.v1.views import v1_bp
from app.api.v1.views.political_party_route import v1_bp as party_bp
from app.api.v1.views.political_office_route import v1_bp as office_bp
from app.api.v2.views.user import v2_bp as user_bp
from app.utils.helper import handle_bad_request, handle_not_found


def create_app(config_name='development'):
    """Returns flask app based on the configuration"""
    flask_app = Flask(__name__)
    flask_app.config.from_object(app_config[config_name])
    flask_app.config['JSON_SORT_KEYS'] = False
    flask_app.url_map.strict_slashes = False
    flask_app.register_error_handler(400, handle_bad_request)
    flask_app.register_error_handler(404, handle_not_found)
    flask_app.register_blueprint(v1_bp)
    flask_app.register_blueprint(party_bp)
    flask_app.register_blueprint(office_bp)
    flask_app.register_blueprint(user_bp)

    return flask_app
