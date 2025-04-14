import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
ret, frame = cap.read()
frame_height, frame_width = frame.shape[:2]
crop_width, crop_height = 320, 240
x_offset, y_offset = 10, -15

start_x = (frame_width - crop_width) // 2
end_x = start_x + crop_width
start_y = (frame_height - crop_height) // 2
end_y = start_y + crop_height

frame = frame[start_y + y_offset:end_y + y_offset, start_x + x_offset:end_x + x_offset]

# Callback function to handle mouse events
def get_hsv_value(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # Left-click
        # Get the pixel value at the (x, y) position
        pixel_bgr = frame[y, x]
        
        # Convert BGR to HSV
        pixel_hsv = cv2.cvtColor(np.uint8([[pixel_bgr]]), cv2.COLOR_BGR2HSV)
        
        # Print the HSV value
        print(f"HSV Value at ({x},{y}): {pixel_hsv[0][0]}")

# Load an image (replace 'your_image.jpg' with the path to your image)
image = cv2.imread('your_image.jpg')

# Convert the image to HSV color space
hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Display the image
cv2.imshow('Image', frame)

# Set the mouse callback function
cv2.setMouseCallback('Image', get_hsv_value)

# Wait until a key is pressed
cv2.waitKey(0)
cv2.destroyAllWindows()
