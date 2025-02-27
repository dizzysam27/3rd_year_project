from PyQt5 import QtWidgets
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtCore import QThread, pyqtSignal as Signal, pyqtSlot as Slot
import cv2
import sys
from GUI import MyThread

cap = cv2.VideoCapture(0)
while cap.isOpened():
    _,testFrames = cap.read()
    moddedFrames = cv2.line(testFrames, (100,100), (300,300), (0,255,0), 10)
    MyThread.run(moddedFrames)
