from os import getenv
from flask import session
from flask_socketio import join_room, emit

import polars as pls

from .. import socketio

from ..modules.data_module import process_data, calculate_data

@socketio.on("joined", namespace = getenv("SOCKETIO_PATH")) # SOCKETIO_PATH can be "/data_room"
def joined(message):
    """
    Join a room based on the user_id or hashed timestamp.
    """
    user_id = session["user"]["user_id"]
    print(user_id)

    if user_id:
        join_room(user_id)
        print("User (map) has joined room!")
    else:
        print("Something is wrong! User cannot join!")
    print("Joined successfully")

@socketio.on("interval_signal_to_server", namespace = getenv("SOCKETIO_PATH"))
def interval_signal_to_server(message):
    """
    Get signal from user every interval of 10 rows.

    {"time_start": time_start}
    """
    user_id = session["user"]["user_id"]
    time_start = message["time_start"]
    
    # TODO: Add a database for weight and height of people => get weight and stride length from that
    weight = 65 # kg
    stride_length = 0.6 # meter

    run_session_query = f"SELECT sensor_data.created_at, ST_X(sensor_data.location) AS latitude, ST_Y(sensor_data.location) AS longitude FROM sensor_data WHERE sensor_data.user_id = {user_id} AND sensor_data.start_time = {time_start};"
    run_session_query = f"SELECT sensor_data.created_at, ST_X(sensor_data.location) AS latitude, ST_Y(sensor_data.location) AS longitude FROM sensor_data WHERE sensor_data.start_time = {time_start};"
    lz_frame = pls.read_database_uri(query = run_session_query, uri = getenv("DATABASE_URI"), engine="connectorx")

    # Get kinematic data
    distances, times, velocities = process_data(lz_frame)
    total_distance, total_time, avg_velocity = calculate_data(lz_frame, distances = distances)
    
    # Get MET parameter for Calorie
    if avg_velocity < 3:
        MET = 2.5
    elif avg_velocity < 4:
        MET = 3.2
    elif avg_velocity < 5:
        MET = 4
    elif avg_velocity < 6:
        MET = 4.6
    elif avg_velocity < 7:
        MET = 7.5
    elif avg_velocity < 8:
        MET = 8.5
    elif avg_velocity < 9:
        MET = 9.75
    elif avg_velocity < 10:
        MET = 11.25
    elif avg_velocity < 12:
        MET = 13
    elif avg_velocity < 14:
        MET = 15
    else:
        MET = 16

    # Calculating calorie
    calorie = MET * weight * total_time / 3600 # MET * weight(kg) * time(hour)

    # Converting and rounding
    calorie = round(calorie, 1)
    step_num = int(total_distance / stride_length) # steps
    total_distance = round(total_distance / 1000, 1) # km
    total_time = round(total_time, 1) # seconds
    pace = round(total_time / total_distance / 3600, 1)

    emit("update_kinematic",
        {
            "calorie": calorie,
            "step": step_num,
            "total_distance": total_distance,
            "total_time": total_time,
            "pace": pace
        },
        to = user_id,
        namespace = getenv("SOCKETIO_PATH"))