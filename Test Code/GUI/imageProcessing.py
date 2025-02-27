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
    
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        if not self.cap.isOpened():
            print("Error: Could not open webcam")
            exit()
            
    def run(self):
        while True:
            ret, self.frame = self.cap.read()
            if not ret:
                print("Error: Failed to capture frame")
                break
                
            cv2.circle(self.frame, (100,100), 10, (0,255,0), -1)
            cv2.imshow("Tracking", self.frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cleanup()

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()
        print("Cleaning up and exiting")

class ImageBuffer(QThread):

    bufferFrame = pyqtSignal(np.ndarray)

    def run(self, processor):
        while True:
            nextFrame = processor.frame
            self.bufferFrame.emit(nextFrame)

processor = ImageProcessor()
buffer = ImageBuffer()
processor.run()
buffer.run()