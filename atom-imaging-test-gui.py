import sys
import os
import glob
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from scipy.optimize import curve_fit
from skimage.io import imread

# --- 2D Gaussian ---
def gaussian_2d(xy, amp, x0, y0, sigma_x, sigma_y, offset):
    x, y = xy
    return (amp * np.exp(-((x - x0)**2 / (2 * sigma_x**2) +
                           (y - y0)**2 / (2 * sigma_y**2))) + offset).ravel()

# --- Load the latest image in folder ---
def load_latest_image(folder):
    files = sorted(glob.glob(os.path.join(folder, '*.tif')), key=os.path.getmtime)
    if not files:
        return None
    return imread(files[-1])

# --- Analyze image within ROI ---
def analyze_roi(image, roi):
    roi_data = roi.getArrayRegion(image, img_item=image_item, returnMappedCoords=True)
    if roi_data is None or roi_data.shape[0] == 0:
        return None

    data = roi_data
    x = np.arange(data.shape[1])
    y = np.arange(data.shape[0])
    x, y = np.meshgrid(x, y)

    try:
        amp = data.max()
        x0 = data.shape[1] / 2
        y0 = data.shape[0] / 2
        sigma = 2
        offset = data.min()
        popt, _ = curve_fit(gaussian_2d, (x.ravel(), y.ravel()), data.ravel(),
                            p0=[amp, x0, y0, sigma, sigma, offset])
        return {
            'amplitude': popt[0],
            'center': (popt[1], popt[2]),
            'sigma_x': popt[3],
            'sigma_y': popt[4],
            'offset': popt[5],
            'total_counts': np.sum(data)
        }
    except Exception as e:
        print("Fit failed:", e)
        return None

# --- Main App ---
class AtomImageAnalyzer(QtGui.QMainWindow):
    def __init__(self, image_folder):
        super().__init__()
        self.setWindowTitle("Atom Image Analyzer")
        self.image_folder = image_folder

        self.widget = pg.GraphicsLayoutWidget()
        self.setCentralWidget(self.widget)

        self.view = self.widget.addViewBox()
        self.view.setAspectLocked(True)

        self.image_item = pg.ImageItem()
        self.view.addItem(self.image_item)
        global image_item
        image_item = self.image_item  # hack for getArrayRegion use

        self.roi = pg.RectROI([20, 20], [40, 40], pen='r')
        self.view.addItem(self.roi)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_image)
        self.timer.start(1000)  # 1 Hz

        self.status = QtGui.QLabel("Ready")
        self.statusBar().addPermanentWidget(self.status)

    def update_image(self):
        image = load_latest_image(self.image_folder)
        if image is None:
            self.status.setText("No image found")
            return

        self.image_item.setImage(image.T)  # transpose for display

        result = analyze_roi(image, self.roi)
        if result:
            txt = f"σx: {result['sigma_x']:.2f}, σy: {result['sigma_y']:.2f}, Counts: {result['total_counts']:.0f}"
            self.status.setText(txt)
        else:
            self.status.setText("Analysis failed")


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    folder = sys.argv[1] if len(sys.argv) > 1 else 'images'
    analyzer = AtomImageAnalyzer(folder)
    analyzer.show()
    sys.exit(app.exec_())
