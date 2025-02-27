import cv2
import numpy as np
import heapq
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
        
        self.sampled_points = []  # Store path points from A*
        self.current_target_index = 0
        self.goal_reached = True
        self.PID_output_limits = 30

        self.pid_x = PID(0.8, 0.05, 0.3)
        self.pid_y = PID(0.8, 0.05, 0.3)
        self.pid_x.output_limits = (-self.PID_output_limits, self.PID_output_limits)
        self.pid_y.output_limits = (-self.PID_output_limits, self.PID_output_limits)

        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            exit()

    def crop_frame(self, frame):
        return frame[40:260, 50:370]

    def detect_light_blue(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_blue, upper_blue = np.array([100, 100, 100]), np.array([130, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest) > 100:
                M = cv2.moments(largest)
                if M["m00"] != 0:
                    return (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        return None

    def a_star(self, start, goal, maze):
        rows, cols = maze.shape
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
        open_set = [(0, start)]
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}
        heapq.heapify(open_set)
        
        while open_set:
            _, current = heapq.heappop(open_set)
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path
            
            for dx, dy in directions:
                neighbor = (current[0] + dx, current[1] + dy)
                if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor] == 0:
                    temp_g = g_score[current] + 1
                    if neighbor not in g_score or temp_g < g_score[neighbor]:
                        g_score[neighbor] = temp_g
                        f_score[neighbor] = temp_g + heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
                        came_from[neighbor] = current
        return []

    def find_maze_path(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
        maze = (binary // 255).astype(np.uint8)
        if self.ball_pos and hasattr(self, "gx") and hasattr(self, "gy"):
            start = (self.ball_pos[1], self.ball_pos[0])
            goal = (self.gy, self.gx)
            return [(x, y) for y, x in self.a_star(start, goal, maze)]
        return []

    def move_motors(self, ball_center):
        if ball_center:
            bx, by = ball_center
            distance_to_goal = np.linalg.norm([bx - self.gx, by - self.gy])
            if distance_to_goal < 20:
                self.goal_reached = True
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
            self.current_target_index += 1
            self.goal_reached = False
        elif self.current_target_index >= len(self.sampled_points):
            self.current_target_index = 0
        self.pid_x.setpoint = self.gx
        self.pid_y.setpoint = self.gy

    def run(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            return
        
        cropped = self.crop_frame(frame)
        self.ball_pos = self.detect_light_blue(cropped)
        self.sampled_points = self.find_maze_path(cropped)
        self.current_target_index = 0
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break
            cropped = self.crop_frame(frame)
            self.update_goal_position()
            self.ball_pos = self.detect_light_blue(cropped)
            self.move_motors(self.ball_pos)
            
            if self.ball_pos:
                cv2.circle(cropped, self.ball_pos, 10, (0, 255, 0), -1)
            cv2.circle(cropped, (self.gx, self.gy), 5, (0, 0, 255), -1)
            cv2.imshow("Tracking", cropped)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cleanup()

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()
        print("Cleaning up and exiting.")

processor = ImageProcessor()
processor.run()
