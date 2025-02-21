import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///gulag.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False