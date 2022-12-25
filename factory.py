from flask import Flask
from auth import app as auth_api
from crawler import app as crawler_api


def create_app():
    app = Flask(__name__)
    # we can set endpoint prefix by using blueprint
    app.register_blueprint(auth_api)
    app.register_blueprint(crawler_api)
    return app
