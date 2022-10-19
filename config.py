import os
from dotenv import load_dotenv

parent_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(parent_dir, '.env'))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    YT_API_KEY = os.environ.get('YT_API_KEY')
    CLIENT_CREDENTIAL = os.path.join(parent_dir, 'client_secret_700492713144-fdog9odfso78ft33a35e6h0jsi72h087.json')
    OAUTHLIB_INSECURE_TRANSPORT = os.environ.get('OAUTHLIB_INSECURE_TRANSPORT')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    DB_HOST = os.environ.get('DB_HOST')
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    DB_PASS = os.environ.get('DB_PASS')
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
