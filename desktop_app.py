import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QLabel
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

API_UPLOAD = "http://127.0.0.1:8001/api/upload/"


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer (Desktop)")
        self.setGeometry(200, 200, 600, 600)

        self.layout = QVBoxLayout()

        self.label = QLabel("No file selected")
        self.layout.addWidget(self.label)

        self.btn_select = QPushButton("Select CSV")
        self.btn_select.clicked.connect(self.select_file)
        self.layout.addWidget(self.btn_select)

        self.btn_upload = QPushButton("Upload & Analyze")
        self.btn_upload.clicked.connect(self.upload_file)
        self.layout.addWidget(self.btn_upload)

        self.result_label = QLabel("")
        self.layout.addWidget(self.result_label)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)
        self.file_path = None

    def select_file(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Open CSV", "", "CSV Files (*.csv)"
        )
        if file:
            self.file_path = file
            self.label.setText(file)

    def upload_file(self):
        if not self.file_path:
            self.result_label.setText("Please select a file first")
            return

        with open(self.file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(API_UPLOAD, files=files)

        data = response.json()

        text = (
            f"Total: {data['total_count']}\n"
            f"Avg Flowrate: {data['avg_flowrate']}\n"
            f"Avg Pressure: {data['avg_pressure']}\n"
            f"Avg Temperature: {data['avg_temperature']}"
        )
        self.result_label.setText(text)

        self.plot_chart(data["type_distribution"])

    def plot_chart(self, dist):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(dist.keys(), dist.values())
        ax.set_title("Equipment Type Distribution")
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())




