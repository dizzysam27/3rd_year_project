import sys
import cv2
import numpy as np

# PyQt5 Imports
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame

# Module Imports
### TO BE FILLED OUT

# mainWindow GUI Class
class App(QWidget):
    def __init__(self):
        # Initialise Class and QApplication
        app = QApplication(sys.argv)
        super().__init__()
        self.setWindowTitle('Group 15 - Maze Project')

        # Set and find fullscreen size
        self.showFullScreen()
        screenWidth = app.primaryScreen().size().width()
        screenHeight = app.primaryScreen().size().height()
        
        # Set camera feed dimensions
        self.imageWidth = int(screenWidth * (2/3))
        self.imageHeight = int(self.imageWidth * (3/4))
        
        # Create main grid with camera feed size
        mainGrid = QGridLayout()
        self.setLayout(mainGrid)
        mainGrid.setHorizontalSpacing(5)
        mainGrid.setVerticalSpacing(5)
        mainGrid.setColumnMinimumWidth(0, self.imageWidth)
        mainGrid.setRowMinimumHeight(1, self.imageHeight)

        # Content vertical layout
        contentVBox = QVBoxLayout()
        mainGrid.addLayout(contentVBox, 1, 1, 1, 1)

        # Rate Commands horizontal layout
        rateHBox = QHBoxLayout()

        # Camera Feed
        self.imageLabel = QLabel('Image')
        self.imageLabel.setStyleSheet('border: 5px solid black')
        mainGrid.addWidget(self.imageLabel, 1, 0, 1, 1)

        # Title Block
        self.titleLabel = QLabel('Title')
        self.titleLabel.setStyleSheet('border: 5px solid black')
        mainGrid.addWidget(self.titleLabel, 0, 0, 1, 2)

        # Timer
        self.timerLabel = QLabel('00:00.0')
        self.timerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timerLabel.setMaximumHeight(150)
        self.timerLabel.setStyleSheet('border: 5px solid black; font: bold 100px')
        contentVBox.addWidget(self.timerLabel)

        # Button Labels
        buttonLabelHBox = QHBoxLayout()
        contentVBox.addLayout(buttonLabelHBox)
        button1Box = QVBoxLayout()
        button2Box = QVBoxLayout()
        button3Box = QVBoxLayout()
        buttonLabelHBox.addLayout(button1Box)
        buttonLabelHBox.addLayout(button2Box)
        buttonLabelHBox.addLayout(button3Box)
        self.buttonLabel1 = QLabel('AI\nSolve')
        self.buttonLabel1.setAlignment(QtCore.Qt.AlignCenter)
        self.buttonLabel1.setMaximumSize(200, 80)
        self.buttonLabel1.setStyleSheet('font: bold 25px')
        button1Box.addWidget(self.buttonLabel1)
        self.button1 = QPushButton()
        self.button1.setMaximumSize(100, 100)
        self.button1.setStyleSheet('border-radius: 50px; border: 8px solid green; background-color: #C0C0C0')
        button1Box.addWidget(self.button1)
        self.buttonLabel2 = QLabel('Manual\nSolve')
        self.buttonLabel2.setAlignment(QtCore.Qt.AlignCenter)
        self.buttonLabel2.setMaximumSize(200, 80)
        self.buttonLabel2.setStyleSheet('font: bold 25px')
        button2Box.addWidget(self.buttonLabel2)
        self.button2 = QPushButton()
        self.button2.setMaximumSize(100, 100)
        self.button2.setStyleSheet('border-radius: 50px; border: 8px solid red; background-color: #C0C0C0')
        button2Box.addWidget(self.button2)
        self.buttonLabel3 = QLabel('Calibrate')
        self.buttonLabel3.setAlignment(QtCore.Qt.AlignCenter)
        self.buttonLabel3.setMaximumSize(200, 80)
        self.buttonLabel3.setStyleSheet('font: bold 25px')
        button3Box.addWidget(self.buttonLabel3)
        self.button3 = QPushButton()
        self.button3.setMaximumSize(100, 100)
        self.button3.setStyleSheet('border-radius: 50px; border: 8px solid blue; background-color: #C0C0C0')
        button3Box.addWidget(self.button3)
        self.button3.clicked.connect(self.testFunc)

        # PWM Brightness Slider
        self.brightnessLabel = QLabel('Brightness')
        self.brightnessLabel.setStyleSheet('border: 5px solid black')
        contentVBox.addWidget(self.brightnessLabel)
        
        # Motor Rate Commands
        contentVBox.addLayout(rateHBox)

        rateTitle = QLabel("Current Motor Positions:")
        rateHBox.addWidget(rateTitle)

        xRateTitle = QLabel("X:")
        xRateTitle.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        rateHBox.addWidget(xRateTitle)
        self.xRateLabel = QLabel("0")
        rateHBox.addWidget(self.xRateLabel)

        yRateTitle = QLabel("Y:")
        yRateTitle.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight) 
        rateHBox.addWidget(yRateTitle)
        self.yRateLabel = QLabel("0")
        rateHBox.addWidget(self.yRateLabel)
        

        sys.exit(app.exec_())

    def testFunc(self):
        self.button3.setStyleSheet('border-radius: 50px; border: 8px solid #C0C0C0; background-color: #C0C0C0')

while True:
    mainWindow = App()
    mainWindow.show()