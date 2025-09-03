"""
Demonstrates a variety of uses for ROI. This class provides a user-adjustable
region of interest marker. It is possible to customize the layout and 
function of the scale/rotate handles in very flexible ways. 
"""

import numpy as np
from tifffile import imread
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
import matplotlib.cm as cm

class MyViewBox_mod_menu(pg.ViewBox):
    def __init__(self):
        super().__init__()
        self.menu = QtWidgets.QMenu()
        self.menu.addAction("Action 1", lambda: print("Action 1 triggered"))
        self.menu.addAction("Action 2", lambda: print("Action 2 triggered"))
        self.menu.addAction("TOF ROI", lambda: self.add_roi('TOF'))
        self.menu.addAction("Blowaway ROI", lambda: self.add_roi('Blowaway'))
        self.menu.addAction("MOT", lambda: self.add_roi("MOT"))
        self.menu.addAction("Remove ROIs", lambda: self.remove_rois())

        

    def add_roi(self,roi_type):
            if roi_type == 'TOF':
                roi = pg.RectROI([20, 20], [500, 500], pen='r')
                rois.append(roi)
                self.addItem(roi)
            elif roi_type == 'Blowaway':
                roi = pg.RectROI([40,40], [250, 250], pen='g')
                rois.append(roi)
                self.addItem(roi) 
            elif roi_type == 'MOT':
                roi = pg.RectROI([100,100], [250,250], pen='w')
                rois.append(roi)
                self.addItem(roi)

    def remove_rois(self):
         for roi in rois:
            self.removeItem(roi)
         rois.clear()


# --- Load image ---
image_path = "1ms-tof-500us-exp.tif"  # <-- change to your file name
arr = np.transpose(imread(image_path))

## create GUI
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
app = pg.mkQApp("ROI Examples")
w = pg.GraphicsLayoutWidget(show=True, size=(1000,800), border=True)
w.setWindowTitle('pyqtgraph example: ROI Examples')




# Layout with label and custom ViewBox
w1 = w.addLayout(row=0, col=0)
text1 = "Hello this is my widget, 好嘢"
label1 = w1.addLabel(text1, row=0, col=0)

v1a = MyViewBox_mod_menu()
v1a.setMouseEnabled(x=False, y=False)  # prevent panning of the image
w1.addItem(v1a, row=1, col=0)

# Add rois
rois = []
# v1a.add_roi()
# rois.append(pg.RectROI([20, 20], [20, 20], pen=(0,9)))

    
# for roi in rois:
#     # roi.sigRegionChanged.connect(update)
#     v1a.addItem(roi)
# Make the ViewBox row expand more than the label row
# label1.setRowStretch(0, 0)   # label row minimal
# v1a.setRowStretch(1, 1)   # ViewBox row expands

# --- Apply jet colormap ---
cmap = cm.get_cmap('jet')                     
lut = (cmap(np.linspace(0, 1, 256)) * 255).astype(np.uint8)

img1a = pg.ImageItem(arr)
img1a.setLookupTable(lut)
v1a.addItem(img1a)

pg.exec()
