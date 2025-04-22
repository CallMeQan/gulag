# ======================
# |       IMPORT       |
# ======================
import polars as pls
from geopy.distance import geodesic

# ======================
# |    FUNCTIONS       |
# ======================

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """

    Calculating distance between two Geographic points, using geopy library.
    Haversine function may be a choice, but in term of performance, using
    bult-in libraries is preferable.

    :lat1: Latitude of first point (Degree).
    :lon1: Longitude of first point (Degree).
    :lat2: Latitude of second point (Degree).
    :lon2: Longitude of second point (Degree).
    :return: Distance between two points (meters).
    """
    # A coordinate (lat, lon)
    point_a = (lat1, lon1)

    # B coordinate (lat, lon)
    point_b = (lat2, lon2)

    # Distance calculating, in meters
    distance = geodesic(point_a, point_b).meters
    return distance

def process_data(df: pls.LazyFrame, step: int = 2) -> tuple:
    """
    
    Process sensor GPS data to RAW kinematic data.

    :df: A dataframe with data "time", "lat" and "lon". "time" is of polars' ISO format.
    :return: A tuple (distances, times, velocities). The interval of data intake is 60s,
    with the last batch be reduced to appropriate time if needed (use batch to reduce
    noise and make the batch data more representative).

    """

    # Create an empty list to store distances
    distances = [0]
    velocities = [0]
    times = [0]
    
    # Loop over each pair of rows to calculate distances
    for i in range(0, df.select(pls.len()).item() - 1, step + 1):
        temp_df = df.slice(i, step + 1)
        lat1, lon1 = float(temp_df[0, 1]), float(temp_df[0, 2])
        lat2, lon2 = float(temp_df[-1, 1]), float(temp_df[-1, 2])
        distance = haversine(lat1, lon1, lat2, lon2)
        delta_t = temp_df[-1, 0] - temp_df[0, 0]
        
        # Convert to second
        delta_t = delta_t.total_seconds()

        # Prepare for Zero Division when time is 0 (just in case)
        try:
            distances.append(distance)
            velocities.append(distance / delta_t)
            times.append(delta_t)
        except ZeroDivisionError:
            distances.append(distance)
            velocities.append(distance)
            times.append(1)
    
    # Return a DataFrame with the calculated distances
    return distances, times, velocities

def calculate_data(df: pls.LazyFrame, distances: list):
    """

    Calculate the total distance, total time and average velocity from dataframe and
    distances, which are received from the function process_data() in this same module.
    The data is more MEANINGFUL and REPRESENTATIVE.

    :df: A dataframe with data "time", "lat" and "lon". "time" is of polars' ISO format.
    :distances: List of distances between points every interval time.
    :return: A tuple of kinematic data.


    """
    total_distance = sum(distances)
    total_time = (df.select(["created_at"])[-1] - df.select(["created_at"])[0]).item().total_seconds()
    try:
        avg_velocity = (total_distance / total_time)
    except:
        avg_velocity = total_distance
    return total_distance, total_time, avg_velocity