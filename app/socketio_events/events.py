from flask import session
from flask_socketio import join_room, leave_room

from .. import socketio

from ..models import Mobile_Session
from ..params import SOCKETIO_PATH

# Join socketio room
@socketio.on("joined", namespace = SOCKETIO_PATH) # SOCKETIO_PATH can be "/data_room"
def joined(message):
    # Take information from session
    user_id = session["user"]["user_id"]
    print(user_id)

    # If user is in session (web Flask) then join room with ID being user_id
    if user_id:
        join_room(user_id)
        print("User (map) has joined room!")
    else:
        hashed_timestamp = message["hashed_timestamp"] # take token from message
        user_id = Mobile_Session.get_user_id_from_hash(hashed_timestamp = hashed_timestamp)
        join_room(user_id)
        print("Mobile has joined room!")

# @socketio.on("send_server_data", namespace = "/data_room")
# def send_data(mes2server):
#     """
#     Send data from client mobile devices to server, through mobile.send_data route.
#     :mes2server: {
#                 "user_id": user_id,
#                 "latitude": latitude,
#                 "longitude": longitude
#                 }
#     """

#     print(f"\n\n\n{mes2server}\n\n\n")
#     user_id = mes2server["user_id"]
#     latitude = mes2server["latitude"]
#     longitude = mes2server["longitude"]

#     # TODO: Check hashed_timestamp in mobile_auth table DB
#     print(f"\n\n\n{user_id, latitude, longitude}\n\n\n")
#     emit("updated_info_on_room",
#         {
#             'latitude': latitude,
#             'longitude': longitude
#         },
#         to = user_id,
#         namespace = "/data_room")