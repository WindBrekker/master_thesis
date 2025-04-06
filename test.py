import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QProgressBar, QPushButton, QDialog, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QThread, pyqtSignal

class WorkerThread(QThread):
    progress_signal = pyqtSignal(int)  # Signal to send progress updates

    def __init__(self, indices):
        super().__init__()
        self.indices = indices

    def run(self):
        for i in range(len(self.indices)):
            # Simulating work, replace with actual work code
            self.progress_signal.emit(int((i + 1) / len(self.indices) * 100))

class ProgressDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Processing...")
        self.setModal(True)  # Make the dialog modal to block interaction with other windows
        self.setGeometry(300, 300, 400, 100)

        # Set up the layout and widgets for the progress dialog
        layout = QVBoxLayout()

        self.label = QLabel("Processing...", self)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)
        
        self.setLayout(layout)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Processing with Progress Bar")
        self.setGeometry(100, 100, 400, 100)

        # Set up the UI layout and widgets
        layout = QVBoxLayout()
        
        self.start_button = QPushButton("Start Processing", self)
        self.start_button.clicked.connect(self.start_processing)

        layout.addWidget(self.start_button)

        self.setLayout(layout)

    def start_processing(self):
        indices = list(range(32000))  # Example indices for processing (32,000 elements)

        # Create the progress dialog
        self.progress_dialog = ProgressDialog(self)
        self.progress_dialog.show()

        # Create the worker thread and connect its progress signal to update the progress bar
        self.worker = WorkerThread(indices)
        self.worker.progress_signal.connect(self.progress_dialog.update_progress)
        self.worker.finished.connect(self.progress_dialog.accept)  # Close the dialog when finished
        self.worker.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
