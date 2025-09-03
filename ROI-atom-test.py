"""
Demonstrates a variety of uses for ROI. This class provides a user-adjustable
region of interest marker. It is possible to customize the layout and 
function of the scale/rotate handles in very flexible ways. 
"""

import numpy as np
from tifffile import imread
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
import matplotlib as plt
from gaussian_fitting import *

pg.setConfigOptions(imageAxisOrder='row-major')

# --- Load image ---
image_path = "1ms-tof-500us-exp.tif"  # <-- change to your file name
arr = imread(image_path)

## create GUI
app = pg.mkQApp("ROI Examples")
w = pg.GraphicsLayoutWidget(show=True, size=(1000,800), border=True) #creates the instance of the window that has all of the roi content
w.setWindowTitle('pyqtgraph example: ROI Examples')

text = """Data Selection From atom Image.<br>\n
Drag an ROI or its handles to update the selected image.<br>
Hold CTRL while dragging to snap to pixel boundaries<br>
and 15-degree rotation angles. This is test code to count up atom numbers while
imaging them
"""
text2 = "Hello world!"
w1 = w.addLayout(row=0, col=0)
label1 = w1.addLabel(text, row=0, col=0) #adds the text as a label above this figure.
label2 = w1.addLabel(text2, row = 0, col= 1) # add a label. This label should be updated as well
v1a = w1.addViewBox(row=1, col=0, lockAspect=True)
v1b = w1.addViewBox(row=2, col=0, lockAspect=True)
#
#imv = pg.ImageView(discreteTimeLine=True, levelMode='mono')

#Initializes to images to view. 
img1a = pg.ImageItem(arr)
v1a.addItem(img1a)
img1b = pg.ImageItem()
v1b.addItem(img1b)
v1a.disableAutoRange('xy')
v1b.disableAutoRange('xy')
v1a.autoRange()
v1b.autoRange()

rois = []
rois.append(pg.RectROI([20, 20], [500, 500], pen=(0,9)))
#rois.append(pg.RectROI([20,40], [20,20], pen=(0,9)))

#add a cursor
vline = pg.InfiniteLine(angle=90, movable=True, pen='y')  # vertical
hline = pg.InfiniteLine(angle=0, movable=True, pen='y')   # horizontal

v1a.addItem(vline)
v1a.addItem(hline)


##atom-number scaling
C = 65.63*10**3
exp_time = 500*10**(-6)

def update(roi): #add sigma-x plotting 
    #define region
    region = roi.getArrayRegion(arr, img1a)
    img1b.setImage(region, levels=(0, arr.max()))
    total_count = np.sum(region)/(C*exp_time)
    avg_count = np.mean(region)

    new_text = f"""Atom number: {total_count:.0f} <br>
                Avg pixel count: {avg_count:.0f} <br> 
                Sigma-x: {total_count: .0f}<br>
                Sigma-y: {total_count: .0f}<br> """
    label2.setText(new_text)
    v1b.autoRange()
  

#add the plotting of the distribution across the cloud
for roi in rois: 
    roi.sigRegionChanged.connect(update) # this only takes one input? say that the roi has changed and needs to be changed. 
    v1a.addItem(roi)
    

update(rois[-1])


#if __name__ == '__main__':
pg.exec()
