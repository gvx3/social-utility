from flask import Flask
from app.api import bp as api_bp


def create_app():
    app = Flask("random_name")

    app.register_blueprint(api_bp, url_prefix='/api')
    return app
