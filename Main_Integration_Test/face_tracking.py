import cv2
import numpy as np
import time
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
        self.gx, self.gy = 320, 240  # Center of the frame
        motor_sensitivity = 25

        # PID controllers for X and Y axes
        self.pid_x = PID(1.0, 0.02, 0.1, setpoint=self.gx)
        self.pid_y = PID(1.0, 0.02, 0.1, setpoint=self.gy)
        self.pid_x.output_limits = (-motor_sensitivity, motor_sensitivity)
        self.pid_y.output_limits = (-motor_sensitivity, motor_sensitivity)

      
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            exit()

    def detect_face(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3, minSize=(0, 0))
        (X1,Y1,W1,H1) = (0,0,0,0)
        for (x, y, w, h) in faces:
            if (x,y,w,h) != (0,0,0,0):
                (X1,Y1,W1,H1) = (x,y,w,h)
            cv2.rectangle(img, (X1, Y1), (X1+W1, Y1+H1), (0, 0, 0), -1)

    def move_motors(self, face_center):
        if face_center:
            fx, fy = face_center
            control_x = self.pid_x(fx)
            control_y = self.pid_y(fy)
            
            self.motors.setServoPulse(1, int(self.defaultx + control_x))
            self.motors.setServoPulse(0, int(self.defaulty + control_y))
        else:
            self.motors.setServoPulse(1, self.defaultx)
            self.motors.setServoPulse(0, self.defaulty)

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break
            
            face_center = self.detect_face(frame)
            print(face_center)
            self.move_motors(face_center)

            # Show camera feed with detected face
            if face_center:
                cv2.circle(frame, face_center, 10, (0, 255, 0), -1)
            cv2.imshow("Face Tracking", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cleanup()

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()
        print("Cleaning up and exiting.")

# Run the processor
processor = ImageProcessor()
processor.run()
