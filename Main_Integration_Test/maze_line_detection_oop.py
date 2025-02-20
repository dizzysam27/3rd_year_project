import cv2
import numpy as np
import threading
import time
from Peripherals.Motor_Control import PCA9685

class ImageProcessing:
    def __init__(self):
        self.motors = PCA9685()
        self.cap = cv2.VideoCapture(0)
        self.running = True  # Control flag for the threads

        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            exit()

        self.line_coordinates = []
        self.min_contour_area = 1000
        self.kernel = np.ones((15, 15), np.uint8)

        # Start the processing and motor control in separate threads
        self.image_thread = threading.Thread(target=self.process_video)
        self.image_thread.start()

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
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_green, upper_green = np.array([35, 50, 50]), np.array([85, 255, 255])
        gmask = cv2.inRange(hsv, lower_green, upper_green)
        gcontours, _ = cv2.findContours(gmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        filled_frame = frame.copy()
        ball_center = None

        for contour in gcontours:
            area = cv2.contourArea(contour)
            if area > self.min_contour_area:
                x, y, w, h = cv2.boundingRect(contour)
                cx, cy = x + w // 2, y + h // 2
                self.line_coordinates.append((cx, cy))
                cv2.drawContours(filled_frame, [contour], -1, (0, 0, 255), thickness=cv2.FILLED)

        # Detect ball
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        threshball = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv2.THRESH_BINARY, 11, 6)
        contours, _ = cv2.findContours(threshball, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        largest_circle = None
        largest_radius = 0

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 10:
                x, y, w, h = cv2.boundingRect(contour)
                radius = max(w, h) // 2
                if radius > largest_radius:
                    largest_radius = radius
                    largest_circle = (x + w // 2, y + h // 2, radius)

        if largest_circle:
            x, y, r = largest_circle
            cv2.circle(filled_frame, (x, y), r, (255, 0, 0), 2)
            cv2.circle(filled_frame, (x, y), 2, (0, 255, 0), 3)
            ball_center = (x, y)

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
    ImageProcessing()
