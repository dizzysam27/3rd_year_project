import cv2
import numpy as np
import time
import math
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSignal

class ImageProcessor:

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # Circle parameters
        self.center_x, self.center_y = 151, 126  # Center of the circular path
        self.radius = 60  # Radius of the circular path
        self.angle = 0  # Starting angle

        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            exit()

    def crop_frame(self, frame):
        frame_height, frame_width = frame.shape[:2]
        crop_width, crop_height = 310, 260
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

    def run(self):
        while True:
            self.ret, self.frame = self.cap.read()
            if not self.ret:
                print("Error: Failed to capture frame.")
                break

            self.cropped_frame = self.crop_frame(self.frame)
            ball_center = self.detect_light_blue(self.cropped_frame)

            # Show camera feed with detected ball and goal position
            if ball_center:
                cv2.circle(self.cropped_frame, ball_center, 10, (0, 255, 0), -1)  # Green for ball
            cv2.circle(self.cropped_frame, (100, 100), 5, (0, 0, 255), -1)  # Red for moving goal

            cv2.imshow("Tracking", self.cropped_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cleanup()

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()
        print("Cleaning up and exiting.")

# Run the processor
processor = ImageProcessor()
processor.run()