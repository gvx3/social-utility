from flask import Flask
from app.api import bp as api_bp
from config import Config
from app.extensions import db, ma


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    ma.init_app(app, db)
    app.secret_key = Config.SECRET_KEY
    app.register_blueprint(api_bp, url_prefix='/api')
    return app
