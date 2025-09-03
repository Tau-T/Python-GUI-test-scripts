import re
import glob
import os

# Step 1: Initial scan to get latest timestamp
def extract_time(filename):
    match = re.search(r"_(\d{6})\.tif$", filename)
    return match.group(1) if match else None

def time_str_to_tuple(time_str):
    return int(time_str[0:2]), int(time_str[2:4]), int(time_str[4:6])

def find_latest_file(files):
    time_file_pairs = [
        (time_str_to_tuple(extract_time(f)), f)
        for f in files if extract_time(f)
    ]
    return max(time_file_pairs, key=lambda x: x[0])[1] if time_file_pairs else None

# Extract HHMMSS from filename and return as (HH, MM, SS)
def extract_time_tuple(filename):
    match = re.search(r"_(\d{6})\.tif$", os.path.basename(filename))
    if match:
        time_str = match.group(1)
        hh = int(time_str[0:2])
        mm = int(time_str[2:4])
        ss = int(time_str[4:6])
        return (hh, mm, ss)
    else:
        return None


# Step 2: Periodically check for new files
def check_for_new_file():
    files = glob.glob(os.path.join(folder, pattern))
    new_files = [f for f in files if extract_time(f) and extract_time(f) > latest_time]

    if new_files:
        new_latest_file = find_latest_file(new_files)
        print("New file found:", new_latest_file)
        # update latest_time and process the new file
        global latest_time, latest_file
        latest_file = new_latest_file
        latest_time = extract_time(new_latest_file)
    else:
        print("No new file found")