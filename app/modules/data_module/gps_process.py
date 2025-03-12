# ======================
# |       IMPORT       |
# ======================
import polars as pls
from zipfile import ZipFile
from os import makedirs
from geopy.distance import geodesic

"""
What does this do:
    - Unzip file:
        + Inside specific user's file
        + Must have time start (and time end?)
    - Process the data and combine it into 1 single file
    - 
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

def read_and_join(username: str, device: str, time_stamp: str) -> pls.LazyFrame:
    """
    
    Read file .zip and turn them into Polars Lazyframe.
    
    :username: Argument username, to get the directory the file is uploaded to.
    :device: Name of users' device, which is important for managing file.
    :timestamp: Timestamp of the .zip file.
    :return: A polars Lazyframe with columns ["time", "grade", "lat", "lon"].
    "time" is in ISO datetime format; "grade" datatype is float32; "lat" and
    "lon" are float64.

    """
    # Make path and file names
    dir_path = f".\\uploads\\{username}\\{time_stamp}"
    filenames = [device + " " + name for name in original_names]

    # Extract stuff
    makedirs(dir_path, exist_ok = True)
    with ZipFile(dir_path + ".zip", 'r') as zipObject: 
        zipObject.extractall(path = dir_path)

    # Linear
    linear_lazy = pls.scan_csv(source = join_path(dir_path, filenames[0]), has_header = False, skip_rows = 1) # Lazy scan, does not do anything (lol)
    linear_lazy = linear_lazy.rename({"column_1": "time", "column_2": "acc linear"})

    # Acce. Z
    acc_z_lazy = pls.scan_csv(join_path(dir_path, filenames[3]), has_header = False, skip_rows = 1)
    acc_z_lazy = acc_z_lazy.rename({"column_1": "time", "column_2": "acc z"})
    
    # Accelerometer Z has been tripped of G value, so there is no need for minusing 10
    grade_lazy = linear_lazy.join(acc_z_lazy, on = "time", how = "inner")
    grade_lazy = grade_lazy.with_columns(
            (pls.col("acc z") / (pls.col("acc linear")**2 - pls.col("acc z") ).sqrt() ).alias("grade")
    )

    # Process GPS data
    gps_lazy = pls.scan_csv(join_path(dir_path, filenames[4]), has_header = False, skip_rows = 1)
    gps_lazy = gps_lazy.with_columns([
        pls.col("column_2")
        .str.extract(r'"lat":([\d\.]+)')
        .cast(pls.Float64)
        .alias("lat"),
        pls.col("column_2")
        .str.extract(r'"lon":([\d\.]+)')
        .cast(pls.Float64)
        .alias("lon")
    ])
    gps_lazy = gps_lazy.select(["column_1", "lat", "lon"]) # Should not use slice for Polars
    gps_lazy = gps_lazy.rename({"column_1": "time"})

    # Merging
    res_df = grade_lazy.select(["time", "grade"]).join(gps_lazy, on = "time", how = "inner")

    res_df = res_df.with_columns(
        pls.col("time").str.strptime(pls.Datetime, format="%FT%H:%M:%S%.fZ", strict=False),
        pls.col("grade").cast(pls.Float32),
        pls.col("lat"),
        pls.col("lon"),
    )

    return res_df

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
            delta_t = temp_df[60, 0] - temp_df[0, 0]
        except:
            lat1, lon1 = float(temp_df[0, 2]), float(temp_df[0, 3])
            lat2, lon2 = float(temp_df[-1, 2]), float(temp_df[-1, 3])
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
    total_time = (df.select(["time"]).collect()[-1] - df.select(["time"]).collect()[0]).item().total_seconds()
    avg_velocity = (total_distance / total_time)
    return total_distance, total_time, avg_velocity




# ======================
# |   Visualization    |
# ======================
if __name__ == "__main__":
    # Parameters
    username = "UserB"
    device = "Pixel 8 Pro"
    time_stamp = "historic-data 2025 03 09"
    res_df = read_and_join(username, device, time_stamp)
    print(res_df.collect())
    
    # Import for plotting if necessary
    import matplotlib.pyplot as plt
    sample_num = len(res_df.collect())

    # Calculating means for plotting
    mean = res_df.select(["grade", "lat", "lon"]).collect().mean()

    # Calculate the distances
    distances, times, velocities = process_data(res_df)
    total_distance, total_time, avg_velocity = calculate_data(res_df, distances)

    # Plot data
    plt.figure(figsize = (15, 7))
    plt.subplot(2, 4, 1)
    plt.plot(res_df.collect()["grade"])
    plt.plot([mean["grade"] for _ in range(sample_num)])
    plt.title("Grade")

    plt.subplot(2, 4, 2)
    plt.plot(res_df.collect()["lat"])
    plt.plot([mean["lat"] for _ in range(sample_num)])
    plt.title("Latitude")

    plt.subplot(2, 4, 3)
    plt.plot(res_df.collect()["lon"])
    plt.plot([mean["lon"] for _ in range(sample_num)])
    plt.title("Longitude")
    
    plt.subplot(2, 4, 4)
    plt.plot(res_df.collect()["lat"], res_df.collect()["lon"], marker = '.')
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