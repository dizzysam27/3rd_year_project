import cv2
import numpy as np
import pickle  # For saving/loading last coordinates
import os
import time
import math
from simple_pid import PID
from PyQt5.QtCore import pyqtSignal, QThread

class ImageProcessor(QThread):
    cameraVideo = pyqtSignal(np.ndarray)
    printBuffer = pyqtSignal(str)
    xRate = pyqtSignal(int)
    yRate = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        self.sampled_points = self.load_last_coordinates()
        self.current_target_index = 0
        self.goal_reached = True
        self.PID_output_limits = 30

        # PID controllers for X and Y axes
        self.pid_x = PID(0.9, 0.05, 0.5)
        self.pid_y = PID(0.9, 0.05, 0.5)
        self.pid_x.output_limits = (-self.PID_output_limits, self.PID_output_limits)
        self.pid_y.output_limits = (-self.PID_output_limits, self.PID_output_limits)

        if not self.cap.isOpened():
            self.printBuffer.emit("Error: Could not open webcam.")
            exit()

    def load_last_coordinates(self):
        if os.path.exists("last_coordinates.pkl"):
            with open("last_coordinates.pkl", "rb") as f:
                return pickle.load(f)
        return []

    def save_last_coordinates(self):
        with open("last_coordinates.pkl", "wb") as f:
            pickle.dump(self.sampled_points, f)

    def crop_frame(self, frame):
        frame_height, frame_width = frame.shape[:2]
        crop_width, crop_height = 320, 240
        x_offset, y_offset = 10, -15

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
            if cv2.contourArea(largest_contour) > 10:
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    return (cx, cy)
        return None

    def move_motors(self, ball_center):
        if ball_center:
            bx, by = ball_center
            if abs(bx - self.gx) < 10 and abs(by - self.gy) < 10:
                self.goal_reached = True

            control_x = self.pid_x(bx)
            control_y = self.pid_y(by)
            print("x %s y %s" % (control_x, control_y))

            self.xRate.emit(control_x)
            self.yRate.emit(control_y)
        else:
            self.xRate.emit(0)
            self.yRate.emit(0)

    def update_goal_position(self):
        if self.goal_reached and self.current_target_index < len(self.sampled_points):
            self.gx, self.gy = self.sampled_points[self.current_target_index]
            self.current_target_index += 1
            self.goal_reached = False  
        elif self.current_target_index >= len(self.sampled_points):
            self.current_target_index = 0  

        self.pid_x.setpoint = self.gx
        self.pid_y.setpoint = self.gy

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.sampled_points.append((x, y))
            self.printBuffer.emit(f"Point added: {x}, {y}")

    def run(self):
        if self.sampled_points:
            choice = input("Use last saved coordinates? (y/n): ")
            if choice.lower() == 'y':
                self.printBuffer.emit(f"Using saved path points: {self.sampled_points}")
            else:
                self.sampled_points = []
                cv2.namedWindow("Select Path")
                cv2.setMouseCallback("Select Path", self.mouse_callback)

                while True:
                    ret, frame = self.cap.read()
                    if not ret:
                        self.printBuffer.emit("Error: Failed to capture frame.")
                        break

                    cropped_frame = self.crop_frame(frame)
                    for (x, y) in self.sampled_points:
                        cv2.circle(cropped_frame, (x, y), 5, (0, 0, 255), -1)

                    self.cameraVideo.emit(cropped_frame)

                self.printBuffer.emit(f"Selected path points: {self.sampled_points}")
                self.save_last_coordinates()
        
        self.current_target_index = 0  

        while True:
            ret, frame = self.cap.read()
            if not ret:
                self.printBuffer.emit("Error: Failed to capture frame.")
                break

            cropped_frame = self.crop_frame(frame)
            self.update_goal_position()
            ball_center = self.detect_light_blue(cropped_frame)
            self.printBuffer.emit(f"Ball: {ball_center}, Goal: ({self.gx}, {self.gy})")

            self.move_motors(ball_center)

            if ball_center:
                cv2.circle(cropped_frame, ball_center, 10, (0, 255, 0), -1)
            cv2.circle(cropped_frame, (self.gx, self.gy), 5, (0, 0, 255), -1)

            self.cameraVideo.emit(cropped_frame)

        self.cleanup()

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.printBuffer.emit("Cleaning up and exiting.")