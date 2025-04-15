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
from collections import deque
import argparse

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
        self.output_limits =  40
        self.last_location = [120, 213]
        self.last_motor_control = [self.defaultx,self.defaulty]
        self.new_motor_control = [0,0]
    

        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video",
            help="path to the (optional) video file")
        ap.add_argument("-b", "--buffer", type=int, default=64,
            help="max buffer size")
        self.args = vars(ap.parse_args())
        self.ballpts = deque(maxlen=self.args["buffer"])

        # PID controllers for X and Y axe
        self.PID_VALUES = [14,1,3]
        self.pid_x = PID(self.PID_VALUES[0],self.PID_VALUES[1],self.PID_VALUES[2])
        self.pid_y = PID(self.PID_VALUES[0],self.PID_VALUES[1],self.PID_VALUES[2])
        # self.pid_x.proportional_on_measurement = True
        # self.pid_y.proportional_on_measurement = True

        self.pid_x.output_limits = (-self.output_limits, self.output_limits)
        self.pid_y.output_limits = (-self.output_limits, self.output_limits)

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
        crop_width, crop_height = 280, 210
        x_offset, y_offset = 10, -10

        start_x = (frame_width - crop_width) // 2
        end_x = start_x + crop_width
        start_y = (frame_height - crop_height) // 2
        end_y = start_y + crop_height

        return frame[start_y + y_offset:end_y + y_offset, start_x + x_offset:end_x + x_offset]

    def detect_light_blue(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Define the color range for the ball (e.g., red ball)
        # Define the color range for the ball (e.g., red ball)
        lower_rgb = np.array([50, 100, 20])
        upper_rgb = np.array([150, 255, 100])

        # Create a mask to isolate the ball's color in RGB
        rgb_mask = cv2.inRange(frame, lower_rgb, upper_rgb)

        # Find contours from the mask
        contours, _ = cv2.findContours(rgb_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        largest_circle = None
        largest_radius = 0

        # Loop through the contours to detect the largest valid circle
        for contour in contours:
            if 5 < cv2.contourArea(contour) < 20:  # Filter small contours
                (x, y), radius = cv2.minEnclosingCircle(contour)
                radius = int(radius)

                if 1 < radius < 10 and radius > largest_radius:  # Track the largest valid circle
                    largest_circle = (int(x), int(y))
                    largest_radius = radius

        # Draw the largest circle if found
        if largest_circle is not None:
            cv2.circle(frame, largest_circle, largest_radius, (0, 255, 0), 2)
            cv2.putText(frame, "Largest Ball", (largest_circle[0] - largest_radius, largest_circle[1] - largest_radius - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            M = cv2.moments(largest_circle)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                self.last_location[0] = int(M["m10"] / M["m00"])
                self.last_location[1] = int(M["m01"] / M["m00"])
                return (cx, cy)       
        else:
            cx = self.last_location[0]
            cy = self.last_location[1]
        return None
    
    

    def move_motors(self, ball_center):
        if ball_center:
            bx, by = ball_center
            if abs(bx - self.gx) < 15 and abs(by - self.gy) < 12:
                self.goal_reached = True

          
            control_x = self.pid_x(bx)
            control_y = self.pid_y(by)
            print("x %s y %s" % (control_x, control_y))
            
            
            # if abs(bx - self.gx) < 10:
            #      self.motors.setServoPulse(1, int(self.defaultx))
            # else:
            #     self.motors.setServoPulse(1, int(self.defaultx + control_x))
    
            # if abs(by - self.gy) < 10:
            #      self.motors.setServoPulse(0, int(self.defaulty))
            # else:
            #     self.motors.setServoPulse(0, int(self.defaulty + control_y))

            # self.motors.setServoPulse(0, int(self.defaulty + control_y))
            # self.motors.setServoPulse(1, int(self.defaultx + control_x))
            self.new_motor_control[0] = self.defaultx + control_x
            self.new_motor_control[1] = self.defaulty + control_y

        else:
            self.new_motor_control[0] = self.defaultx
            self.new_motor_control[1] = self.defaulty

        if self.new_motor_control[0] == self.last_motor_control[0]:
            pass
        else:
            self.motors.setServoPulse(1, self.new_motor_control[0])
            self.last_motor_control[0] = self.new_motor_control[0]

        if self.new_motor_control[1] == self.last_motor_control[1]:
            pass
        else:
            self.motors.setServoPulse(0, self.new_motor_control[1])
            self.last_motor_control[1] = self.new_motor_control[1]


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
        self.motors.setServoPulse(1, self.defaultx)
        self.motors.setServoPulse(0, self.defaulty)
        
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
            ball_center = self.detect_light_blue(cropped_frame)
            self.update_goal_position()
            print(f"Ball: {ball_center}, Goal: ({self.gx}, {self.gy})")

            self.move_motors(ball_center)

            if ball_center:
                cv2.circle(cropped_frame, ball_center, 3, (0, 0, 255), -1)
                self.ballpts.appendleft(ball_center)
                for i in range(1, len(self.ballpts)):
                    # if either of the tracked points are None, ignore
                    # them
                    if self.ballpts[i - 1] is None or self.ballpts[i] is None:
                        continue
                    # otherwise, compute the thickness of the line and
                    # draw the connecting lines
                    thickness = int(np.sqrt(self.args["buffer"] / float(i + 1)) * 2.5)
                    cv2.line(cropped_frame, self.ballpts[i - 1], self.ballpts[i], (0, 0, 255), thickness)


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