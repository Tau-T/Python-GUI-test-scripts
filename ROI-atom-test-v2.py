"""

File:        ROI_atomi-test.py
Author:      Matthew Tao
Date:        2025-07-31
Description: Demonstrates a variety of uses for ROI. This class provides a user-adjustable
region of interest marker. It is possible to customize the layout and
function of the scale/rotate handles in very flexible ways. In creating this code, ChatGPT was used.

Usage:
    python your_script_name.py [optional arguments]

Notes:
    - Any relevant background info or caveats
    - External dependencies (e.g. numpy, matplotlib)
    - Optional: link to related documentation or paper

Changes:
"""

import numpy as np
from tifffile import imread
import pyqtgraph as pg
import time
from gui_util import *

from pyqtgraph.Qt import QtWidgets
from PyQt5.QtCore import QTimer

import matplotlib as plt
#OS modules for file manipulation
import os
import glob
import re
import sys

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors


##########################################################################################################

################## FILE MANIPULATION##################

##########################################################################################################
# --- Load image from the most recent shot---
#folder path
base_dir = '/home/cscavity/Documents/cavity-control/solo_dev/MJT/repository/thorcam test/Images/MOT-images'  # CHANGE to your preferred root directory
date_str = time.strftime("%m-%d-%y")  # Format: MM-DD-YY
daily_folder = os.path.join(base_dir, date_str)
file_type = "*.tif"

#grab the most recent .tif file loaded from the experiment (format for files is hour, minute seconds)
#Reads all tif files and looks for the one with the latest time (max number file naming convention

# Get all .tif files
files = glob.glob(os.path.join(daily_folder, file_type))

# Build a list of (timestamp_tuple, filepath)
timestamped_files = [
    (extract_time_tuple(f), f) for f in files if extract_time_tuple(f) is not None
]

# Find the file with the largest time
if timestamped_files:
    latest_file = max(timestamped_files, key=lambda x: x[0])[1]
    print("Latest file:", latest_file)
else:
    print("No matching .tif files found.")
    exit()

#get the file_name in the current folder
file_name = os.path.basename(latest_file)

#load the filepath into python and grab the image.
image_path = latest_file  # <-- change to your file name
arr = imread(image_path)
##########################################################################################################

################## GUI CREATION ##################

##########################################################################################################
## create GUI
#define gui window
pg.setConfigOptions(imageAxisOrder='row-major')
app = pg.mkQApp("ROI Examples")
w = pg.GraphicsLayoutWidget(show=True, size=(1000, 800),
                            border=True)  # creates the instance of the window that has all of the roi content
w.setWindowTitle('pyqtgraph example: ROI Examples')

#define text to be displayed on GUI and color scheme
text = """Data Selection From atom Image.<br>\n
Drag an ROI or its handles to update the selected image.<br>
Hold CTRL while dragging to snap to pixel boundaries<br>
and 15-degree rotation angles. This is test code to count up atom numbers while
imaging them
"""
text2 = "Hello world!"

# Create LUT from jet colormap
cmap = cm.get_cmap('jet', 256)  # 256 color levels
lut = (cmap(np.linspace(0, 1, 256))[:, :3] * 255).astype(np.uint8)


w1 = w.addLayout(row=0, col=0)
label1 = w1.addLabel(text, row=0, col=0)  # adds the text as a label above this figure.
label2 = w1.addLabel(text2, row=0, col=1)  # add a label. This label should be updated as well
v1a = w1.addViewBox(row=1, col=0, lockAspect=True)
v1b = w1.addViewBox(row=2, col=0, lockAspect=True)
#
# imv = pg.ImageView(discreteTimeLine=True, levelMode='mono')

# Initializes to images to view.
img1a = pg.ImageItem(arr, lut=lut)
v1a.addItem(img1a)
img1b = pg.ImageItem(lut=lut)
v1b.addItem(img1b)
v1a.disableAutoRange('xy')
v1b.disableAutoRange('xy')
v1a.autoRange()
v1b.autoRange()

rois = []
rois.append(pg.RectROI([20, 20], [500, 500], pen=(0, 9)))
# rois.append(pg.RectROI([20,40], [20,20], pen=(0,9)))

# add a cursor
vline = pg.InfiniteLine(angle=90, movable=True, pen='y')  # vertical
hline = pg.InfiniteLine(angle=0, movable=True, pen='y')  # horizontal

v1a.addItem(vline)
v1a.addItem(hline)

##atom-number scaling
C = 65.63 * 10 ** 3
exp_time = 500 * 10 ** (-6)


def update(roi, force_reload=False): #changed so that we reload the image if new file is detected
    global arr
    if force_reload:
        arr = imread(latest_file)
        img1a.setImage(arr, levels=(0, arr.max()))
        print("Updating image with:", latest_file)
    #define region
    region = roi.getArrayRegion(arr, img1a)
    v1a.autoRange()

    img1b.setImage(region, levels=(0, arr.max()))
    total_count = np.sum(region) / (C * exp_time)
    avg_count = np.mean(region)

    new_text = f"""Atom number: {total_count:.0f} <br>
                Avg pixel count: {avg_count:.0f} <br> 
                Sigma-x: {total_count: .0f}<br>
                Sigma-y: {total_count: .0f}<br> 
                File opened: {file_name}<br>"""
    label2.setText(new_text)
    v1b.autoRange()



#extract time from current image:
# Find all numbers (including negative and decimal)
current_file = re.findall(r'-?\d+\.?\d*', file_name)
#print(f"The current file is: {current_file}")


# Step 2: Periodically check for new files


def check_for_new_file():
    global file_name, current_file
    files = glob.glob(os.path.join(daily_folder, file_type))
    new_files = [f for f in files if extract_time(f) and extract_time(f) > extract_time(latest_file)]

    if new_files:
        new_latest_file = find_latest_file(new_files)
        print("New file found:", new_latest_file)
        # update latest_time and process the new file
        global latest_time, latest_file
        latest_file = new_latest_file
        latest_time = extract_time(new_latest_file)

        file_name = os.path.basename(latest_file) #update file name on display

        update(rois[-1], force_reload=True)



#check for new file
timer = QTimer()
timer.timeout.connect(check_for_new_file) #lambda creates a function object out of print("hello"), which would other wise return "None" Type
timer.start(1000)


# add the plotting of the distribution across the cloud
for roi in rois:
    roi.sigRegionChanged.connect(lambda: update(roi))  # this only takes one input? say that the roi has changed and needs to be changed.
    v1a.addItem(roi)

update(rois[-1])



# if __name__ == '__main__':
sys.exit(pg.exec())
