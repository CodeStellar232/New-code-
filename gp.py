import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QGridLayout, QLabel
from PyQt5.QtCore import pyqtSignal, Qt
import pyqtgraph as pg
import serial
import serial.tools.list_ports
import threading
from PyQt5.QtGui import QFont, QColor, QPalette
import time

class GraphsWindow(QWidget):
    update_graphs_signal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Telemetry Graphs")
        self.setGeometry(100, 100, 1100, 650)
        self.update_graphs_signal.connect(self.update_graphs)   

        self.arduino_connected = False
        self.serial_data = []
        self.arduino_port = None

        self.telemetry_fields = [
            "Team ID", "Timestamp", "Packet Count", "Altitude", "Pressure", "Temperature", "Voltage",
            "GNSS Time", "GNSS Latitude", "GNSS Longitude", "GNSS Altitude", "GNSS Satellites",
            "AccX", "AccY", "AccZ", "GyroX", "GyroY", "GyroZ", "Flight State"
        ]

        # Adjust graph_specs to fit into six boxes
        self.graph_specs = [
            ("Pressure [Pa]", ["Pressure"]),
            ("Altitude [m]", ["Altitude"]),
            ("Voltage [V]", ["Voltage"]),
            ("Accelerometer [m/s²]", ["AccX", "AccY", "AccZ"]),
            ("Gyroscope [rad/s]", ["GyroX", "GyroY", "GyroZ"]),
            ("Temperature [°C]", ["Temperature"])
        ]
        self.graphs = {}
        self.curves = {}
        self.data = {}
        
         # Create the main layout
        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)

        # Arrange graphs in a 2x3 grid (6 boxes)
        positions = [(i // 3, i % 3) for i in range(len(self.graph_specs))]
        for pos, (title, labels) in zip(positions, self.graph_specs):
            graph = self.create_graph(title, labels)
            grid_layout.addWidget(graph, *pos)

        self.serial_monitor = QLabel("Serial Monitor:\n")
        self.serial_monitor.setStyleSheet("color: black; background-color: white; padding: 6px;")
        self.serial_monitor.setFont(QFont('Arial', 10))

        main_layout.addLayout(grid_layout)
        main_layout.addWidget(self.serial_monitor)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        

    def create_graph(self, title, labels):
        plot_widget = pg.PlotWidget(title=title)
        plot_widget.setBackground("black")
        plot_widget.showGrid(x=True, y=True)

        legend = pg.LegendItem(offset=(70, 30))
        legend.setParentItem(plot_widget.getPlotItem())

        colors = ['r', 'g', 'b', 'y', 'c', 'm', 'w']

        for i, label in enumerate(labels):
            color = colors[i % len(colors)]
            self.graphs[label] = plot_widget
            self.data[label] = {'x': [], 'y': []}
            curve = plot_widget.plot([], [], pen=pg.mkPen(color=color, width=2), name=label)
            self.curves[label] = curve
            legend.addItem(curve, label)

        return plot_widget
   
    def update_graphs(self, new_data=None):
        if not self.arduino_connected or new_data is None:
            return

        for key, values in new_data.items():
            if key in self.curves:
                x_data = values['x'][-1000:]
                y_data = values['y'][-1000:]

                self.data[key]['x'] = self.data[key]['x'][-1000:]
                self.data[key]['y'] = self.data[key]['y'][-1000:]

                self.curves[key].setData(x_data, y_data)

                self.graphs[key].enableAutoRange(axis='x', enable=True)
                self.graphs[key].enableAutoRange(axis='y', enable=True)
                
    def update_data(self, data):
        """Update the graphs with the received data."""
        print(f"GraphsPage received data: {data}")
        self.update_graphs(data)

        self.show()

    

 