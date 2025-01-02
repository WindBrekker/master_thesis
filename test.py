from PyQt6.QtWidgets import QApplication, QCheckBox, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

class ToggleSwitch(QCheckBox):
    def __init__(self):
        super().__init__()
        self.setFixedSize(60, 30)
        self.setStyleSheet("""
            QCheckBox {
                background-color: #ccc;
                border-radius: 15px;
                width: 60px;
                height: 30px;
                padding: 0px;
            }
            QCheckBox::indicator {
                width: 30px;
                height: 30px;
                border-radius: 15px;
            }
            QCheckBox::indicator:checked {
                background-color: #3498db; /* Blue */
                margin-left: 30px;
            }
            QCheckBox::indicator:unchecked {
                background-color: #e74c3c; /* Red */
                margin-left: 0px;
            }
        """)
        self.setChecked(False)  # Start in the "Red" state

app = QApplication([])
window = QWidget()
layout = QVBoxLayout()

switch = ToggleSwitch()
switch.toggled.connect(lambda: print("Blue" if switch.isChecked() else "Red"))
layout.addWidget(switch)

window.setLayout(layout)
window.show()
app.exec()
