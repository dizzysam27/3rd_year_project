# General Imports
import sys
import cv2
import numpy as np
from gpiozero import Button # type: ignore

# PyQt5 Imports
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSlot, Qt, QTimer, QDateTime
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGridLayout, QPushButton, QHBoxLayout, QVBoxLayout, QPlainTextEdit

# Maze Game Module Imports
from maze_ball_detection_1_copy import ImageProcessor
from lcdControl import LCD1602_WRITE
from peripherals import LEDSTRIPCONTROL
from peripherals import LEDBUTTONCONTROL
import joystickControl
from motorControl import PCA9685

global screenWidth, screenHeight, aiControlFlag
aiControlFlag = False

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
        self.imageWidth = int(screenWidth * (2/3) + 20)
        self.imageHeight = int(self.imageWidth * (3/4))
        
        # Create main grid with camera feed size
        mainGrid = QGridLayout()
        self.setLayout(mainGrid)
        self.setStyleSheet('background-color: #A0A0A0')
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
        self.timerLabel.setStyleSheet('background-color: #A0A0A0; font: bold 100px')
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
        self.button1.clicked.connect(lambda : mode.currentMode.handleInput(1))
        self.button2.clicked.connect(lambda : mode.currentMode.handleInput(2))
        self.button3.clicked.connect(lambda : mode.currentMode.handleInput(3))

        # PWM Brightness Slider
        self.brightnessLabel = QLabel('Brightness Slider')
        self.brightnessLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.brightnessLabel.setStyleSheet('font: bold 25px')
        contentVBox.addWidget(self.brightnessLabel)

        brightnessHBox = QHBoxLayout()
        contentVBox.addLayout(brightnessHBox)

        brightnessZero = QLabel('0  ')
        brightnessZero.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        brightnessZero.setStyleSheet('font: bold 25px')
        brightnessMax = QLabel('  100')
        brightnessMax.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        brightnessMax.setStyleSheet('font: bold 25px')

        self.brightnessSlider = QSlider(Qt.Horizontal)
        self.brightnessSlider.setMinimum(0)
        self.brightnessSlider.setMaximum(100)
        self.brightnessSlider.setTickInterval(10)
        self.brightnessSlider.setTickPosition(QSlider.TicksBothSides)
        self.brightnessSlider.setSingleStep(10)
        self.brightnessSlider.setMinimumSize(300, 100)

        self.brightnessSlider.valueChanged.connect(self.brightnessChanged)

        brightnessHBox.addWidget(brightnessZero)
        brightnessHBox.addWidget(self.brightnessSlider, alignment=QtCore.Qt.AlignCenter)
        brightnessHBox.addWidget(brightnessMax)
        
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

        processor.xRate.connect(self.AIupdateX)
        processor.yRate.connect(self.AIupdateY)

        # Command Box
        self.commandBox = QPlainTextEdit('Initialising System...')
        self.commandBox.setStyleSheet('border: 2px solid black; font: 10px; background-color: #C0C0C0')
        self.commandBox.appendPlainText('Done!')
        contentVBox.addWidget(self.commandBox)

        joystick.printBuffer.connect(self.updateConsole)
        ledStrip.printBuffer.connect(self.updateConsole)
        processor.printBuffer.connect(self.updateConsole)
        motors.printBuffer.connect(self.updateConsole)

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
        motors.setServoPulse(1,x1+xRate/2)
        self.xRateLabel.setText('X: {}'.format(xRate))
    @pyqtSlot(int)
    def updateY(self, yRate):
        motors.setServoPulse(0,y1+yRate/2)
        self.yRateLabel.setText('Y: {}'.format(yRate))
    @pyqtSlot(int)
    def AIupdateX(self, xRate):
        if aiControlFlag == True: motors.setServoPulse(1,x1+xRate)
        else: pass
    @pyqtSlot(int)
    def AIupdateY(self, yRate):
        if aiControlFlag == True: motors.setServoPulse(0,y1+yRate)
        else: pass

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
    
    def brightnessChanged(self, value):
        self.updateConsole('New Brightness Value: {}'.format(value))
        arduinoValue = value + 100
        self.ledStrip.writeArduino(arduinoValue)

