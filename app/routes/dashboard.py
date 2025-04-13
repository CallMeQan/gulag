from flask import Blueprint, render_template, jsonify
from flask import render_template, redirect, url_for, session, request
from flask_login import login_user, logout_user, login_required

from dotenv import load_dotenv
from os import getenv
import requests
from json import dumps, loads

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
    # get_iot_url = getenv("GET_IOT_URL")
    # response = requests.get(get_iot_url)
    # data = response.json()
    # print(data["data"])
    # print(data["user_id"])
    
    # Current position (mock data)
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "name": "Running Route",
                    "type": "Loop Run"
                },
                "geometry": {
                "type": "LineString",
                    "coordinates": [
                    [106.612543, 11.107656],
                    [106.612943, 11.107656],
                    [106.613543, 11.107656],
                    [106.614543, 11.107656],
                    [106.615143, 11.107256],
                    [106.616143, 11.107456],
                    [106.617543, 11.107356],
                    [106.614543, 11.107256],
                    [106.614243, 11.107156],
                    [106.613243, 11.107056]
                ]
            }
        }
    ]
    }
    current_pos = [11.107656, 106.612543]

    current_pos = dumps(current_pos)
    loaded_pos = loads(current_pos)

    # Parse dictionary into json-string
    geojson = dumps(geojson)
    loaded_geojson = loads(geojson)

    # Get map api key
    map_key = getenv("MAP_KEY")
    return render_template("dashboard/map.html", map_key = map_key, current_pos = loaded_pos, geojson = loaded_geojson)