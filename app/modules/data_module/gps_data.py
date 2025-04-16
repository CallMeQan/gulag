# ======================
# |       IMPORT       |
# ======================
import polars as pls
from zipfile import ZipFile
from os import makedirs
from geopy.distance import geodesic

"""

What does this do:
    - Get data input for **run_history** table:
        + Table **run_history** will have nullable fields (start, end, velocity, etc)
        + Query the table **sensor_data** database to get the GIS data from start_time to end_time.
        + Process data in **sensor_data** (multiple rows) and put into **run_history** (one row).

""" 



# ======================
# |  HYPERPARAMTERS    |
# ======================
original_names = ["Thing-Accelerometer_Linear.csv",
             "Thing-Accelerometer_X.csv",
             "Thing-Accelerometer_Y.csv",
             "Thing-Accelerometer_Z.csv",
             "Thing-Gps.csv"]



# ======================
# |    FUNCTIONS       |
# ======================

def join_path(path, file):
    return path + "\\" + file

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

def process_data(df: pls.LazyFrame) -> tuple:
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
    for i in range(0, df.select(pls.len()).collect().item() - 1, 60):
        temp_df = df.slice(i, 62).collect()
        try:
            lat1, lon1 = float(temp_df[0, 2]), float(temp_df[0, 3])
            lat2, lon2 = float(temp_df[60, 2]), float(temp_df[60, 3])
            distance = haversine(lat1, lon1, lat2, lon2)
            delta_t = temp_df[60, 1] - temp_df[0, 1]
        except:
            lat1, lon1 = float(temp_df[0, 2]), float(temp_df[0, 3])
            lat2, lon2 = float(temp_df[-1, 2]), float(temp_df[-1, 3])
            distance = haversine(lat1, lon1, lat2, lon2)
            delta_t = temp_df[-1, 1] - temp_df[0, 1]
        
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
    total_time = (df.select(["time"]).collect()[-1] - df.select(["time"]).collect()[0]).item().total_seconds()
    avg_velocity = (total_distance / total_time)
    return total_distance, total_time, avg_velocity




# ======================
# |   Visualization    |
# ======================
"""

To visualize, make directory: ./uploads/UserB/ and put the .zip file into there.
Then, just run this script.

"""
if __name__ == "__main__":
    # Parameters
    username = "Ceenen"
    user_id = 5
    device = "Pixel 8 Pro"
    time_stamp = "historic-data 2025 03 09"
    gps_lf, grade_lf = read_and_join(username, user_id, device, time_stamp, has_grade = True)
    print(gps_lf.collect())
    
    # Import for plotting if necessary
    import matplotlib.pyplot as plt
    sample_num = len(gps_lf.collect())

    # Calculating means for plotting
    mean_gps = gps_lf.select(["lat", "lon"]).collect().mean()
    mean_grade = grade_lf.select(["grade"]).collect().mean() 

    # Calculate the distances
    distances, times, velocities = process_data(gps_lf)
    total_distance, total_time, avg_velocity = calculate_data(gps_lf, distances)

    # Plot data
    plt.figure(figsize = (15, 7))
    plt.subplot(2, 4, 1)
    plt.plot(grade_lf.collect()["grade"])
    plt.plot([mean_grade["grade"] for _ in range(sample_num)])
    plt.title("Grade")

    plt.subplot(2, 4, 2)
    plt.plot(gps_lf.collect()["lat"])
    plt.plot([mean_gps["lat"] for _ in range(sample_num)])
    plt.title("Latitude")

    plt.subplot(2, 4, 3)
    plt.plot(gps_lf.collect()["lon"])
    plt.plot([mean_gps["lon"] for _ in range(sample_num)])
    plt.title("Longitude")
    
    plt.subplot(2, 4, 4)
    plt.plot(gps_lf.collect()["lat"], gps_lf.collect()["lon"], marker = '.')
    plt.title("Map")

    plt.subplot(2, 4, 5)
    plt.plot(distances, marker = ".", linestyle='-', color='b')
    plt.title("Distance running")

    plt.subplot(2, 4, 6)
    plt.plot(velocities, linestyle='-', color='b')
    plt.plot([avg_velocity for _ in range(len(velocities))], color='r')
    plt.title("Velocity running")

    plt.subplot(2, 4, 7)
    plt.plot(times, linestyle='-', color='b')
    plt.title("Delta time")

    # Adjust space
    plt.subplots_adjust(left=0.1, right=0.9, 
                        top=0.9, bottom=0.1, 
                        wspace=0.4, hspace=0.4)
    
    # Printing result
    print(f"Total time: {total_time}s")
    print(f"Total distance: {round(total_distance, 2)}m")
    print(f"Average velocity: {round(avg_velocity, 2)}m/s")

    # Show plot
    plt.show()