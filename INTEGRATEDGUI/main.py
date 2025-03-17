# General Imports
import sys
import cv2
import numpy as np
from gpiozero import Button # type: ignore

# PyQt5 Imports
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QTimer, QDateTime
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGridLayout, QPushButton, QHBoxLayout, QVBoxLayout, QPlainTextEdit

# Maze Game Module Imports
from imageProcessing import IMAGEPROCESSOR
from lcdControl import LCD1602_WRITE
from peripherals import LEDSTRIPCONTROL
from peripherals import LEDBUTTONCONTROL
import joystickControl
#from joystickControl import JOYSTICK_READ_DATA
from motorControl import PCA9685

global screenWidth, screenHeight

# Main GUI App Class
class App(QWidget):
    def __init__(self):
        # Initialise Class and QApplication
        super().__init__()
        self.setWindowTitle('Group 15 - Maze Project')

        # Set and find fullscreen size
        self.showFullScreen()
        self.setFixedSize(QtCore.QSize(screenWidth, screenHeight))

        print(screenWidth)
        print(screenHeight)
        
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

        # Camera Feed
        self.imageLabel = QLabel('Image')
        self.imageLabel.setStyleSheet('border: 2px solid black')
        mainGrid.addWidget(self.imageLabel, 1, 0, 1, 1)
        # Video Capture Thread
        processor.cameraVideo.connect(self.updateImage) # Run updateImage when cameraVideo is modified in ImageProcessor()
        processor.start()
        
        # Timer
        self.timerLabel = QLabel('00:00.0')
        self.timerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timerLabel.setMinimumHeight(150)
        self.timerLabel.setStyleSheet('border: 5px solid black; font: bold 100px')
        contentVBox.addWidget(self.timerLabel)
        # Timer Item
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(100)
        self.timerFlag = False
        self.tenCount = 0
        self.secCount = 0
        self.minCount = 0
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
        self.button1.clicked.connect(lambda : kendama.currentMode.handleInput(1))
        self.button2.clicked.connect(lambda : kendama.currentMode.handleInput(2))
        self.button3.clicked.connect(lambda : kendama.currentMode.handleInput(3))

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

        joystick.xRate.connect(self.updateX)
        joystick.yRate.connect(self.updateY)

        # Command Box
        self.commandBox = QPlainTextEdit('Initialising System...')
        self.commandBox.setStyleSheet('border: 2px solid black; font: 10px; background-color: #C0C0C0')
        self.commandBox.appendPlainText('Done!')
        contentVBox.addWidget(self.commandBox)

        joystick.printBuffer.connect(self.updateConsole)

        # Begin Event Loop

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
        self.imageLabel.setPixmap(pixmapImage)

    # PyQt Slot for updating motor rates
    @pyqtSlot(int)
    def updateX(self, xRate):
        motors.setServoPulse(0,1915+xRate/2)
        self.xRateLabel.setText('X: {}'.format(xRate))
    def updateY(self, yRate):
        motors.setServoPulse(1,1850+yRate/2)
        self.yRateLabel.setText('Y: {}'.format(yRate))

    def showTime(self):
        if self.timerFlag == True:
            self.timerLabel.setText('{:02d}:{:02d}.{:01d}'.format(self.minCount, self.secCount, self.tenCount))
            lcd.update_messages(self.timerLabel.text(), "")
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
        self.timerLabel.setText('{:02d}:{:02d}.{:01d}'.format(self.minCount, self.secCount, self.tenCount))

    @pyqtSlot(str)
    def updateConsole(self, printBuffer):
        self.commandBox.appendPlainText('[{}]: {}'.format(QDateTime.currentDateTime(), printBuffer))

