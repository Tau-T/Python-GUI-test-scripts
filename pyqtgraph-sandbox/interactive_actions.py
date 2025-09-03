from pyqtgraph.Qt import QtWidgets #this imports from pyQt5 and PyQt6 
from pyqtgraph.Qt.QtWidgets import QWidget, Qmenu, QApplication
import pyqtgraph as pg

class MyViewBox(pg.ViewBox):
    def getContextMenus(self):
        # Start with the default menus
        menus = super().getContextMenus()
        
        # Create a custom menu and add your actions
        customMenu = QtWidgets.QMenu()
        action1 = customMenu.addAction("Custom Action 1")
        action2 = customMenu.addAction("Custom Action 2")
        action1.triggered.connect(lambda: print("Custom Action 1 triggered"))
        action2.triggered.connect(lambda: print("Custom Action 2 triggered"))
        
        menus.append(customMenu)  # append to default menus
        return menus