import polars as pls
from zipfile import ZipFile
from os.path import exists
from os import makedirs
import json

"""
What does this do:
    - Unzip file:
        + Inside specific user's file
        + Must have time start (and time end?)
    - Process the data and combine it into 1 single file
    - 
""" 

# Hyperparameter
original_names = ["Thing-Accelerometer_Linear.csv",
             "Thing-Accelerometer_X.csv",
             "Thing-Accelerometer_Y.csv",
             "Thing-Accelerometer_Z.csv",
             "Thing-Gps.csv"]

# Local util function
def join_path(path, file):
    return path + "\\" + file

def read_and_join(username: str, device: str, time_stamp: str) -> pls.LazyFrame:
    # Make path and file names
    dir_path = f".\\data\\{username}\\{time_stamp}"
    filenames = [device + " " + name for name in original_names]

    # Extract stuff
    makedirs(dir_path, exist_ok = True)
    with ZipFile(dir_path + ".zip", 'r') as zipObject: 
        zipObject.extractall(path = f".\\data\\{username}\\{time_stamp}")

    # Linear
    linear_lazy = pls.scan_csv(source = join_path(dir_path, filenames[0]), has_header = False, skip_rows = 1) # Lazy scan, does not do anything (lol)
    linear_lazy = linear_lazy.rename({"column_1": "time", "column_2": "lin. accel."})

    # Acce. X
    acc_x_lazy = pls.scan_csv(join_path(dir_path, filenames[1]), has_header = False, skip_rows = 1)
    acc_x_lazy = acc_x_lazy.rename({"column_1": "time", "column_2": "acc x"})

    # Acce. Y
    acc_y_lazy = pls.scan_csv(join_path(dir_path, filenames[2]), has_header = False, skip_rows = 1)
    acc_y_lazy = acc_y_lazy.rename({"column_1": "time", "column_2": "acc y"})

    # Acce. Z
    acc_z_lazy = pls.scan_csv(join_path(dir_path, filenames[3]), has_header = False, skip_rows = 1)
    acc_z_lazy = acc_z_lazy.rename({"column_1": "time", "column_2": "acc z"})

    # GPS
    gps_lazy = pls.scan_csv(r".\data\UserA\2025\Pixel 8 Pro Thing-Gps.csv", has_header = False, skip_rows = 1)
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
    res_df = linear_lazy.join(acc_x_lazy, on = "time", how = "inner")
    res_df = res_df.join(acc_y_lazy, on = "time", how = "inner")
    res_df = res_df.join(acc_z_lazy, on = "time", how = "inner")
    res_df = res_df.join(gps_lazy, on = "time", how = "inner")

    res_df = res_df.with_columns(
        pls.col("time"),
        pls.col("lin. accel.").cast(pls.Float32),
        pls.col("acc x").cast(pls.Float32),
        pls.col("acc y").cast(pls.Float32),
        pls.col("acc z").cast(pls.Float32),
        pls.col("lat"),
        pls.col("lon"),
    )

    return res_df

if __name__ == "__main__":
    # Parameters
    username = "UserB"
    device = "Pixel 8 Pro"
    time_stamp = "historic-data-20250227T082337Z"
    res_df = read_and_join(username, device, time_stamp)
    
    print(res_df.collect())
    import matplotlib.pyplot as plt
    sample_num = len(res_df.collect())

    # Linear Accelerometer
    mean = res_df.collect().mean()

    plt.figure(figsize = (7, 7))
    plt.subplot(2, 2, 1)
    plt.plot(res_df.collect()["lin. accel."])
    plt.plot([mean["lin. accel."] for _ in range(sample_num)])
    plt.title("Linear Accelerometer")

    plt.subplot(2, 2, 2)
    plt.plot(res_df.collect()["acc x"])
    plt.plot([mean["acc x"] for _ in range(sample_num)])
    plt.title("Accelerometer on X-axis")

    plt.subplot(2, 2, 3)
    plt.plot(res_df.collect()["acc y"])
    plt.plot([mean["acc y"] for _ in range(sample_num)])
    plt.title("Accelerometer on Y-axis")
    
    plt.subplot(2, 2, 4)
    plt.plot(res_df.collect()["acc z"])
    plt.plot([mean["acc z"] for _ in range(sample_num)])
    plt.title("Accelerometer on Z-axis")

    # Adjust space
    plt.subplots_adjust(left=0.1, right=0.9, 
                        top=0.9, bottom=0.1, 
                        wspace=0.4, hspace=0.4)
    plt.show()