import cv2
import numpy as np
import time
import math
from PyQt5 import QtGui
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
import sys

class ImageProcessor:
            
    def run(self, inputFrame):
        modifiedFrame = inputFrame
        cv2.circle(modifiedFrame, (100,100), 10, (0,255,0), -1)
        return modifiedFrame