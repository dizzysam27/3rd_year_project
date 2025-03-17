import sys
import cv2
import numpy as np

# PyQt5 Imports
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QPlainTextEdit

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

        # Camera Feed
        self.imageLabel = QLabel('Image')
        self.imageLabel.setStyleSheet('border: 5px solid black')
        mainGrid.addWidget(self.imageLabel, 1, 0, 1, 1)

        # Header
        headerHBox = QHBoxLayout()
        mainGrid.addLayout(headerHBox, 0, 0, 1, 2)
        self.titleLabel = QLabel('Group 15 Maze Game')
        self.titleLabel.setStyleSheet('border: 5px solid black; font: bold 50px')
        headerHBox.addWidget(self.titleLabel)
        self.modeLabel = QLabel('Menu')
        self.modeLabel.setStyleSheet('border: 5px solid black; font: bold 50px')
        self.modeLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
        headerHBox.addWidget(self.modeLabel)

        # Timer
        self.timerLabel = QLabel('00:00.0')
        self.timerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timerLabel.setMinimumHeight(150)
        self.timerLabel.setStyleSheet('border: 5px solid black; font: bold 100px')
        contentVBox.addWidget(self.timerLabel)

        # Button Labels
        buttonLabelHBox = QHBoxLayout()
        contentVBox.addLayout(buttonLabelHBox)
        button1Box = QVBoxLayout()
        button2Box = QVBoxLayout()
        button3Box = QVBoxLayout()
        buttonPH = QLabel('')
        buttonPH.setMinimumHeight(200)
        buttonPH.setMaximumWidth(1)
        buttonLabelHBox.addWidget(buttonPH)
        buttonLabelHBox.addLayout(button1Box)
        buttonLabelHBox.addLayout(button2Box)
        buttonLabelHBox.addLayout(button3Box)
        buttonPH2 = QLabel('')
        buttonPH2.setMinimumHeight(200)
        buttonPH2.setMaximumWidth(1)
        buttonLabelHBox.addWidget(buttonPH2)
        self.buttonLabel1 = QLabel('AI\nSolve')
        self.buttonLabel1.setAlignment(QtCore.Qt.AlignCenter)
        self.buttonLabel1.setMaximumSize(500, 80)
        self.buttonLabel1.setStyleSheet('font: bold 25px')
        button1Box.addWidget(self.buttonLabel1)
        self.button1 = QPushButton()
        self.button1.setMaximumSize(100, 100)
        self.button1.setStyleSheet('border-radius: 50px; border: 8px solid green; background-color: #C0C0C0')
        button1Box.addWidget(self.button1)
        self.buttonLabel2 = QLabel('Manual\nSolve')
        self.buttonLabel2.setAlignment(QtCore.Qt.AlignCenter)
        self.buttonLabel2.setMaximumSize(500, 80)
        self.buttonLabel2.setStyleSheet('font: bold 25px')
        button2Box.addWidget(self.buttonLabel2)
        self.button2 = QPushButton()
        self.button2.setMaximumSize(100, 100)
        self.button2.setStyleSheet('border-radius: 50px; border: 8px solid red; background-color: #C0C0C0')
        button2Box.addWidget(self.button2)
        self.buttonLabel3 = QLabel('Calibrate')
        self.buttonLabel3.setAlignment(QtCore.Qt.AlignCenter)
        self.buttonLabel3.setMaximumSize(500, 80)
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
        self.brightnessLabel.setMinimumHeight(100)
        contentVBox.addWidget(self.brightnessLabel)
        
        # Motor Rate Commands
        rateHBox = QHBoxLayout()
        contentVBox.addLayout(rateHBox)

        rateTitle = QLabel('Current Motor Positions:')
        rateTitle.setMinimumHeight(100)
        rateTitle.setStyleSheet('font: 30px')
        rateHBox.addWidget(rateTitle)

        self.xRateLabel = QLabel('X: 0')
        self.xRateLabel.setMinimumHeight(100)
        self.xRateLabel.setStyleSheet('font: 30px')
        self.xRateLabel.setAlignment(QtCore.Qt.AlignCenter)
        rateHBox.addWidget(self.xRateLabel)

        self.yRateLabel = QLabel('Y: 0')
        self.yRateLabel.setMinimumHeight(100)
        self.yRateLabel.setStyleSheet('font: 30px')
        self.yRateLabel.setAlignment(QtCore.Qt.AlignCenter)
        rateHBox.addWidget(self.yRateLabel)

        # Command Box
        self.commandBox = QPlainTextEdit('Initialising System...')
        self.commandBox.setStyleSheet('border: 2px solid black; font: 10px; background-color: #C0C0C0')
        self.commandBox.appendPlainText('Done!')
        contentVBox.addWidget(self.commandBox)
        

        sys.exit(app.exec_())

    def testFunc(self):
        self.button3.setStyleSheet('border-radius: 50px; border: 8px solid #C0C0C0; background-color: #C0C0C0')

while True:
    mainWindow = App()
    mainWindow.show()