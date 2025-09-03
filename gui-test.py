import numpy as np
import pyqtgraph as pg

from pyqtgraph.Qt import QtCore, QtWidgets


app = pg.mkQApp()
app = pg.mkQApp()
mw = QtWidgets.QMainWindow()
mw.setWindowTitle('pyqtgraph example: PlotWidget')
mw.resize(800,800)
cw = QtWidgets.QWidget()
mw.setCentralWidget(cw)
l = QtWidgets.QVBoxLayout()
cw.setLayout(l)

pw = pg.PlotWidget(name='Plot1')  ## giving the plots names allows us to link their axes together
l.addWidget(pw)
pw2 = pg.PlotWidget(name='Plot2')
l.addWidget(pw2)
pw3 = pg.PlotWidget()
l.addWidget(pw3)

mw.show()
