import cv2
import numpy as np
from Peripherals.Motor_Control import PCA9685
import time

class IMAGEPROCESSING:
    
    def __init__(self):
        self.motors = PCA9685()
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            exit()

        # Crop parameters (unchanged)
        self.crop_width = 1000
        self.crop_height = 700
        self.x_offset = 90
        self.y_offset = 100

        self.min_contour_area = 1000  # Minimum contour area threshold
        self.kernel = np.ones((15, 15), np.uint8)  # Kernel for morphological operations

    def process_frame(self, frame):
        # Get frame dimensions
        frame_height, frame_width = frame.shape[:2]
        
        # Calculate start and end coordinates for the central region
        start_x = (frame_width - self.crop_width) // 2
        end_x = start_x + self.crop_width
        start_y = (frame_height - self.crop_height) // 2
        end_y = start_y + self.crop_height

        # Perform cropping
        cropped_frame = frame[start_y + self.y_offset :end_y + self.y_offset, start_x + self.x_offset :end_x + self.x_offset]
        
        return cropped_frame

    def find_green_contours(self, cropped_frame):
        # Convert to HSV and create a green mask
        hsv = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)
        lower_green = np.array([35, 50, 50])
        upper_green = np.array([85, 255, 255])
        gmask = cv2.inRange(hsv, lower_green, upper_green)
        
        # Find contours of green regions
        gcontours, _ = cv2.findContours(gmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        return gcontours

    def find_ball(self, cropped_frame):
        # Convert to grayscale and apply thresholding
        gray = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
        threshball = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 6
        )

        # Use HoughCircles to find the ball
        circles = cv2.HoughCircles(
            threshball, cv2.HOUGH_GRADIENT, 1, 20, param1=130, param2=20, minRadius=2, maxRadius=20
        )

        return circles, threshball

    def control_motors(self, offset_x, offset_y):
        # Control logic for motors based on offsets
        changex = 300
        changey = 300
        defaultx = 1870
        defaulty = 1925
        change = 50

        if offset_x > 20:
            changey = 100
        if offset_x < -20:
            changey = -100
        if offset_y > 20:
            changex = 100
        if offset_y < -20:
            changex = -100

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

    def process(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break

            cropped_frame = self.process_frame(frame)
            gcontours = self.find_green_contours(cropped_frame)
            
            # Handle the contours
            for contour in gcontours:
                area = cv2.contourArea(contour)
                if area > self.min_contour_area:
                    # Handle green contours here
                    pass

            circles, threshball = self.find_ball(cropped_frame)

            if circles is not None:
                circles = circles[0, :]  # Extract circles

                # Find the largest circle
                largest_circle = max(circles, key=lambda c: c[2], default=None)

                if largest_circle:
                    x, y, r = largest_circle  # Get circle center and radius
                    print(f"Largest Circle Center: ({x:.2f}, {y:.2f}), Radius: {r:.2f}")

                    # Ball's center coordinates
                    ball_center = (x, y)

                    # Reference center (adjust this as needed)
                    gx, gy = 510, 390

                    # Calculate offsets
                    offset_x = gx - ball_center[0]
                    offset_y = gy - ball_center[1]

                    # Control motors based on offsets
                    self.control_motors(offset_x, offset_y)

            time.sleep(0.001)  # Optional sleep to control loop speed

            # Show processed frames
            cv2.imshow('Processed Frame', cropped_frame)

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release resources
        self.cap.release()
        cv2.destroyAllWindows()

# Run the processing
run = IMAGEPROCESSING()
run.process()
