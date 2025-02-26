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

        # Circle parameters
        self.center_x, self.center_y = 151, 126  # Center of the circular path
        self.radius = 60  # Radius of the circular path
        self.angle = 0  # Starting angle

        self.PID_output_limits = 50

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

    def move_motors(self, ball_center):
        if ball_center:
            bx, by = ball_center
            distance_to_goal = np.sqrt((bx - self.gx) ** 2 + (by - self.gy) ** 2)

            # Stop motors when close enough to the goal
            if abs(bx - self.gx) < 1 and abs(by - self.gy) < 1:
                self.motors.setServoPulse(1, self.defaultx)
                self.motors.setServoPulse(0, self.defaulty)
                return

            # Reduce motor sensitivity as the ball nears the goal
            sensitivity_factor = max(0.1, min(1.0, distance_to_goal / 50))
            print(sensitivity_factor)

            control_x = self.pid_x(bx)
            control_y = self.pid_y(by) 

            self.motors.setServoPulse(1, int(self.defaultx + control_x))
            self.motors.setServoPulse(0, int(self.defaulty + control_y))
        else:
            self.motors.setServoPulse(1, self.defaultx)
            self.motors.setServoPulse(0, self.defaulty)

    def update_goal_position(self):
        """Update goal position along a circular path."""
        self.angle += 0.01  # Speed of movement (adjust as needed)
        if self.angle >= 2 * math.pi:
            self.angle = 0  # Reset angle after a full rotation

        self.gx = int(self.center_x + self.radius * math.cos(self.angle))
        self.gy = int(self.center_y + self.radius * math.sin(self.angle))

        # Update PID setpoints dynamically
        self.pid_x.setpoint = self.gx
        self.pid_y.setpoint = self.gy


    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break

            self.update_goal_position()  # Update goal position dynamically
            cropped_frame = self.crop_frame(frame)
            ball_center = self.detect_light_blue(cropped_frame)
            print(f"Ball: {ball_center}, Goal: ({self.gx}, {self.gy})")

            self.move_motors(ball_center)

            # Show camera feed with detected ball and goal position
            if ball_center:
                cv2.circle(cropped_frame, ball_center, 10, (0, 255, 0), -1)  # Green for ball
            cv2.circle(cropped_frame, (self.gx, self.gy), 5, (0, 0, 255), -1)  # Red for moving goal
            cv2.imshow("Tracking", cropped_frame)

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
