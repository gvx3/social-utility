import os
from dotenv import load_dotenv

parent_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(parent_dir, '.env'))


class Config:

    YT_API_KEY = os.environ.get('YT_API_KEY')
    CLIENT_CREDENTIAL = os.path.join(parent_dir, 'client_secret_700492713144-fdog9odfso78ft33a35e6h0jsi72h087.json')