class PHYSICALBUTTONS():
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
            'Menu' : MenuMode(),
            'Manual' : ManualMode(),
            'ManualRunning' : ManualRunningMode(),
            'ManualStopped' : ManualStoppedMode(),
            'AI' : AIMode(),
            'Calibration' : CalibrationMode()
        }

        self.currentMode = self.modes['Menu']

    def switchMode(self, nextMode):
        if nextMode in self.modes:
            self.currentMode = self.modes[nextMode]
            self.currentMode.update()

    def update(self, b1=None, b2=None, b3=None, title=None, lcdTxt=None, lcdCol=None, ledStr=None, ledBtn=None):
        if b1 == None: pass
        else: mainWindow.buttonLabel1.setText(b1)
        if b2 == None: pass
        else: mainWindow.buttonLabel2.setText(b2)
        if b3 == None: pass
        else: mainWindow.buttonLabel3.setText(b3)
        if title == None: pass
        else: mainWindow.modeLabel.setText(title)
        if lcdTxt == None: pass
        else: lcd.update_messages(lcdTxt[0], lcdTxt[1])
        if lcdCol == None: pass
        else: lcd.setRGB(lcdCol[0], lcdCol[1], lcdCol[2])
        if ledStr == None: pass
        else: ledStrip.writeArduino(ledStr)
        if ledBtn == None: pass
        else:
            colourArray = ['#C0C0C0', 'green', 'red', 'blue']
            ledButtons.setLED(ledBtn[0], ledBtn[1], ledBtn[2])
            mainWindow.button1.setStyleSheet('border-radius: 50px; border: 8px solid {}; background-color: #C0C0C0'.format(colourArray[ledBtn[0]]))
            mainWindow.button2.setStyleSheet('border-radius: 50px; border: 8px solid {}; background-color: #C0C0C0'.format(colourArray[ledBtn[1]*2]))
            mainWindow.button3.setStyleSheet('border-radius: 50px; border: 8px solid {}; background-color: #C0C0C0'.format(colourArray[ledBtn[2]*3]))
            

class MenuMode():

    def update(self):
        kendama.update(b1='AI',
                       b2='Manual',
                       b3='Cal.',
                       title='Welcome to the Maze Game!',
                       lcdTxt=['Main Menu',
                               'AI   Manual  Cal'],
                       lcdCol=[255,255,255],
                       ledStr=4,
                       ledBtn=[1,1,1]
        )
    
    def handleInput(self, button):
        if button == 1:
            kendama.switchMode('AI')
        elif button == 2:
            kendama.switchMode('Manual')
        elif button == 3:
            kendama.switchMode('Calibration')
        else:
            pass

class ManualMode():

    def update(self):
        kendama.update(b1='Start',
                       b2='',
                       b3='Menu',
                       title='Manual Solving Mode',
                       lcdTxt=['{}'.format(mainWindow.timerLabel.text()),
                               'Start       Menu'],
                       lcdCol=[255,0,0],
                       ledStr=2,
                       ledBtn=[1,0,1]
        )

    def handleInput(self, button):
        if button == 1:
            mainWindow.startTimer()
            kendama.switchMode('ManualRunning')
        elif button == 3:
            kendama.switchMode('Menu')
        else:
            pass

class ManualRunningMode():

    def update(self):
        kendama.update(b1='',
                       b2='Stop',
                       b3='',
                       title='Manual Solving Mode',
                       lcdTxt=['',
                               '      Stop      '],
                       ledStr=5,
                       ledBtn=[0,1,0]
        )
        joystick.start_reading()

    def handleInput(self, button):
        if button == 2:
            mainWindow.stopTimer()
            kendama.switchMode('ManualStopped')
            mainWindow.joystickFlag = 0
        else:
            pass

class ManualStoppedMode():

    def update(self):
        kendama.update(b1='Start',
                       b2='',
                       b3='Reset',
                       lcdTxt=['',
                               'Start      Reset'],
                       ledStr=2,
                       ledBtn=[1,0,1]
        )
        joystick.stop_reading()

    def handleInput(self, button):
        if button == 1:
            mainWindow.startTimer()
            kendama.switchMode('ManualRunning')
        elif button == 3:
            mainWindow.resetTimer()
            kendama.switchMode('Manual')
        else:
            pass

class AIMode():

    def update(self):
        kendama.update(b1='Start',
                       b2='',
                       b3='Menu',
                       title='AI Solving Mode',
                       lcdTxt=['{}'.format(mainWindow.timerLabel.text()),
                               'Start       Menu'],
                       lcdCol=[0,255,0],
                       ledStr=1,
                       ledBtn=[1,0,1]
        )

    def handleInput(self, button):
        if button == 1:
            kendama.switchMode('AIRunning')
        elif button == 3:
            kendama.switchMode('Menu')
        else:
            pass

class CalibrationMode():

    def handleInput(self, button):
        pass

# Mode Manager Call
kendama = KENDAMA()

# Other Peripheral Calls
processor = IMAGEPROCESSOR()
pButtons = PHYSICALBUTTONS()
ledButtons = LEDBUTTONCONTROL()
lcd = LCD1602_WRITE()
ledStrip = LEDSTRIPCONTROL()
joystick = joystickControl.JOYSTICK_READ_DATA()
motors = PCA9685()

# Main PyQt Application Loop
app = QApplication(sys.argv)
screenWidth = app.primaryScreen().size().width()
screenHeight = app.primaryScreen().size().height()
mainWindow = App()
mainWindow.show()
kendama.currentMode.update()
sys.exit(app.exec_())