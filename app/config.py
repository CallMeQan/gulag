import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///gulag.db'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')