import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
ret, frame = cap.read()
frame_height, frame_width = frame.shape[:2]
crop_width, crop_height = 305, 220
x_offset, y_offset = 10, -10

start_x = (frame_width - crop_width) // 2
end_x = start_x + crop_width
start_y = (frame_height - crop_height) // 2
end_y = start_y + crop_height

frame = frame[start_y + y_offset:end_y + y_offset, start_x + x_offset:end_x + x_offset]

# Convert the image to HSV color space
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Define the color range for the ball (e.g., red ball)
lower_red = np.array([33, 0, 50])
upper_red = np.array([84, 69, 130])

# Create a mask to isolate the ball's color
mask = cv2.inRange(hsv, lower_red, upper_red)

# Find contours from the mask
contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Loop through the contours to detect the ball
for contour in contours:
    if cv2.contourArea(contour) > 5 and cv2.contourArea(contour) < 20 :  # Filter small contours
        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y))
        radius = int(radius)

        if radius > 1 and radius < 100:  # Ensure the detected object is big enough to be a ball
            cv2.circle(frame, center, radius, (0, 255, 0), 2)
            cv2.putText(frame, "Ball Detected", (int(x - radius), int(y - radius - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

# Show the result
cv2.imshow('Ball Detection', frame)
cv2.imshow('Mask', mask)

cv2.waitKey(0)
cv2.destroyAllWindows()
