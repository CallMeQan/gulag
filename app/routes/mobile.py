from flask import Blueprint
from flask import session, request

from dotenv import load_dotenv

from ..models import User, Mobile_Session, Sensor_Data
from ..extensions import db, login_manager

# env get
load_dotenv()

mobile_bp = Blueprint('mobile', __name__)

# User loader to get user object from the session when a request is made
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@mobile_bp.route("/send_data", methods = ["GET", "POST"])
def send_data():
    """
    
    Get data from mobile and send it to the map in JSON format.

    {
        "hashed_timestamp": "e4dbc3acc15744bbac473655167aa1211da77da3796a703a9625e93c0a10eb09!",
        "latitude": 0,
        "longitude": 0,
        "time_start": [INT timestamp],
        "created_at": [ISO format - TIMESTAMPTZ],
    }
    
    """

    # if True:
    #     hashed_timestamp = "4e797e555f01f0dd367491846b7feeb06bc39192fc6b98361326b933e688a5c4"
    #     latitude = 0
    #     longitude = 1
    #     time_start = int(time.time())
    #     created_at = datetime.datetime.now(tz = datetime.timezone(datetime.timedelta(seconds=25200)))

    if request.method == "POST":
        # Get data from mobile
        hashed_timestamp = request.form["hashed_timestamp"]
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]
        time_start = request.form["time_start"]
        created_at = request.form["created_at"]

        # Get user_id and check token
        user_id = Mobile_Session.get_user_id_from_hash(hashed_timestamp)
        if user_id is None:
            return "Token is expired or does not exist! Please log in on Mobile again."

        row = {
            "user_id": 1,
            "start_time": time_start,
            "created_at": created_at,
            "location": f"Point({latitude} {longitude})"
        }

        row = Sensor_Data(**row)
        db.session.add(row)
        db.session.commit()
        
        return "Data sent successfully!"
    return "Send data here to show it in the map!"