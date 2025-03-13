import cv2
import numpy as np
import time
import math
from PyQt5 import QtGui
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
import sys

global xRate, yRate
xRate = 0
yRate = 0

class IMAGEPROCESSOR(QThread):
    cameraVideo = pyqtSignal(np.ndarray)

    def __init__(self):
        # Inherit QThread features
        super().__init__()

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            exit()

    def crop_frame(self, frame):
        frame_height, frame_width = frame.shape[:2]
        crop_width, crop_height = 320, 220
        x_offset, y_offset = 50, 40

        start_x = (frame_width - crop_width) // 2
        end_x = start_x + crop_width
        start_y = (frame_height - crop_height) // 2
        end_y = start_y + crop_height

        return frame[start_y + y_offset:end_y + y_offset, start_x + x_offset:end_x + x_offset]

    def detect_light_blue(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv = cv2.GaussianBlur(hsv, (5, 5), 0)
        lower_blue, upper_blue = np.array([100, 100, 100]), np.array([130, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) > 100:
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    return (cx, cy)
        return None

    def find_line(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

        kernel = np.ones((5, 5), np.uint8)
        morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        morph = cv2.dilate(morph, kernel, iterations=1)

        contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return []
        
        contour = max(contours, key=lambda c: cv2.arcLength(c, True))
        contour_points = contour.reshape(-1, 2)
        num_points = 100
        indices = np.linspace(0, len(contour_points) - 1, num_points, dtype=int)
        sampled_points = contour_points[indices]
        
        for (x, y) in sampled_points:
            cv2.circle(image, (x, y), 3, (0, 0, 255), -1)

        cv2.imshow("Detected Path", image)
        return sampled_points

    def run(self):
        # capture from web cam
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            cropped_frame = self.crop_frame(frame)
            ball_center = self.detect_light_blue(cropped_frame)

            if ball_center:
                cv2.circle(cropped_frame, ball_center, 10, (0, 255, 0), -1)
            cv2.circle(cropped_frame, (100,100), 5, (0,0,255), -1)

            self.cameraVideo.emit(frame)

        self.cleanup()

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()
        print("Cleaning up and exiting.")