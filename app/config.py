from .env import SECRET_KEY, DATABASE_URI

class Config:
    SESSION_TYPE = "filesystem" # Read doc for more info
    secret_key = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False