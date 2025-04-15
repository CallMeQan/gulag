from dotenv import load_dotenv
from os import getenv

load_dotenv()

# URI and web
DATABASE_URI = getenv("DATABASE_URI")
SESSION_TYPE = "filesystem"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# KEYS
SECRET_KEY = getenv("SECRET_KEY")
MAP_KEY = getenv("MAP_KEY")
EMAIL_PASSWORD = getenv("EMAIL_PASSWORD")

# SocketIO paths
SOCKETIO_URL = getenv("SOCKETIO_URL")
SOCKETIO_PATH = "/" + SOCKETIO_URL.split("/")[-1] # Get "/data_room" from "http://localhost:5000/data_room"