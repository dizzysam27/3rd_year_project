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
from a_star_mostrecent import MazeSolver

class ImageProcessor:


    def __init__(self):

        self.motors = PCA9685()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        flat_x, flat_y = get_flat_values()
        self.defaultx = flat_x
        self.defaulty = flat_y
        
        self.sampled_points = self.load_last_coordinates()
        self.current_target_index = 0
        self.goal_reached = True

        self.default_limits_x = 18
        self.default_limits_y = 15
        self.output_limits =  self.default_limits_x
        self.output_limitsy =  self.default_limits_y
        self.last_location = [133, 249]
        self.last_motor_control = [self.defaultx,self.defaulty]
        self.new_motor_control = [0,0]

        self.reached_distance = 22
        self.motorcounter = 0
        self.lastinput = [0,0]

        self.balltracker = [0,0]
        self.balltrackercounter = 0
        self.boosted = 0

        self.line_points = np.zeros(shape=(400,2))

        
        

        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video",
            help="path to the (optional) video file")
        ap.add_argument("-b", "--buffer", type=int, default=64,
            help="max buffer size")
        self.args = vars(ap.parse_args())
        self.ballpts = deque(maxlen=self.args["buffer"])

        # PID controllers for X and Y axes
        self.PID_VALUES = [9,0,3]
        self.PID_VALUESy = [9,0,3]
        self.pid_x = PID(self.PID_VALUES[0],self.PID_VALUES[1],self.PID_VALUES[2])
        self.pid_y = PID(self.PID_VALUESy[0],self.PID_VALUESy[1],self.PID_VALUESy[2])
        # self.pid_x.proportional_on_measurement = True
        # self.pid_y.proortional_on_measurement = True

        self.pid_x.output_limits = (-self.output_limits, self.output_limits)
        self.pid_y.output_limits = (-self.output_limitsy, self.output_limitsy)

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
        crop_width, crop_height = 370, 280
        x_offset, y_offset = 10, -10

        start_x = (frame_width - crop_width) // 2
        end_x = start_x + crop_width
        start_y = (frame_height - crop_height) // 2
        end_y = start_y + crop_height

        return frame[start_y + y_offset:end_y + y_offset, start_x + x_offset:end_x + x_offset]
    
    def rotate_frame(self, image):
        # Define three source points (e.g., corners of a triangle in the original image)
        src_pts = np.float32([[10, 10], [305, 13], [15, 235]])

        # Define three corresponding destination points (where you want those points to map)
        dst_pts = np.float32([[0, 0], [310, 0], [0, 250]])

        # Get the affine transformation matrix
        M = cv2.getAffineTransform(src_pts, dst_pts)

        # Apply the affine transformation
        rows, cols, _ = image.shape
        transformed_img = cv2.warpAffine(image, M, (cols, rows))
        
        # return transformed_img
        return image

    def detect_ball(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv = cv2.GaussianBlur(hsv, (5, 5), 0)
        lower_red, upper_red = np.array([120,50, 80]), np.array([255,255, 159])
        mask = cv2.inRange(hsv, lower_red, upper_red)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) > 10:
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    self.last_location[0] = int(M["m10"] / M["m00"])
                    self.last_location[1] = int(M["m01"] / M["m00"])

                    if self.balltrackercounter == 0:
                        self.balltracker[0] = int(M["m10"] / M["m00"])
                        self.balltracker[1] = int(M["m01"] / M["m00"])



                    if self.balltrackercounter == 10:
                        if self.balltracker[0] == cx and self.balltracker[1] == cy:
                            self.output_limits = 30
                            self.output_limitsy = 30
                            print('boosted')
                            self.boosted = 1
                            cx = 0
                            cy = 0
                            if self.current_target_index < 4:
                                self.current_target_index = 0
                            else:
                                self.current_target_index = self.current_target_index - 4
                                self.goal_reached = True

                    if self.balltrackercounter == 14:
                        if self.boosted == 1:
                            self.output_limitsy = self.default_limits_y
                            self.output_limits = self.default_limits_x
                            print('normal')
                        self.balltrackercounter = -1
                        self.balltracker = [0,0]
                        self.boosted = 0
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])

                    self.balltrackercounter += 1
                    self.pid_x.output_limits = (-self.output_limits, self.output_limits)
                    self.pid_y.output_limits = (-self.output_limitsy, self.output_limitsy)
                    return (cx, cy)
                
        else:
            cx = self.last_location[0]
            cy = self.last_location[1]
        return None
    
    def find_and_fill_contours(self, mask, frame):
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        filled_frame = frame.copy()
        for contour in contours:
            area = cv2.contourArea(contour)
            largest_contour = max(contours, key=cv2.contourArea)
        

            x, y, w, h = cv2.boundingRect(largest_contour)
            cx, cy = x + w // 2, y + h // 2
            cv2.drawContours(filled_frame, [largest_contour], -1, (0, 255, 0), thickness=cv2.FILLED)
        return filled_frame, contours
    import numpy as np

    def reorder_line_to_start(self, line_points, start):
        # line_points: np.array of shape (N, 2)
        distances = np.linalg.norm(line_points - start, axis=1)
        start_idx = np.argmin(distances)

        # Rotate using np.concatenate instead of +
        return np.concatenate((line_points[start_idx:], line_points[:start_idx]), axis=0)

    def detect_line(self, frame):
        cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX)

        lower_blue, upper_blue = np.array([157,121,58]), np.array([255,198,166])
        bmask = cv2.inRange(frame, lower_blue, upper_blue)

        gfilled_frame, gcontours = self.find_and_fill_contours(bmask, frame)

        if gcontours:
            # Get the largest contour
            contour = max(gcontours, key=cv2.contourArea)

            # Approximate the contour for simplicity
            epsilon = 0.001 * cv2.arcLength(contour, False)
            approx = cv2.approxPolyDP(contour, epsilon, False)
            points = approx.reshape(-1, 2)

            # Compute distances between points to get total curve length
            distances = np.cumsum(
                [0] + [np.linalg.norm(points[i] - points[i - 1]) for i in range(1, len(points))]
            )
            total_length = distances[-1]

            # Normalize distances to [0, 1]
            distances /= total_length

            # Interpolate 100 evenly spaced points
            num_points = 400
            evenly_spaced_alphas = np.linspace(0, 1, num_points)
            interpolated_points = []

            for alpha in evenly_spaced_alphas:
                idx = np.searchsorted(distances, alpha)
                if idx == 0:
                    interpolated_points.append(points[0])
                elif idx >= len(points):
                    interpolated_points.append(points[-1])
                else:
                    t = (alpha - distances[idx - 1]) / (distances[idx] - distances[idx - 1])
                    interp_point = (1 - t) * points[idx - 1] + t * points[idx]
                    interpolated_points.append(interp_point)

            interpolated_points = np.array(interpolated_points, dtype=int)

            # Draw points on the frame
            for (x, y) in interpolated_points:
                cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)

            # print coordinates
            print("Sampled 100 points:", interpolated_points)

        return interpolated_points


    def move_motors(self, ball_center):
        if ball_center:
            self.motorcounter += 1
            bx, by = ball_center
            if abs(bx - self.gx) < self.reached_distance and abs(by - self.gy) < self.reached_distance:
                self.goal_reached = True

            
            control_x = self.pid_x(bx)
            control_y = self.pid_y(by)
            print("x %s y %s" % (control_x, control_y))
            if self.motorcounter == 1:
                self.lastinput = [control_x, control_y]
            elif self.motorcounter > 30:
                if [control_x,control_y] == self.lastinput:
                    print('ballstuck')
                    # self.motors.setServoPulse(0, self.defaulty)
                    # self.motors.setServoPulse(1, self.defaultx)

                self.motorcounter = 1
                self.lastinput = [control_x, control_y]

                    
            
            
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
       
        # if self.motorcounter > 60:   
        #     self.motors.setServoPulse(0, self.defaulty)
        #     self.motors.setServoPulse(1, self.defaultx)
        #     self.motorcounter = 0

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

    def run(self, waypoints):
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
                    cropped_frame = self.rotate_frame(cropped_frame)
             
                    for (x, y) in self.sampled_points:
                        cv2.circle(cropped_frame, (x, y), 5, (0, 0, 255), -1)
        

                    cv2.imshow("Select Path", cropped_frame)

                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('s') and self.sampled_points:
                        break

                print(f"Selected path points: {self.sampled_points}")
                self.save_last_coordinates()
        
        self.motors.setServoPulse(1, self.defaultx)
        self.motors.setServoPulse(0, self.defaulty)
        self.current_target_index = 0  
        

        # print('5')
        # time.sleep(1)
        # print('4')
        # time.sleep(1)
        # print('3')
        # time.sleep(1)
        # print('2')
        # time.sleep(1)
        # print('1')
        # time.sleep(1)
        # print('READY')
        ret, frame = self.cap.read()
    
        frame = self.crop_frame(frame)
        cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX)

        self.sampled_points = waypoints
      
    

        while True:
   
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break

            cropped_frame = self.crop_frame(frame)
            cropped_frame = self.rotate_frame(cropped_frame)
            for goal in waypoints:
                cv2.circle(cropped_frame, (goal[1], goal[0]), 3, (0, 150, 255), -1)
            ball_center = self.detect_ball(cropped_frame)
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


a_star = MazeSolver()

try:
    # Run the simplified process: find path, print waypoints, display static result
    a_star_waypoints = a_star.run()
    print(a_star_waypoints)
    print(a_star_waypoints[0])
    print(a_star_waypoints[0][0])
except KeyboardInterrupt:
    print("\nManual interruption detected.")
finally:
    # Ensure cleanup happens
    a_star.cleanup()

processor = ImageProcessor()
processor.run(a_star_waypoints)