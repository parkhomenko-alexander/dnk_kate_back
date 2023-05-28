from datetime import timedelta

class Config():
    DEBUG: bool = True
    SECRET_KEY: str = 'key'
    UPLOAD_FOLDER: str = '/static/upload'
    STATIC_URL_PATH: str ='/static'
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = True
    SQLALCHEMY_DATABASE_URI: str = 'sqlite:///database.db'
    PROD_IP = 'localhost:5000'
    JSON_AS_ASCII = False