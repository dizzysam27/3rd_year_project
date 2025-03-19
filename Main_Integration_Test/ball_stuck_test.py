import cv2
import numpy as np
import pickle  # For saving/loading last coordinates
import os
import time
import math
from simple_pid import PID
from Peripherals.Motor_Control import PCA9685
from center_maze import get_flat_values
import PyQt5
from PyQt5.QtCore import pyqtSignal, QThread

class ImageProcessor:


    def __init__(self):

        self.motors = PCA9685()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        flat_x, flat_y = get_flat_values()
        self.defaultx = flat_x
        self.defaulty = flat_y
        
        self.sampled_points = self.load_last_coordinates()
        self.current_target_index = 0
        self.goal_reached = True
        self.PID_output_limits =  40

        # PID controllers for X and Y axes
        Px_static, Py_static = 0.3,0.7
        self.pid_x = PID(Px, 0.05, 0.5)
        self.pid_y = PID(Py, 0.05, 0.3)
        self.pid_x.output_limits = (-self.PID_output_limits, self.PID_output_limits)
        self.pid_y.output_limits = (-self.PID_output_limits, self.PID_output_limits)

        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
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
        crop_width, crop_height = 310, 230
        x_offset, y_offset = 10, -15

        start_x = (frame_width - crop_width) // 2
        end_x = start_x + crop_width
        start_y = (frame_height - crop_height) // 2
        end_y = start_y + crop_height

        return frame[start_y + y_offset:end_y + y_offset, start_x + x_offset:end_x + x_offset]

    def detect_ball(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv = cv2.GaussianBlur(hsv, (5, 5), 0)
        lower_blue, upper_blue = np.array([140,80, 80]), np.array([175, 175, 255])
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
    def ball_speed(self, ball_center):
        if ball_center:
            prev_cx, prev_cy = cx , cy
            cx, cy = ball_center
            for i in range(5):
                try:
                    prev_ball_speed(6-i) = prev_ball_speed(5-i)
                else:
                    prev_ball_speed(6-i) = 0
            prev_ball_speed(0) = math.sqrt((cx - prev_cx)**2 + (cy - prev_cy)**2)
            speed = sum(prev_ball_speed)/6
            print(speed)
            return speed


    def move_motors(self, ball_center):
        if ball_center:
            bx, by = ball_center
            if abs(bx - self.gx) < 10 and abs(by - self.gy) < 10:
                self.goal_reached = True

            control_x = self.pid_x(bx)
            control_y = self.pid_y(by)
            print("x %s y %s" % (control_x, control_y))
            
            
            if abs(bx - self.gx) < 10:
                 self.motors.setServoPulse(1, int(self.defaultx))
            else:
                self.motors.setServoPulse(1, int(self.defaultx + control_x))
    
            if abs(by - self.gy) < 10:
                 self.motors.setServoPulse(0, int(self.defaulty))
            else:
                self.motors.setServoPulse(0, int(self.defaulty + control_y))

        else:
            self.motors.setServoPulse(1, self.defaultx)
            self.motors.setServoPulse(0, self.defaulty)

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
            print(f"Point added: {x}, {y}")

    def run(self):
        if self.sampled_points:
            choice = input("Use last saved coordinates? (y/n): ")
            if choice.lower() == 'y':
                print(f"Using saved path points: {self.sampled_points}")
            else:
                self.sampled_points = []
                cv2.namedWindow("Select Path")
                cv2.setMouseCallback("Select Path", self.mouse_callback)

                while True:
                    ret, frame = self.cap.read()
                    if not ret:
                        print("Error: Failed to capture frame.")
                        break

                    cropped_frame = self.crop_frame(frame)
                    for (x, y) in self.sampled_points:
                        cv2.circle(cropped_frame, (x, y), 5, (0, 0, 255), -1)

                    cv2.imshow("Select Path", cropped_frame)

                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('s') and self.sampled_points:
                        break

                print(f"Selected path points: {self.sampled_points}")
                self.save_last_coordinates()
        
        self.current_target_index = 0  

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break

            cropped_frame = self.crop_frame(frame)
            self.update_goal_position()
            ball_center= self.detect_ball(cropped_frame)
            print(f"Ball: {ball_center}, Goal: ({self.gx}, {self.gy})")

            ball_speed = self.ball_speed(ball_center)
            Px_correction, Py_correction = (((0.95-Px_static)/(0.001+ball_speed*10)), (((0.95-Py_static)/(0.001+ball_speed*10))
            Px , Py = Px_static + Px_correction, Py_static + Py_correction
            self.move_motors(ball_center)

            if ball_center:
                cv2.circle(cropped_frame, ball_center, 3, (0, 0, 255), -1)
            cv2.circle(cropped_frame, (self.gx, self.gy), 5, (0, 0, 255), -1)

            
            cv2.imshow("Tracking", cropped_frame)
            if cv2.waitKey(1) & 0xFF == ord('r'):
                self.current_target_index = 0
                self.goal_reached = True
                print("reset")
               
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.motors.setServoPulse(1, self.defaultx)
                self.motors.setServoPulse(0, self.defaulty)
                break
          
                

        self.cleanup()

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()
        print("Cleaning up and exiting.")

processor = ImageProcessor()
processor.run()
