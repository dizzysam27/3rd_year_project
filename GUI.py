import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer, Qt
import cv2


class CameraDashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Camera Dashboard")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Camera display
        self.camera_label = QLabel(self)
        self.camera_label.setText("Initializing Camera...")
        self.camera_label.setStyleSheet("background-color: black; color: white;")
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.camera_label)

        # Start video feed
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        self.cap = cv2.VideoCapture(0)  # Open default camera
        if not self.cap.isOpened():
            self.camera_label.setText("Failed to open camera.")
        else:
            self.timer.start(30)  # Update every 30ms

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to RGB and then to QImage
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = channel * width
            qimage = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)

            # Update the QLabel with the new frame
            self.camera_label.setPixmap(QPixmap.fromImage(qimage))
        else:
            self.camera_label.setText("No frame captured.")

    def closeEvent(self, event):
        """Handle cleanup on close."""
        self.timer.stop()
        self.cap.release()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraDashboard()
    window.show()
    sys.exit(app.exec_())
