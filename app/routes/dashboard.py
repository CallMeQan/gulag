from os import getenv
from flask import Blueprint, render_template
from flask import render_template, session
from ..models import User
from ..extensions import login_manager


# Create instance
dashboard_bp = Blueprint('dashboard', __name__)

# User loader to get user object from the session when a request is made
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# Main
@dashboard_bp.route("/map", methods = ["GET", "POST"])
def map():
    user_id = session["user"]["user_id"]
    user = User.query.get(user_id)
    # replace with how you track session
    # Get map api key and socketio url
    return render_template("dashboard/map.html", socketio_url = getenv("SOCKETIO_URL"), map_key = getenv("MAP_API_KEY"),username = user.username) 