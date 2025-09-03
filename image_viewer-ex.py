"""
This example demonstrates the use of ImageView with 3-color image stacks.
ImageView is a high-level widget for displaying and analyzing 2D and 3D data.
ImageView provides:

  1. A zoomable region (ViewBox) for displaying the image
  2. A combination histogram and gradient editor (HistogramLUTItem) for
     controlling the visual appearance of the image
  3. A timeline for selecting the currently displayed frame (for 3D data only).
  4. Tools for very basic analysis of image data (see ROI and Norm buttons)

"""

import numpy as np
from tifffile import imread
import matplotlib.pyplot as plt

import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets

# Interpret image data as row-major instead of col-major
pg.setConfigOptions(imageAxisOrder='row-major')

app = pg.mkQApp("Lattice-AI-test-GUI")

## Create window with ImageView widget
win = QtWidgets.QMainWindow() #Qtwidgets is different from the other ROI code how? 
win.resize(1000,1000) #sets the size of the window
imv = pg.ImageView(discreteTimeLine=True, levelMode='mono')
win.setCentralWidget(imv)
win.show()
win.setWindowTitle('pyqtgraph example: ImageView')
imv.setHistogramLabel("Histogram label goes here")


# --- Load image ---
image_path = "1ms-tof-500us-exp.tif"  # <-- change to your file name
image = imread(image_path)

#display data
imv.setImage(image)

# Start up with an ROI
v3 = win.addViewBox(row=1, col=0, lockAspect=True)
r3a = pg.ROI([0,0], [10,10])
v3.addItem(r3a)

imv.ui.roiBtn.setChecked(True)
imv.roiClicked()

pg.exec()

#if __name__ == '__main__':
 #   pg.exec()
