import cv2
import numpy as np
from Peripherals.Motor_Control import PCA9685

class ImageProcessing:
    def __init__(self):
        self.motors = PCA9685()
        self.cap = cv2.VideoCapture(0)
        self.running = True  # Control flag for the loop

        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            exit()

        self.line_coordinates = []
        self.min_contour_area = 1000
        self.kernel = np.ones((15, 15), np.uint8)

    def process_video(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break

            cropped_frame = self.crop_frame(frame)
            processed_frame, ball_center = self.detect_objects(cropped_frame)

            if ball_center:
                self.control_motors(ball_center)

            cv2.imshow('Processed Frame', processed_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False

        self.cleanup()

    def crop_frame(self, frame):
        frame_height, frame_width = frame.shape[:2]
        crop_width, crop_height = 1000, 700
        x_offset, y_offset = 90, 100

        start_x = (frame_width - crop_width) // 2
        start_y = (frame_height - crop_height) // 2

        return frame[start_y + y_offset:start_y + y_offset + crop_height,
                     start_x + x_offset:start_x + x_offset + crop_width]

    def detect_objects(self, frame):
        # Convert frame to HSV color space for better color segmentation
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define the HSV range for detecting a green ball (or your target color)
        lower_green = np.array([35, 50, 50])  # Adjust for your environment
        upper_green = np.array([85, 255, 255])
        
        # Create mask for green color
        gmask = cv2.inRange(hsv, lower_green, upper_green)
        gmask = cv2.morphologyEx(gmask, cv2.MORPH_CLOSE, self.kernel)  # Clean the mask

        # Find contours in the mask
        gcontours, _ = cv2.findContours(gmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        filled_frame = frame.copy()
        ball_center = None

        # Process contours to filter out small objects
        for contour in gcontours:
            area = cv2.contourArea(contour)
            if area > self.min_contour_area:
                x, y, w, h = cv2.boundingRect(contour)
                cx, cy = x + w // 2, y + h // 2
                self.line_coordinates.append((cx, cy))
                cv2.drawContours(filled_frame, [contour], -1, (0, 0, 255), thickness=cv2.FILLED)

        # Debug: Show the green mask and contours
        cv2.imshow('Green Mask', gmask)

        # Additional ball detection using adaptive thresholding and contour checking
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (15, 15), 0)
        threshball = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv2.THRESH_BINARY, 11, 6)

        # Find contours for ball-like objects
        contours, _ = cv2.findContours(threshball, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        largest_circle = None
        largest_radius = 0

        # Process contours to find the largest circular object
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100:  # Threshold for ball size
                x, y, w, h = cv2.boundingRect(contour)
                radius = max(w, h) // 2

                # Check for circularity (aspect ratio should be close to 1)
                aspect_ratio = float(w) / float(h)
                if 0.8 < aspect_ratio < 1.2:  # Ball should be nearly circular
                    if radius > largest_radius:
                        largest_radius = radius
                        largest_circle = (x + w // 2, y + h // 2, radius)

        # If we found a ball, draw it
        if largest_circle:
            x, y, r = largest_circle
            cv2.circle(filled_frame, (x, y), r, (255, 0, 0), 2)
            cv2.circle(filled_frame, (x, y), 2, (0, 255, 0), 3)
            ball_center = (x, y)

        # Debug: Show the thresholded image
        cv2.imshow('Thresholded Image', threshball)

        return filled_frame, ball_center

    def control_motors(self, ball_center):
        gx, gy = 510, 390
        bx, by = ball_center
        offset_x, offset_y = gx - bx, gy - by

        changex, changey = 300, 300
        defaultx, defaulty = 1870, 1925
        change = 50

        if offset_x > 20:
            changey = 100
        elif offset_x < -20:
            changey = -100
        if offset_y > 20:
            changex = 100
        elif offset_y < -20:
            changex = -100

        if changex == 300 and changey != 300:
            self.motors.setServoPulse(0, defaulty - change if changey < 0 else defaulty + change)
        elif changey == 300 and changex != 300:
            self.motors.setServoPulse(1, defaultx - change if changex < 0 else defaultx + change)
        elif changex != 300 and changey != 300:
            self.motors.setServoPulse(1, defaultx - change if changex < 0 else defaultx + change)
            self.motors.setServoPulse(0, defaulty - change if changey < 0 else defaulty + change)
        else:
            self.motors.setServoPulse(1, defaultx)
            self.motors.setServoPulse(0, defaulty)

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()
        with open('line_coordinates.txt', 'w') as f:
            for coord in self.line_coordinates:
                f.write(f"{coord}\n")
        print("Processing stopped and coordinates saved.")

if __name__ == "__main__":
    ip = ImageProcessing()
    ip.process_video()
