from app import create_app
from instance.config import app_config


flask_app = create_app('development')

@flask_app.route("/")
def say_hello():
    return "Hello world"

if __name__ == '__main__':
    flask_app.run()