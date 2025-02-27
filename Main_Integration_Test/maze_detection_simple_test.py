import cv2
import numpy as np
from Peripherals.Motor_Control import PCA9685
import time

class ImageProcessor:
    
    def __init__(self):
        self.motors = PCA9685()
        self.cap = cv2.VideoCapture(0)
        self.line_coordinates = []
        self.min_contour_area = 1000
        self.kernel = np.ones((15, 15), np.uint8)
        self.defaultx = 1870
        self.defaulty = 1925
        self.change = 20
        self.gx, self.gy = 510, 390

        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            exit()

    def crop_frame(self, frame):
        frame_height, frame_width = frame.shape[:2]
        crop_width = 1000
        crop_height = 700
        x_offset = 90
        y_offset = 100

        start_x = (frame_width - crop_width) // 2
        end_x = start_x + crop_width

        start_y = (frame_height - crop_height) // 2
        end_y = start_y + crop_height

        return frame[start_y + y_offset : end_y + y_offset, start_x + x_offset : end_x + x_offset]

    def process_frame(self, frame):
        cropped_frame = self.crop_frame(frame)

        # Process ball detection
        ball_center = self.detect_ball(cropped_frame)

        return ball_center

    def detect_ball(self, cropped_frame):
        # Detect circles using HoughCircles
        gray = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
        cleaned_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 6)
        circles = cv2.HoughCircles(cleaned_thresh, cv2.HOUGH_GRADIENT, 1, 20, param1=130, param2=20, minRadius=2, maxRadius=20)
        
        if circles is not None:
            circles = circles[0, :]
            largest_circle = max(circles, key=lambda c: c[2], default=None)
            if largest_circle is not None:
                return (largest_circle[0], largest_circle[1])
        return None

    def move_motors(self, ball_center):
        if ball_center:
            bx, by = ball_center
            offset_x = self.gx - bx
            offset_y = self.gy - by
            changex = changey = 300

            if offset_x > 20:
                changex = 100
            elif offset_x < -20:
                changex = -100

            if offset_y > 20:
                changey = 100
            elif offset_y < -20:
                changey = -100

            if changex == 300:
                if changey != 300:
                    self.adjust_motor(0, changey)
            elif changey == 300:
                if changex != 300:
                    self.adjust_motor(1, changex)
            else:
                self.adjust_motor(1, changex)
                self.adjust_motor(0, changey)
        else:
            self.reset_motors()

    def adjust_motor(self, motor_index, change):
        if motor_index == 0:
            if change < 0:
                self.motors.setServoPulse(0, self.defaulty - self.change)
                     
            elif change > 0:
                self.motors.setServoPulse(0, self.defaulty + self.change)
         
        elif motor_index == 1:
            if change < 0:
                self.motors.setServoPulse(1, self.defaultx - self.change)
   
            elif change > 0:
                self.motors.setServoPulse(1, self.defaultx + self.change)
             

    def reset_motors(self):
        self.motors.setServoPulse(1, self.defaultx)
        self.motors.setServoPulse(0, self.defaulty)

    def run(self):
        frame_rate = 30
        prev = 0
        while True:
  
            while True:
                time_elapsed = time.time() - prev
                ret, image = self.cap.read()

                if not ret:
                    print("Error: Failed to capture frame.")
                    break

                if time_elapsed > 1./frame_rate:
                    prev = time.time()

                    # Do something with your image here.
                    ball_center = self.process_frame(image)
                    self.move_motors(ball_center)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            
        self.save_coordinates()
        self.cleanup()

    def save_coordinates(self):
        with open('line_coordinates.txt', 'w') as f:
            for coord in self.line_coordinates:
                f.write(f"{coord}\n")

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()
        print("Coordinates of black line segments have been saved to 'line_coordinates.txt'.")

# Run the processor
processor = ImageProcessor()
processor.run()
