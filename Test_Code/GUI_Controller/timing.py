# General Imports
import sys
import cv2
import numpy as np
import time

# PyQt5 Imports
from PyQt5.QtCore import pyqtSignal

class Timer:
    timerString = pyqtSignal(np.ndarray)

    def __init__(self):
        self.startTime = None
    
    def formatTime(self, time):
        minutes = int(time // 60)
        seconds = int(time % 60)
        milliseconds = int((time % 1) * 1000)
        return f"{minutes:02}:{seconds:02}:{milliseconds:03}"

    def startTimer(self):
        self.startTime = time.time()
        self.startFlag = True

    def stopTimer(self):
        self.startFlag = False

    def resetTimer(self):
        self.elapsedTime = self.format(0)
        self.timerString.emit(self.elapsedTime)
    
    def runTimer(self):
        if self.startFlag == True:
            self.elapsedTime = self.format(time.time() - self.startTime)
            self.timerString.emit(self.elapsedTime)
        else:
            pass
    
        