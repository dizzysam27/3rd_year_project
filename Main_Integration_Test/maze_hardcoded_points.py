import cv2
import numpy as np
import time
import math
from simple_pid import PID
from Peripherals.Motor_Control import PCA9685
from center_maze import get_flat_values

class ImageProcessor:
    def __init__(self):
        self.motors = PCA9685()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        flat_x, flat_y = get_flat_values()
        self.defaultx = flat_x
        self.defaulty = flat_y
        
        self.sampled_points = []  # Store detected path points
        self.current_target_index = 0  # Index for tracking movement along the path
        self.goal_reached = True  # Track if the ball has reached the goal before moving
        
        self.PID_output_limits = 30

        # PID controllers for X and Y axes
        self.pid_x = PID(0.8, 0.05, 0.3)
        self.pid_y = PID(0.8, 0.05, 0.3)
        self.pid_x.output_limits = (-self.PID_output_limits, self.PID_output_limits)
        self.pid_y.output_limits = (-self.PID_output_limits, self.PID_output_limits)

        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            exit()

    def crop_frame(self, frame):
        frame_height, frame_width = frame.shape[:2]
        crop_width, crop_height = 320, 220
        x_offset, y_offset = 10, 0

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

    def move_motors(self, ball_center):
        if ball_center:
            bx, by = ball_center
            distance_to_goal = np.sqrt((bx - self.gx) ** 2 + (by - self.gy) ** 2)

            if abs(bx - self.gx) < 20 and abs(by - self.gy) < 20:
                self.goal_reached = True

            #sensitivity_factor = max(0.1, min(1.0, distance_to_goal / 50))
            control_x = self.pid_x(bx)
            control_y = self.pid_y(by) 

            self.motors.setServoPulse(1, int(self.defaultx + control_x))
            self.motors.setServoPulse(0, int(self.defaulty + control_y))
        else:
            self.motors.setServoPulse(1, self.defaultx)
            self.motors.setServoPulse(0, self.defaulty)

    def update_goal_position(self):
        if self.goal_reached and self.current_target_index < len(self.sampled_points):
            self.gx, self.gy = self.sampled_points[self.current_target_index]
            self.current_target_index += 1  # Move to next point
            self.goal_reached = False  # Wait for ball to reach before moving again
        elif self.current_target_index >= len(self.sampled_points):
            self.current_target_index = 0  # Restart path

        self.pid_x.setpoint = self.gx
        self.pid_y.setpoint = self.gy

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
        ret, frame = self.cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            return

        cropped_frame = self.crop_frame(frame)
        self.sampled_points = self.find_line(cropped_frame)
        self.current_target_index = 0  # Reset path tracking

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break

            cropped_frame = self.crop_frame(frame)
            self.update_goal_position()
            ball_center = self.detect_light_blue(cropped_frame)
            print(f"Ball: {ball_center}, Goal: ({self.gx}, {self.gy})")

            self.move_motors(ball_center)

            if ball_center:
                cv2.circle(cropped_frame, ball_center, 10, (0, 255, 0), -1)
            cv2.circle(cropped_frame, (self.gx, self.gy), 5, (0, 0, 255), -1)
            cv2.imshow("Tracking", cropped_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cleanup()

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()
        print("Cleaning up and exiting.")

processor = ImageProcessor()
processor.run()
