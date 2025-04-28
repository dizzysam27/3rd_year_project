# necessary imports
import cv2
import numpy as np
import pickle  # For saving/loading last coordinates
import os
from simple_pid import PID
import PyQt5
from PyQt5.QtCore import pyqtSignal, QThread, pyqtSlot
from collections import deque
import argparse

# global variables for gui communication
global xRate, yRate, finish_flag
xRate = 0
yRate =0
finish_flag = 0

# Main
class ImageProcessor(QThread):
    # signals for communicating with gui
    cameraVideo = pyqtSignal(np.ndarray)
    xRate = pyqtSignal(int)
    yRate = pyqtSignal(int)
    finish_flag = pyqtSignal(int)
    aiControlStateChanged = pyqtSignal(bool)
    
    def __init__(self, motors):
        super().__init__()
        
        self.motors = motors
        self._ai_control_active = False
        self.aiControlStateChanged.connect(self.onAiControlStateChanged)

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

        #flat_x, flat_y = get_flat_values()
        self.defaultx = 1849#flat_x
        self.defaulty = 1941#flat_y
        
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
        self.maze_finished = 0
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
        # self.pid_y.proportional_on_measurement = True

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
    
    def detect_ball(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      
        lower_red, upper_red = np.array([120,50, 80]), np.array([255,255, 159])
        mask = cv2.inRange(hsv, lower_red, upper_red)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) > 10:
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    
                    # store center coordinates of ball 
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    self.last_location[0] = int(M["m10"] / M["m00"])
                    self.last_location[1] = int(M["m01"] / M["m00"])
                    
                    # store ball location for stuck detection
                    if self.balltrackercounter == 0:
                        self.balltracker[0] = int(M["m10"] / M["m00"])
                        self.balltracker[1] = int(M["m01"] / M["m00"])

                    # if ball still in same location then boost motors
                    if self.balltrackercounter == 10:
                        if self.balltracker[0] >= cx - 1 and self.balltracker[0] <= cx + 1 and self.balltracker[1] >= cy - 1 and self.balltracker[1] <= cy + 1:
                            self.output_limits = 30
                            self.output_limitsy = 30
                            print('boosted')
                            self.boosted = 1
                            cx = 800 - cx 
                            cy = 600 - cy
                            if self.current_target_index < 4:
                                self.current_target_index = 0
                            else:
                                self.current_target_index = self.current_target_index - 4
                                self.goal_reached = True

                    # stop boost after 3 frames
                    if self.balltrackercounter == 13:
                        if self.boosted == 1:
                            self.output_limitsy = self.default_limits_y
                            self.output_limits = self.default_limits_x
                            print('normal')
                        self.balltrackercounter = -1
                        self.balltracker = [0,0]
                        self.boosted = 0
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])

                    #increment ball tracker counter and return limits to normal
                    self.balltrackercounter += 1
                    self.pid_x.output_limits = (-self.output_limits, self.output_limits)
                    self.pid_y.output_limits = (-self.output_limitsy, self.output_limitsy)
                    
                    # check if maze is finished
                    self.finished_zone(cx,cy)

                    return (cx, cy)
                
        else:
            # if ball not detected then use last known location
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

        # Return line points in correct order
        return np.concatenate((line_points[start_idx:], line_points[:start_idx]), axis=0)


    def detect_line(self, frame):
        # self.xRate.emit(self.defaultx)
        # self.yRate.emit(self.defaulty)
        cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX)

        lower_blue, upper_blue = np.array([150,115,49]), np.array([255,219,168])
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

        return interpolated_points
    
    # function to reset goal to start
    def resetline(self):
        self.current_target_index = 0
        self.goal_reached = True
        self.pid_x.reset()
        self.pid_y.reset()

        print("reset")
               

    # function to check if ball is in end area
    def finished_zone(self, x,y):
        # [x_min, x_max, y_min, y_max] points
        goal_area = [0, 50, 110, 210]
        # Current goal for ball movement
        goal_x, goal_y = self.sampled_points[self.current_target_index]

        if (goal_area[0] <=x<= goal_area[1] and goal_area[2] <=y<= goal_area[3]):

            if (goal_area[0] <=goal_x<= goal_area[1] and goal_area[2] <=goal_y<= goal_area[3]):
                
                self.maze_finished = 1
                self.finish_flag.emit(self.maze_finished)
                print("finish flagerer") 
            else:
                pass
        else:
            pass

    @pyqtSlot(bool)
    def onAiControlStateChanged(self, is_active):
        self._ai_control_active = is_active
        # Reset motors to default if AI is deactivated
        if not is_active:
            self.motors.setServoPulse(1, self.defaultx)
            self.motors.setServoPulse(0, self.defaulty)


    def move_motors(self, ball_center):
        if ball_center:
            bx, by = ball_center
            # check if ball has reached goal
            if abs(bx - self.gx) < self.reached_distance and abs(by - self.gy) < self.reached_distance:
                self.goal_reached = True

            # Calculate motor change with PID
            control_x = self.pid_x(bx)
            control_y = self.pid_y(by)
            
            # new motor values
            motor_x_val = self.defaultx + control_x
            motor_y_val = self.defaulty + control_y

        # Check the internal flag before sending commands
            if self._ai_control_active:
                self.motors.setServoPulse(1, int(motor_x_val)) # Send X command
                self.motors.setServoPulse(0, int(motor_y_val)) # Send Y command

    # function to update goal position
    def update_goal_position(self):
        # if last goal was reached and maze has not reached end of goals
        if self.goal_reached and self.current_target_index < len(self.sampled_points):
            self.gx, self.gy = self.sampled_points[self.current_target_index]
            # then go to next goal
            self.current_target_index += 1
            self.goal_reached = False  
        # if the last goal was reached, goal goes back to start
        elif self.current_target_index >= len(self.sampled_points):
            self.current_target_index = 0  

        # set PID setpoints to new goal location
        self.pid_x.setpoint = self.gx
        self.pid_y.setpoint = self.gy

    # function for picking manual goal points ( not really used anymore )
    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.sampled_points.append((x, y))
            print(f"Point added: {x}, {y}")
         
    # cleanup function for exiting         
    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()
        print("Cleaning up and exiting.")


    # main loop
    def run(self):
        
        # set motors to flat and goal to start position
        self.motors.setServoPulse(1, self.defaultx)
        self.motors.setServoPulse(0, self.defaulty)
        self.current_target_index = 0  
        
        # setup camera and initial line detectio
        ret, frame = self.cap.read()
        frame = self.crop_frame(frame)
        cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX)
        self.sampled_points = self.detect_line(frame)
        start = (130, 268)
        self.sampled_points = self.reorder_line_to_start(self.sampled_points, start)

        while True:            
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break

            cropped_frame = self.crop_frame(frame)
            ball_center = self.detect_ball(cropped_frame)
            
            for goal in self.sampled_points[:198]:
                if  not self._ai_control_active:
                    cv2.circle(cropped_frame, (goal[0], goal[1]), 2, (0, 150, 255), -1)
            
            self.update_goal_position()
            self.move_motors(ball_center)

            # draw line for visual ball tracking on gui
            if ball_center:
                cv2.circle(cropped_frame, ball_center, 3, (0, 0, 255), -1)
                self.ballpts.appendleft(ball_center)
                for i in range(1, len(self.ballpts)):
                    # if either of the tracked points are None, ignore
                    if self.ballpts[i - 1] is None or self.ballpts[i] is None:
                        continue
                    # compute the thickness of the line and
                    # draw the connecting lines
                    thickness = int(np.sqrt(self.args["buffer"] / float(i + 1)) * 2.5)
                    cv2.line(cropped_frame, self.ballpts[i - 1], self.ballpts[i], (0, 0, 255), thickness)

            cv2.circle(cropped_frame, (self.gx, self.gy), 5, (0, 0, 255), -1)

            # send final video to gui
            self.cameraVideo.emit(cropped_frame)
            
        # exit     
        self.cleanup()