class PHYSICALBUTTONS():
    def __init__(self):
        self.pButton1 = Button(26, pull_up=True, bounce_time=0.1)
        self.pButton2 = Button(19, pull_up=True, bounce_time=0.1)
        self.pButton3 = Button(13, pull_up=True, bounce_time=0.1)

        self.pButton1.when_pressed = lambda : mode.currentMode.handleInput(1)
        self.pButton2.when_pressed = lambda : mode.currentMode.handleInput(2)
        self.pButton3.when_pressed = lambda : mode.currentMode.handleInput(3)

class MODE():
    def __init__(self):
        self.modes = {
            'Menu' : MenuMode(),
            'Manual' : ManualMode(),
            'ManualRunning' : ManualModeRunning(),
            'ManualStopped' : ManualModeStopped(),
            'AI' : AIMode(),
            'AIRunning' : AIModeRunning(),
            'Solved' : SolvedMaze()
        }

        self.currentMode = self.modes['Menu']

    # Switch Mode function called by each currenMode.handleInput()
    def switchMode(self, nextMode):
        if nextMode in self.modes:
            self.currentMode = self.modes[nextMode]
            self.currentMode.update()
        else: pass

    # Update Function called each currentMode.update(), changing all features on GUI and peripherals
    def update(self, title=None, b1=None, b2=None, b3=None, colour=None, lcdTxt=None):
        if title == None: pass
        else: mainWindow.modeLabel.setText(title)

        if b1 == None:
            mainWindow.buttonLabel1.setText('')
            mainWindow.button1.setStyleSheet('border-radius: 50px; border: 8px solid #C0C0C0; background-color: #C0C0C0')
            ledButtons.setLED(g=0)
        else:
            mainWindow.buttonLabel1.setText(b1)
            mainWindow.button1.setStyleSheet('border-radius: 50px; border: 8px solid green; background-color: #C0C0C0')
            ledButtons.setLED(g=1)

        if b2 == None:
            mainWindow.buttonLabel2.setText('')
            mainWindow.button2.setStyleSheet('border-radius: 50px; border: 8px solid #C0C0C0; background-color: #C0C0C0')
            ledButtons.setLED(r=0)
        else:
            mainWindow.buttonLabel2.setText(b2)
            mainWindow.button2.setStyleSheet('border-radius: 50px; border: 8px solid red; background-color: #C0C0C0')
            ledButtons.setLED(r=1)

        if b3 == None:
            mainWindow.buttonLabel3.setText('')
            mainWindow.button3.setStyleSheet('border-radius: 50px; border: 8px solid #C0C0C0; background-color: #C0C0C0')
            ledButtons.setLED(b=0)
        else:
            mainWindow.buttonLabel3.setText(b3)
            mainWindow.button3.setStyleSheet('border-radius: 50px; border: 8px solid blue; background-color: #C0C0C0')
            ledButtons.setLED(b=1)

        if colour == 'green':
            lcd.setRGB(0,255,0)
            ledStrip.writeArduino(1)
        elif colour == 'red':
            lcd.setRGB(255,0,0)
            ledStrip.writeArduino(2)
        elif colour == 'green':
            lcd.setRGB(0,0,255)
            ledStrip.writeArduino(3)
        elif colour == 'chase':
            lcd.setRGB(255,0,0)
            ledStrip.writeArduino(5)
        else:
            lcd.setRGB(255,255,255)
            ledStrip.writeArduino(4)

        if lcdTxt == None: pass
        else: lcd.update_messages(lcdTxt[0], lcdTxt[1])

# Each class is created with handleInput() and update() functions to update the UI and other peripherals

class MenuMode():
    def update(self):
        mainWindow.resetTimer()
        mode.update(title = 'Welcome to the Maze Game!',
                       b1 = 'AI',
                       b2 = 'Manual',
                       b3 = 'Calibrate',
                       lcdTxt = ['Main Menu',
                                 'AI   Manual  Cal']
        )

    def handleInput(self, button):
        if button == 1:
            mode.switchMode('AI')
        elif button == 2:
            mode.switchMode('Manual')
        elif button == 3:
            mode.switchMode('Calibrate')
        else: pass

