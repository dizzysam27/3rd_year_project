# General Imports
import sys
import cv2
import numpy as np
from gpiozero import Button

# PyQt5 Imports
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QTimer, QDateTime
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGridLayout, QPushButton, QHBoxLayout

# Maze Game Module Imports
from imageProcessing import ImageProcessor
from peripherals.lcdControl import LCD1602_WRITE
from peripherals.ledStripControl import ARDUINO
from peripherals.ledButtonControl import LEDBUTTON

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
        self.TimerLabel = QLabel('Time: 00:00.0')
        self.TimerLabel.setStyleSheet('border: 5px solid black; padding: 15px; font-size: 50px; background-color: rgb(200,200,200);')
        self.TimerLabel.setAlignment(QtCore.Qt.AlignCenter)
        gridLayout.addWidget(self.TimerLabel,
                             1, 1,
                             1, 1)
        # Timer Item
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(100)
        self.timerFlag = False
        self.tenCount = 0
        self.secCount = 0
        self.minCount = 0
        # Timer Buttons
        self.button1 = QPushButton('Start')
        self.button2 = QPushButton('Stop')
        self.button3 = QPushButton('Reset')
        hBoxLayout.addWidget(self.button1)
        hBoxLayout.addWidget(self.button2)
        hBoxLayout.addWidget(self.button3)
        self.button1.clicked.connect(lambda : kendama.currentMode.handleInput(1))
        self.button2.clicked.connect(lambda : kendama.currentMode.handleInput(2))
        self.button3.clicked.connect(lambda : kendama.currentMode.handleInput(3))

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

    def showTime(self):
        if self.timerFlag == True:
            self.TimerLabel.setText('Time: {:02d}:{:02d}.{:01d}'.format(self.minCount, self.secCount, self.tenCount))
            lcd.update_messages("", self.TimerLabel.text())
            self.tenCount += 1
        if self.tenCount == 10:
            self.tenCount = 0
            self.secCount += 1
        if self.secCount == 60:
            self.secCount = 0
            self.minCount += 1
    def startTimer(self):
        self.timerFlag = True
    def stopTimer(self):
        self.timerFlag = False
    def resetTimer(self):
        self.tenCount = 0
        self.secCount = 0
        self.minCount = 0

class PhysicalButtons():
    def __init__(self):
        self.pButton1 = Button(26, pull_up=True, bounce_time=0.1)
        self.pButton2 = Button(19, pull_up=True, bounce_time=0.1)
        self.pButton3 = Button(13, pull_up=True, bounce_time=0.1)

        self.pButton1.when_pressed = lambda : kendama.currentMode.handleInput(1)
        self.pButton2.when_pressed = lambda : kendama.currentMode.handleInput(2)
        self.pButton3.when_pressed = lambda : kendama.currentMode.handleInput(3)

class KENDAMA():
    def __init__(self):
        self.modes = {
            "Menu" : MenuMode(),
            "Manual" : ManualMode()
        }

        self.currentMode = self.modes["Menu"]

    def switchMode(self, nextMode):
        if nextMode in self.modes:
            self.currentMode = self.modes[nextMode]
            self.currentMode.update()

class MenuMode():

    def handleInput(self, button):
        if button == 1:
            mainWindow.startTimer()
        elif button == 2:
            mainWindow.stopTimer()
        elif button == 3:
            kendama.switchMode("Manual")

    def update(self):
        mainWindow.button3.setText("Manual")
        mainWindow.TitleLabel.setText("MENU MODE")
        lcd.update_messages("MENU MODE", "")
        ledStrip.write_to_arduino(4)
        lcd.setRGB(255, 255, 255)
        ledButtons.setLED(0,1,1)

class ManualMode():

    def handleInput(self, button):
        if button == 1:
            mainWindow.startTimer()
        elif button == 2:
            mainWindow.stopTimer()
        elif button == 3:
            kendama.switchMode("Menu")
    
    def update(self):
        mainWindow.button3.setText("Menu")
        mainWindow.TitleLabel.setText("MANUAL MODE")
        lcd.update_messages("MANUAL MODE", "")
        ledStrip.write_to_arduino(2)
        lcd.setRGB(255, 0, 0)
        ledButtons.setLED(1,0,0)

# Mode Manager Call
kendama = KENDAMA()

# Other Peripheral Calls
processor = ImageProcessor()
pButtons = PhysicalButtons()
ledButtons = LEDBUTTON()
lcd = LCD1602_WRITE()
ledStrip = ARDUINO()

# Main PyQt Application Loop
while True:
    app = QApplication(sys.argv)
    mainWindow = App()
    mainWindow.show()
    sys.exit(app.exec_())