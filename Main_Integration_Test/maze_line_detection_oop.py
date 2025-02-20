import cv2
import numpy as np
from threading import Thread

class BallTracker:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            exit()
        
        # Reduce resolution for better performance
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        self.min_contour_area = 1000
        self.kernel = np.ones((5, 5), np.uint8)  # Smaller kernel for speed
        self.line_coordinates = []
        self.frame_count = 0
        self.running = True
        cv2.namedWindow('Video')
        
    def process_frame(self, frame):
        self.frame_count += 1
        cropped_frame = self.crop_frame(frame)
        gmask = self.get_green_mask(cropped_frame)
        
        # Run heavy processing every 5th frame to improve speed
        if self.frame_count % 5 == 0:
            ball_center = self.detect_ball(cropped_frame)
            if ball_center:
                self.control_motors(ball_center)
        
        cv2.imshow('Video', cropped_frame)
    
    def crop_frame(self, frame):
        frame_height, frame_width = frame.shape[:2]
        crop_width, crop_height = 750, 560
        x_offset, y_offset = 90, 100
        start_x = (frame_width - crop_width) // 2
        end_x = start_x + crop_width
        start_y = (frame_height - crop_height) // 2
        end_y = start_y + crop_height
        return frame[start_y + y_offset:end_y + y_offset, start_x + x_offset:end_x + x_offset]
    
    def get_green_mask(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_green, upper_green = np.array([35, 50, 50]), np.array([85, 255, 255])
        return cv2.inRange(hsv, lower_green, upper_green)
    
    def detect_ball(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # Reduce noise
        
        # Adaptive thresholding
        threshball = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 6)
        cleaned_thresh = cv2.morphologyEx(threshball, cv2.MORPH_OPEN, self.kernel)
        
        circles = cv2.HoughCircles(cleaned_thresh, cv2.HOUGH_GRADIENT, 1.2, 30, param1=100, param2=30, minRadius=5, maxRadius=20)
        
        if circles is not None:
            largest_circle = max(circles[0, :], key=lambda c: c[2])
            x, y, r = largest_circle
            cv2.circle(frame, (int(x), int(y)), int(r), (255, 0, 0), 2)
            cv2.circle(frame, (int(x), int(y)), 2, (0, 255, 0), 3)
            return x, y
        return None
    
    def control_motors(self, ball_center):
        gx, gy = 370, 280
        bx, by = ball_center
        offset_x, offset_y = gx - bx, gy - by
        print(f"Ball offset: x={offset_x}, y={offset_y}")
        if abs(offset_x) > 20:
            print("Move motor on X axis")
            self.motor_control(10 if offset_x > 0 else -10, 0)
        if abs(offset_y) > 20:
            print("Move motor on Y axis")
            self.motor_control(0, 10 if offset_y > 0 else -10)

    def motor_control(self, x, y):
        pass  # Implement motor control logic here
    
    def process_loop(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break
            self.process_frame(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False
                break
        self.cap.release()
        cv2.destroyAllWindows()

    def run(self):
        processing_thread = Thread(target=self.process_loop, daemon=True)
        processing_thread.start()
        while self.running:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False
                break
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    tracker = BallTracker()
    tracker.run()