class ManualMode():
    def update(self):
        mainWindow.resetTimer()
        mode.update(b1 = 'Start',
                       b3 = 'Menu',
                       colour = 'red',
                       lcdTxt = ['{}'.format(mainWindow.timerLabel.text()),
                                 'Start       Menu']
        )

    def handleInput(self, button):
        if button == 1:
            mode.switchMode('ManualRunning')
        elif button == 3:
            mode.switchMode('Menu')
        else: pass

class ManualModeRunning():
    def update(self):
        mainWindow.startTimer()
        joystick.start_reading()
        mode.update(title = 'Manual Solving Mode',
                       b2 = 'Stop',
                       colour = 'red',
                       lcdTxt = ['{}'.format(mainWindow.timerLabel.text()),
                                 '      Stop      ']
        )

    def handleInput(self, button):
        if button == 2:
            mode.switchMode('ManualStopped')
        else: pass

class ManualModeStopped():
    def update(self):
        mainWindow.stopTimer()
        joystick.stop_reading()
        mode.update(title = 'Manual Solving Mode',
                       b1 = 'Start',
                       b3 = 'Reset',
                       colour = 'red',
                       lcdTxt = ['{}'.format(mainWindow.timerLabel.text()),
                                 'Start      Reset']
        )

    def handleInput(self, button):
        if button == 1:
            mode.switchMode('ManualRunning')
        elif button == 3:
            mode.switchMode('Manual')
        else: pass

class AIMode():
    def update(self):
        mainWindow.stopTimer()
        mainWindow.resetTimer()
        aiControlFlag = False
        mode.update(title = 'AI Solving Mode',
                       b1 = 'Start',
                       b3 = 'Menu',
                       colour = 'green',
                       lcdTxt = ['{}'.format(mainWindow.timerLabel.text()),
                                 'Start       Menu']
        )

    def handleInput(self, button):
        if button == 1:
            mode.switchMode('AIRunning')
        elif button == 3:
            mode.switchMode('Menu')
        else: pass

class AIModeRunning():
    def update(self):
        mainWindow.startTimer()
        aiControlFlag = True
        mode.update(title = 'AI Solving Mode',
                       b2 = 'Stop',
                       colour = 'green',
                       lcdTxt = ['{}'.format(mainWindow.timerLabel.text()),
                                 '      Stop      ']
        )

    def handleInput(self, button):
        if button == 2:
            mode.switchMode('AI')
        else: pass

class SolvedMaze():
    def update(self):
        mainWindow.stopTimer()
        aiControlFlag = False
        mode.update(title = 'Maze Solved!',
                       b3 = 'Menu',
                       colour = 'chase',
                       lcdTxt = ['{}'.format(mainWindow.timerLabel.text()),
                                 '            Menu']
        )

    def handleInput(self, button):
        if button == 3:
            mode.switchMode('Menu')
        else: pass

def get_flat_values():
    defaultx = 1847
    defaulty = 1933


    motors.setServoPulse(0, int(defaulty))
    motors.setServoPulse(1, int(defaultx))

    return defaultx, defaulty

# Mode Manager Call
mode = MODE()

# Other Peripheral Calls
processor = ImageProcessor()
pButtons = PHYSICALBUTTONS()
ledButtons = LEDBUTTONCONTROL()
lcd = LCD1602_WRITE()
ledStrip = LEDSTRIPCONTROL()
joystick = joystickControl.JOYSTICK_READ_DATA()
motors = PCA9685()

x1,y1 = get_flat_values()

# Main PyQt Application Loop
app = QApplication(sys.argv)
screenWidth = app.primaryScreen().size().width()
screenHeight = app.primaryScreen().size().height()
mainWindow = App()
mainWindow.show()
mode.currentMode.update()
sys.exit(app.exec_())