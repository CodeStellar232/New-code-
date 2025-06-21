import sys

from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QPushButton, QGridLayout,  QWidget, QMainWindow
)
from PyQt5.QtCore import Qt

class DbWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.setGeometry(150, 150, 1280, 750)
        self.resize(600, 550)
        self.telemetry_fields = [
            "Team ID", "Timestamp", "Packet Count", "Altitude", "Pressure", "Temperature", "Voltage",
            "GNSS Time", "GNSS Latitude", "GNSS Longitude", "GNSS Altitude", "GNSS Satellites",
            "Accel X", "Accel Y", "Accel Z", "Gyro X", "Gyro Y", "Gyro Z", "Flight State"
        ]
        self.data_store = []  # Sample data store
        self.labels = {}
        self.values = {}
        self.initUI()

    def initUI(self):
        container = QWidget()
        self.setCentralWidget(container)

        main_layout = QHBoxLayout()
        container.setLayout(main_layout)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        telemetry_group = QGroupBox("Dashboard")
        telemetry_layout = QGridLayout()
        telemetry_layout.setColumnStretch(0, 0)
        telemetry_layout.setColumnStretch(1, 0)
        telemetry_layout.setColumnStretch(2, 0)

        for i, key in enumerate(self.telemetry_fields):
            row = i // 3
            col = i % 3

            # Create a group box for each telemetry field
            field_group = QGroupBox()
            field_layout = QHBoxLayout(field_group)
            field_layout.setContentsMargins(5, 5, 5, 5)
            field_layout.setSpacing(5)

            label = QLabel(f"{key}:")
            value = QLabel("N/A")
            self.labels[key] = label
            self.values[key] = value

            field_layout.addWidget(label)
            field_layout.addWidget(value)

            telemetry_layout.addWidget(field_group, row, col)

        telemetry_group.setLayout(telemetry_layout)
        telemetry_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")

        right_layout = QVBoxLayout()
        self.save_button = QPushButton("Save Data to CSV & PDF", self)
        self.save_button.clicked.connect(self.save_data)
        right_layout.addWidget(self.save_button)

        main_layout.addWidget(telemetry_group)
        main_layout.addLayout(right_layout)

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    db_window = DbWindow()
    db_window.show()
    sys.exit(app.exec_())
    