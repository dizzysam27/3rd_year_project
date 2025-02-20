import cv2
import numpy as np
from Peripherals.Motor_Control import PCA9685
import time
import threading

class IMAGEPROCESSING:
    
    def __init__(self):
        self.motors = PCA9685()
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            exit()

        self.line_coordinates = []
        self.min_contour_area = 1000  # Adjust this value to fit your needs
        self.kernel = np.ones((15, 15), np.uint8)  # Larger kernels will help close larger gaps

        self.lock = threading.Lock()  # To handle shared resources safely

        # Start the image processing thread
        self.processing_thread = threading.Thread(target=self.process_frame)
        self.processing_thread.daemon = True
        self.processing_thread.start()

        # Main loop for frame capture
        self.main_loop()

    def process_frame(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break

            # Process frame (image processing code goes here)
            self.process_image(frame)

    def process_image(self, frame):
        with self.lock:
            # Image processing code goes here (cropping, HSV conversion, contour detection, etc.)
            frame_height, frame_width = frame.shape[:2]
            crop_width = 1000
            crop_height = 700
            x_offset = 30
            y_offset = 30

            start_x = (frame_width - crop_width) // 2
            end_x = start_x + crop_width

            start_y = (frame_height - crop_height) // 2
            end_y = start_y + crop_height

            cropped_frame = frame[start_y + y_offset :end_y + y_offset, start_x + x_offset :end_x + x_offset]

            # Perform image processing (you can keep the same processing logic)
            hsv = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)

            # Example: Detect green contours
            lower_green = np.array([35, 50, 50])  # Lower bound of green
            upper_green = np.array([85, 255, 255])  # Upper bound of green
            gmask = cv2.inRange(hsv, lower_green, upper_green)
            gcontours, ghierarchy = cv2.findContours(gmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            gfilled_frame = cropped_frame.copy()
            for contour in gcontours:
                area = cv2.contourArea(contour)
                if area > self.min_contour_area:
                    x, y, w, h = cv2.boundingRect(contour)
                    cx, cy = x + w // 2, y + h // 2
                    self.line_coordinates.append((cx, cy))
                    cv2.drawContours(gfilled_frame, [contour], -1, (0, 0, 255), thickness=cv2.FILLED)

            # Example: Detect circles (ball detection using HoughCircles)
            circles = cv2.HoughCircles(gmask, cv2.HOUGH_GRADIENT, 1, 20, param1=130, param2=20, minRadius=2, maxRadius=20)
            if circles is not None:
                circles = circles[0, :]
                largest_circle = max(circles, key=lambda c: c[2], default=None)  # Find the largest circle
                if largest_circle:
                    # Ball's center coordinates
                    ball_center = (largest_circle[0], largest_circle[1])
                    print(f"Largest Circle Center: ({ball_center[0]:.2f}, {ball_center[1]:.2f})")

                    # Perform motor control based on ball position
                    self.control_motors(ball_center)

            # Display the processed frame
            cv2.imshow('Processed Frame', gfilled_frame)
    
    def control_motors(self, ball_center):
        # Motor control logic based on the ball position (use same logic as your code)
        gx = 510
        gy = 390
        bx, by = ball_center
        offset_x = gx - bx
        offset_y = gy - by

        changex = 300
        changey = 300
        defaultx = 1870
        defaulty = 1925
        change = 50

        if offset_x > 20:
            changex = 100
        if offset_x < -20:
            changex = -100
        if offset_y > 20:
            changey = 100
        if offset_y < -20:
            changey = -100

        if changex == 300:
            if changey != 300:
                if changey < 0:
                    self.motors.setServoPulse(0, defaulty - change)
                if changey > 0:
                    self.motors.setServoPulse(0, defaulty + change)
        elif changey == 300:
            if changex != 300:
                if changex > 0:
                    self.motors.setServoPulse(1, defaultx + change)
                if changex < 0:
                    self.motors.setServoPulse(1, defaultx - change)
        elif changex != 300 and changey != 300:
            if changey < 0:
                if changex > 0:
                    self.motors.setServoPulse(1, defaultx + change)
                    self.motors.setServoPulse(0, defaulty - change)
                if changex < 0:
                    self.motors.setServoPulse(1, defaultx - change)
                    self.motors.setServoPulse(0, defaulty - change)
            if changey > 0:
                if changex > 0:
                    self.motors.setServoPulse(1, defaultx + change)
                    self.motors.setServoPulse(0, defaulty + change)
                if changex < 0:
                    self.motors.setServoPulse(1, defaultx - change)
                    self.motors.setServoPulse(0, defaulty + change)
        else:
            self.motors.setServoPulse(1, defaultx)
            self.motors.setServoPulse(0, defaulty)

    def main_loop(self):
        while True:
            # Main loop to capture and display the frame
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break

            # Display the frame
            cv2.imshow('Webcam Feed', frame)

            # Break the loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

run = IMAGEPROCESSING()
