import cv2
import numpy as np
import threading
import time
from queue import Queue
from Peripherals.Motor_Control import PCA9685

class IMAGEPROCESSING:
    
    def __init__(self):
        self.motors = PCA9685()
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            exit()

        self.line_coordinates = []
        self.min_contour_area = 1000
        self.kernel = np.ones((15, 15), np.uint8)
        
        # Queue for passing frames between threads
        self.frame_queue = Queue(maxsize=10)

        self.running = True  # Control flag for all threads

        # Start the threads
        self.capture_thread = threading.Thread(target=self.capture_frames)
        self.capture_thread.start()

        self.process_thread = threading.Thread(target=self.process_frames)
        self.process_thread.start()

    def capture_frames(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                # Put the captured frame in the queue for processing
                if not self.frame_queue.full():
                    self.frame_queue.put(frame)
            else:
                print("Error: Failed to capture frame.")

    def process_frames(self):
        while self.running:
            if not self.frame_queue.empty():
                frame = self.frame_queue.get()
                processed_frame, ball_center = self.detect_objects(frame)
                self.control_motors(ball_center)
                self.display_frame(processed_frame)
            time.sleep(0.01)  # Allow time for other threads to run

    def detect_objects(self, frame):
        # Process the frame to detect objects (similar to your original processing)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_green = np.array([35, 50, 50])
        upper_green = np.array([85, 255, 255])
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

        # Ball detection (same as your original approach)
        gray = cv2.cvtColor(filled_frame, cv2.COLOR_BGR2GRAY)
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
        if ball_center:
            gx, gy = 510, 390  # Green center (hardcoded)
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

    def display_frame(self, frame):
        # Display the frame, and handle closing the window
        cv2.imshow('Processed Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.running = False

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()
        with open('line_coordinates.txt', 'w') as f:
            for coord in self.line_coordinates:
                f.write(f"{coord}\n")
        print("Processing stopped and coordinates saved.")

if __name__ == "__main__":
    processor = IMAGEPROCESSING()
    processor.cleanup()
