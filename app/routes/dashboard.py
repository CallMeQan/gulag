from flask import Blueprint, render_template, jsonify
from flask import render_template, redirect, url_for, session, request
from flask_login import login_user, logout_user, login_required
from dotenv import load_dotenv
from os import getenv
import requests

from ..models import User
from ..extensions import db, login_manager
from ..modules.data_module import read_and_join, process_data, calculate_data

# Load env for Google Map
load_dotenv()

# Create instance
dashboard_bp = Blueprint('dashboard', __name__)

# User loader to get user object from the session when a request is made
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Main
@dashboard_bp.route("/map", methods = ["GET", "POST"])
def map():
    google_map_api_key = getenv("GOOGLE_MAP_API_KEY")
    get_iot_url = getenv("GET_IOT_URL")
    response = requests.get(get_iot_url)
    data = response.json()
    print(data["data"])
    print(data["user_id"])
    
    return render_template("dashboard/map.html", gg_api = google_map_api_key)