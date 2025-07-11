import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
)
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
from matplotlib.figure import Figure

class HeatmapApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Zoomable Heatmap with Mean')
        self.setGeometry(100, 100, 800, 600)

        # Main widget
        widget = QWidget(self)
        layout = QVBoxLayout(widget)

        # Mean label
        self.mean_label = QLabel("Mean of visible region: ", self)
        layout.addWidget(self.mean_label)

        # Create figure & canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        # Generate heatmap data
        self.data = np.random.rand(100, 100)

        # Plot heatmap
        self.heatmap = self.ax.imshow(self.data, cmap='viridis', interpolation='nearest')
        self.figure.colorbar(self.heatmap)

        # Toolbar for zoom/pan
        layout.addWidget(NavigationToolbar(self.canvas, self))
        layout.addWidget(self.canvas)

        # Connect to zoom/pan events
        self.canvas.mpl_connect('draw_event', self.update_mean_on_zoom)

        # Finalize layout
        self.setCentralWidget(widget)

    def update_mean_on_zoom(self, event):
        # Get current view limits
        x0, x1 = self.ax.get_xlim()
        y0, y1 = self.ax.get_ylim()

        # Convert to integer indices
        x0, x1 = int(np.floor(x0)), int(np.ceil(x1))
        y0, y1 = int(np.floor(y0)), int(np.ceil(y1))

        # Clip to valid range
        x0, x1 = np.clip([x0, x1], 0, self.data.shape[1])
        y0, y1 = np.clip([y0, y1], 0, self.data.shape[0])

        # Slice visible data
        visible_data = self.data[y0:y1, x0:x1]

        if visible_data.size > 0:
            mean_val = visible_data.mean()
            self.mean_label.setText(f"Mean of visible region: {mean_val:.4f}")
        else:
            self.mean_label.setText("Mean of visible region: N/A")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HeatmapApp()
    window.show()
    sys.exit(app.exec())
