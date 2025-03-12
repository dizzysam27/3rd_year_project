# General Imports
import sys
import cv2
import numpy as np
from gpiozero import Button # type: ignore

# PyQt5 Imports
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QTimer, QDateTime
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGridLayout, QPushButton, QHBoxLayout

# Maze Game Module Imports
from imageProcessing import IMAGEPROCESSOR
from lcdControl import LCD1602_WRITE
from peripherals import LEDSTRIPCONTROL
from peripherals import LEDBUTTONCONTROL

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
        self.button1 = QPushButton('AI')
        self.button2 = QPushButton('Manual')
        self.button3 = QPushButton('Cal.')
        hBoxLayout.addWidget(self.button1)
        hBoxLayout.addWidget(self.button2)
        hBoxLayout.addWidget(self.button3)
        self.button1.clicked.connect(lambda : kendama.currentMode.handleInput(1))
        self.button2.clicked.connect(lambda : kendama.currentMode.handleInput(2))
        self.button3.clicked.connect(lambda : kendama.currentMode.handleInput(3))

        # Flags for Manual/AI Mode
        self.joystickFlag = 0
        self.aiFlag = 0

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
            lcd.update_messages(self.TimerLabel.text(), "")
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
        self.TimerLabel.setText('Time: {:02d}:{:02d}.{:01d}'.format(self.minCount, self.secCount, self.tenCount))

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
        else: mainWindow.button1.setText(b1)
        if b2 == None: pass
        else: mainWindow.button2.setText(b2)
        if b3 == None: pass
        else: mainWindow.button3.setText(b3)
        if title == None: pass
        else: mainWindow.TitleLabel.setText(title)
        if lcdTxt == None: pass
        else: lcd.update_messages(lcdTxt[0], lcdTxt[1])
        if lcdCol == None: pass
        else: lcd.setRGB(lcdCol[0], lcdCol[1], lcdCol[2])
        if ledStr == None: pass
        else: ledStrip.writeArduino(ledStr)
        if ledBtn == None: pass
        else: ledButtons.setLED(ledBtn[0], ledBtn[1], ledBtn[2])

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
                       lcdTxt=['{}'.format(mainWindow.TimerLabel.text()),
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
        mainWindow.joystickFlag = 1

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
                       ledStr=2
        )

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
                       lcdTxt=['{}'.format(mainWindow.TimerLabel.text()),
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

# Main PyQt Application Loop
while True:
    app = QApplication(sys.argv)
    mainWindow = App()
    mainWindow.show()
    sys.exit(app.exec_())