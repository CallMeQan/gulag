import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///gulag.db'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    MAX_CONTENT_LENGTH = 1024 * 1024 * 1024 # 1GB
    SQLALCHEMY_TRACK_MODIFICATIONS = True