from pyqtgraph.Qt import QtWidgets #this imports from pyQt5 and PyQt6 
from pyqtgraph.Qt.QtWidgets import *
import pyqtgraph as pg
import sys
import numpy as np
from tifffile import imread
import matplotlib.cm as cm


class MyWindow(pg.GraphicsLayoutWidget):
    def __init__(self):
        super().__init__()
        self.context_menu = QMenu(self)
        action1 = self.context_menu.addAction("Action 1")
        action2 = self.context_menu.addAction("Action 2")

        self.show()

    def contextMenuEvent(self, event):
        print(event.globalPos())
        self.context_menu.exec(event.globalPos())
        

# app = QApplication(sys.argv)
app = pg.mkQApp("Right click example")
w = MyWindow()

# --- Load image ---
image_path = "1ms-tof-500us-exp.tif"  # <-- change to your file name
arr = np.transpose(imread(image_path))


## create GUI
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

# w = pg.GraphicsLayoutWidget(show=True, size=(1000,800), border=True)
# w.setWindowTitle('pyqtgraph example: ROI Examples')

# Layout with label and custom ViewBox
w1 = w.addLayout(row=0, col=0)
text1 = "Hello this is my widget, 好嘢"
label1 = w1.addLabel(text1, row=0, col=0)

v1a = w1.addViewBox(row=1, col=0, lockAspect=True, enableMenu=True)

# v1a = MyViewBox(lockAspect=True)
# v1a.setMouseEnabled(x=False, y=False)  # prevent panning of the image
# w1.addItem(v1a, row=1, col=0)

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