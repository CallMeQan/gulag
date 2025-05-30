from os import getenv
from dotenv import load_dotenv
load_dotenv()

class Config:
    SESSION_TYPE = "filesystem" # Read doc for more info
    SECRET_KEY = getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False