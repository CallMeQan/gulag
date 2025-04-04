import polars as pls
from zipfile import ZipFile
from os import makedirs
from pykalman import KalmanFilter
import scipy.signal as signal

"""

- Some insights into Accel. Data, which we may not use.
- Accelerometer data has so many error in it, so it is
not feasible to use integral to calculate velocity.
- An alternative which has been done is using geo-info
in place of accelerometer data. This is very successful
in the file file_manip.py
    
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

def read_and_join(username: str, device: str, time_stamp: str, filtered: bool) -> pls.LazyFrame:
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

    # Acce. X
    acc_x_lazy = pls.scan_csv(join_path(dir_path, filenames[1]), has_header = False, skip_rows = 1)
    acc_x_lazy = acc_x_lazy.rename({"column_1": "time", "column_2": "acc x"})
    ax = acc_x_lazy.collect()["acc x"].to_numpy()
    filtered_ax = apply_highpass_filter(ax)
    acc_x_lazy = acc_x_lazy.with_columns(
        pls.Series("ax", filtered_ax)
    )

    # Acce. Y
    acc_y_lazy = pls.scan_csv(join_path(dir_path, filenames[2]), has_header = False, skip_rows = 1)
    acc_y_lazy = acc_y_lazy.rename({"column_1": "time", "column_2": "acc y"})
    ay = acc_y_lazy.collect()["acc y"].to_numpy()
    filtered_ay = apply_highpass_filter(ay)
    acc_y_lazy = acc_y_lazy.with_columns(
        pls.Series("ay", filtered_ay)
    )

    # Acce. Z
    acc_z_lazy = pls.scan_csv(join_path(dir_path, filenames[3]), has_header = False, skip_rows = 1)
    acc_z_lazy = acc_z_lazy.rename({"column_1": "time", "column_2": "acc z"})
    acc_z_lazy = acc_z_lazy.with_columns(
        (pls.col("acc z")).alias("acc z") # - 9.805
    )
    az = acc_z_lazy.collect()["acc z"].to_numpy()
    filtered_az = apply_highpass_filter(az)
    acc_z_lazy = acc_z_lazy.with_columns(
        pls.Series("az", filtered_az)
    )

    # Merging
    res_df = linear_lazy.join(acc_x_lazy, on = "time", how = "inner")
    res_df = res_df.join(acc_y_lazy, on = "time", how = "inner")
    res_df = res_df.join(acc_z_lazy, on = "time", how = "inner")
    print(res_df.collect())

    if filtered:
        res_df = res_df.with_columns([
            pls.col("ax").cum_sum().alias("vx"),
            pls.col("ay").cum_sum().alias("vy"),
            pls.col("az").cum_sum().alias("vz")
        ])
    else:
        res_df = res_df.with_columns([
            pls.col("acc x").cum_sum().alias("vx"),
            pls.col("acc y").cum_sum().alias("vy"),
            pls.col("acc z").cum_sum().alias("vz")
        ])

    # Velocity counting
    res_df = res_df.with_columns(
        ((pls.col("vx")**2 + pls.col("vy")**2).sqrt() + pls.col("vz")**2).sqrt().alias("velocity")
    )
    print(res_df.collect())

    # Counting grade
    res_df = res_df.with_columns(
            ((pls.col("acc z")) / (pls.col("acc linear")**2 - (pls.col("acc z")) ).sqrt() ).alias("grade_acc")
    )
    res_df = res_df.with_columns(
            (pls.col("vz") / (pls.col("velocity")**2 - pls.col("vz") ).sqrt() ).alias("grade")
    )

    res_df = res_df.with_columns(
        pls.col("time"),
        pls.col("acc linear"),
        pls.col("acc x").cast(pls.Float32),
        pls.col("ax").cast(pls.Float32),
        pls.col("acc y").cast(pls.Float32),
        pls.col("ay").cast(pls.Float32),
        pls.col("acc z").cast(pls.Float32),
        pls.col("az").cast(pls.Float32),
        pls.col("vx").cast(pls.Float32),
        pls.col("vy").cast(pls.Float32),
        pls.col("vz").cast(pls.Float32),
        pls.col("velocity").cast(pls.Float32),
        pls.col("grade_acc").cast(pls.Float32),
        pls.col("grade").cast(pls.Float32),
        # pls.col("lat"),
        # pls.col("lon"),
    )

    return res_df

def apply_highpass_filter(data, cutoff = 0.3, fs = 50.0, order = 2):
    """
    Apply filter high-pass Butterworth.
    
    :param data: Data array needed to filter.
    :param cutoff: (Hz).
    :param fs: (Hz).
    :param order: Order of filter.
    :return: Data after filtered.
    """
    nyq = 0.5 * fs  # Tần số Nyquist
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    filtered_data = signal.filtfilt(b, a, data)
    return filtered_data

def apply_kalman_filter(data):
    """
    Apply kalman filter.
    
    :param data: Input array (1 dim).
    :return: Array after filtered.
    """
    # Initialize on one dimension
    kf = KalmanFilter(
        initial_state_mean=0,
        n_dim_obs=1,
        # Configurable
        transition_matrices = [1],
        observation_matrices = [1],
        observation_covariance = 2.088889e-06,
        transition_covariance = 50 * 2.088889e-06
    )
    
    state_means, _ = kf.smooth(data)
    return state_means.flatten()

if __name__ == "__main__":
    # Parameters
    username = "UserB"
    device = "Pixel 8 Pro"
    time_stamp = "historic-data 2025 03 09"
    res_df = read_and_join(username, device, time_stamp, filtered = False)

    import matplotlib.pyplot as plt
    sample_num = len(res_df.collect())

    # Linear Accelerometer
    mean = res_df.collect().mean()

    import matplotlib.pyplot as plt
    sample_num = len(res_df.collect())

    # Linear Accelerometer
    mean = res_df.collect().mean()

    plt.figure(figsize = (7, 7))

    plt.subplot(3, 3, 1)
    plt.plot(res_df.collect()["acc x"])
    plt.plot([mean["acc x"] for _ in range(sample_num)])
    plt.title("Accel. on X-axis")

    plt.subplot(3, 3, 2)
    plt.plot(res_df.collect()["acc y"])
    plt.plot([mean["acc y"] for _ in range(sample_num)])
    plt.title("Accel. on Y-axis")

    plt.subplot(3, 3, 3)
    plt.plot(res_df.collect()["acc z"])
    plt.plot([mean["acc z"] for _ in range(sample_num)])
    plt.title("Accel. on Z-axis")

    plt.subplot(3, 3, 4)
    plt.plot(res_df.collect()["vx"])
    plt.plot([mean["vx"] for _ in range(sample_num)])
    plt.title("Velocity on X-axis")

    plt.subplot(3, 3, 5)
    plt.plot(res_df.collect()["vy"])
    plt.plot([mean["vy"] for _ in range(sample_num)])
    plt.title("Velocity on Y-axis")

    plt.subplot(3, 3, 6)
    plt.plot(res_df.collect()["vz"])
    plt.plot([mean["vz"] for _ in range(sample_num)])
    plt.title("Velocity on Z-axis")
    
    plt.subplot(3, 3, 7)
    plt.plot(res_df.collect()["velocity"])
    plt.plot([mean["velocity"] for _ in range(sample_num)])
    plt.title("Velocity when running")

    plt.subplot(3, 3, 8)
    plt.plot(res_df.collect()["grade_acc"])
    plt.plot([mean["grade_acc"] for _ in range(sample_num)])
    plt.title("Grade when running (Accel.)")

    plt.subplot(3, 3, 9)
    plt.plot(res_df.collect()["grade"])
    plt.plot([mean["grade"] for _ in range(sample_num)])
    plt.title("Grade when running (Velocity)")

    # Adjust space
    plt.subplots_adjust(left=0.1, right=0.9, 
                        top=0.9, bottom=0.1, 
                        wspace=0.4, hspace=0.4)
    plt.show()