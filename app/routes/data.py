from flask import Blueprint, jsonify
from flask import redirect, url_for, session, request
import polars as pls
from dotenv import load_dotenv
from os import getenv

from ..models import User, Sensor_Data
from ..extensions import db, login_manager
from ..modules.data_module import read_and_join, process_data, calculate_data

# Create instance
data_bp = Blueprint('data', __name__)

# User loader to get user object from the session when a request is made
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Fetch data
@data_bp.route("/data_fetch", methods = ["GET", "POST"])
def data_fetch():
    if request.method == "GET":

        # Load .env
        load_dotenv()

        # Get user info from session
        user_info = session.get("user")
        if not user_info:
            return redirect(url_for("auth.login"))

        # Input
        DATABASE_URI = getenv("DATABASE_URI")
        username = user_info["username"]
        user_id = user_info["user_id"]
        
        # Mock input
        if __name__ == "__main__":
            username = "Ceenen"
            user_id = 5
        device = "Pixel 8 Pro"
        time_stamp = "historic-data 2025 03 09"

        # Process file
        gps_lf, grade_lf = read_and_join(username, user_id, device, time_stamp, has_grade = True)
        gps_lf = gps_lf.with_columns(
            (pls.lit("POINT(") + pls.col("lon").cast(pls.Utf8) + pls.lit(" ") + pls.col("lat").cast(pls.Utf8) + pls.lit(")")).alias("location")
        )
        
        gps_lf = gps_lf.select(["user_id", "time", "location"])
        
        # Input into database
        gps_lf.collect().write_database(table_name = "sensor_data", connection = DATABASE_URI, if_table_exists = "append")

        return jsonify({"email": "104240073@gmail.com", "user_id": 5, "username": "Ceenen"})
    return redirect(url_for("home.index"))