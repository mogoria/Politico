"""main file to run the flask application"""
from app import create_app


flask_app = create_app(config_name='development')


if __name__ == '__main__':
    flask_app.run()
