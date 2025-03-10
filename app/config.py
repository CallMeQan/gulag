from dotenv import load_dotenv
from os import getenv

load_dotenv()

class Config:
    SESSION_TYPE = "filesystem" # Read doc for more info
    secret_key = getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
