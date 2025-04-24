from os import getenv
from flask import Blueprint, jsonify, request

from flask_socketio import emit

from ..models import Mobile_Session, Sensor_Data
from ..extensions import db

mobile_bp = Blueprint('mobile', __name__)

@mobile_bp.route("/send_mobile_data", methods = ["GET", "POST"])
def send_mobile_data():
    """
    
    Get data from mobile and send it to the map in JSON format.

    POST method will send these:
    {
        "hashed_timestamp": "e4dbc3acc15744bbac473655167aa1211da77da3796a703a9625e93c0a10eb09!",
        "latitude": 0,
        "longitude": 0,
        "time_start": [INT timestamp],
        "created_at": [ISO format - TIMESTAMPTZ],
    }
    
    """

    if request.method == "POST":
        # Get data from mobile
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received!"}), 400

        hashed_timestamp = data.get('hashed_timestamp')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        time_start = data.get('time_start')
        created_at = data.get('created_at')

        # Get user_id and check token
        user_id = Mobile_Session.get_user_id_from_hash(hashed_timestamp)
        if user_id is None:
            return "Token is expired or does not exist! Please log in on Mobile again."

        # Commit row to data base
        row = {
            "user_id": user_id,
            "start_time": time_start,
            "created_at": created_at,
            "location": f"Point({latitude} {longitude})"
        }
        row = Sensor_Data(**row)
        db.session.add(row)
        db.session.commit()
        
        # Add Socketio
        emit("send_server_data",
             {
                "time_start": time_start,
                "latitude": latitude,
                "longitude": longitude
             },
             to = user_id,
             namespace = getenv("SOCKETIO_PATH"))
        res = jsonify("Data sent to the map!")
        res.headers["Access-Control-Allow-Origin"] = "*"
        return res, 200
    return jsonify("Send data here to show it in the map!"), 400