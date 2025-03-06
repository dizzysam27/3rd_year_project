# General Imports
import sys
import cv2
import numpy as np

# PyQt5 Imports
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QTimer, QDateTime
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGridLayout, QPushButton, QHBoxLayout

# Maze Game Module Imports
from imageProcessing import ImageProcessor

# Main GUI App Class
class App(QWidget):
    def __init__(self):
        # Inherit QWidget features
        super().__init__()

        # Image Size Definition
        self.imageWidth = 1374
        self.imageHeight = 1219

        # Overall GUI appearance
        self.setWindowTitle("Group 15 - Maze Game")
        self.showFullScreen()

        # Layout Boxes
        gridLayout = QGridLayout()
        self.setLayout(gridLayout)
        hBoxLayout = QHBoxLayout()
        gridLayout.addLayout(hBoxLayout,
                             2, 1,
                             1, 1)

        # Title GUI
        self.TitleLabel = QLabel('Welcome to the Maze Game! Sponsored by Kendama Playtime')
        self.TitleLabel.setStyleSheet('border: 5px solid black; padding: 15px; font-size: 50px; background-color: rgb(200,200,200);')
        self.TitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        gridLayout.addWidget(self.TitleLabel,
                             0, 0,
                             1, 2)

        # Video GUI
        self.VideoLabel = QLabel('Video Output')
        self.VideoLabel.resize(self.imageWidth, self.imageHeight)
        self.VideoLabel.setStyleSheet('border: 5px solid black')
        self.VideoLabel.setAlignment(QtCore.Qt.AlignCenter)
        gridLayout.addWidget(self.VideoLabel,
                             1, 0,
                             10, 1)
        # Video Capture Thread
        processor.cameraVideo.connect(self.updateImage) # Run updateImage when cameraVideo is modified in ImageProcessor()
        processor.start()
        
        # Timer GUI
        self.TimerLabel = QLabel('Time: 00:00.000')
        self.TimerLabel.setStyleSheet('border: 5px solid black; padding: 15px; font-size: 50px; background-color: rgb(200,200,200);')
        self.TimerLabel.setAlignment(QtCore.Qt.AlignCenter)
        gridLayout.addWidget(self.TimerLabel,
                             1, 1,
                             1, 1)
        # Start/Stop Timer Test Buttons
        self.TimerStart = QPushButton('Start')
        self.TimerStop = QPushButton('Stop')
        hBoxLayout.addWidget(self.TimerStart)
        hBoxLayout.addWidget(self.TimerStop)
        # Timer Stuff?
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTimer)
        #self.TimerStart.clicked.connect(self.startTimer)
        #self.TimerStop.clicked.connect(self.stopTimer)

    # PyQt Slot for updating image contents
    @pyqtSlot(np.ndarray)
    # Image conversion from opencv image to QT pixel map
    def updateImage(self, image):
        rgbImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgbImage.shape
        lineSize = ch * w
        qtImage = QtGui.QImage(rgbImage.data, w, h, lineSize, QtGui.QImage.Format_RGB888)
        scaledImage = qtImage.scaled(self.imageWidth, self.imageHeight, Qt.KeepAspectRatio)
        pixmapImage = QPixmap.fromImage(scaledImage)
        self.VideoLabel.setPixmap(pixmapImage)

    def updateTimer(self, time):
        pass

processor = ImageProcessor()
while True:
    app = QApplication(sys.argv)
    mainWindow = App()
    mainWindow.show()
    sys.exit(app.exec_())