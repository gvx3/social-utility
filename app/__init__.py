from flask import Flask
from app.api import bp as api_bp
from config import Config


def create_app(config=Config):
    app = Flask("random_name")
    app.config.from_object(config)
    app.secret_key = Config.SECRET_KEY
    app.register_blueprint(api_bp, url_prefix='/api')
    return app
