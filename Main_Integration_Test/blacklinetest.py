import cv2
import numpy as np

# Read the image
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
ret, frame = cap.read()
cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX)
frame_height, frame_width = frame.shape[:2]
crop_width, crop_height = 290, 210
x_offset, y_offset = 10, -10

start_x = (frame_width - crop_width) // 2
end_x = start_x + crop_width
start_y = (frame_height - crop_height) // 2
end_y = start_y + crop_height

img = frame[start_y + y_offset:end_y + y_offset, start_x + x_offset:end_x + x_offset]

# Threshold to detect dark regions (black line)
lower = (0, 0, 0)
upper = (149, 158, 162)
thresh = cv2.inRange(img, lower, upper)

# Apply Canny edge detection to capture the edges of the line
edges = cv2.Canny(thresh, 100, 200)

# Dilate the edges to make the line thicker, improving the detection of even spaces
kernel = np.ones((3, 3), np.uint8)
dilated_edges = cv2.dilate(edges, kernel, iterations=1)

# Use Hough Line Transform to detect lines and spaces between them
lines = cv2.HoughLinesP(dilated_edges, 1, np.pi / 180, threshold=50, minLineLength=30, maxLineGap=10)

if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw detected lines

    # Optionally, highlight spaces by analyzing distances between the detected lines (i.e., gap size)
    for i in range(len(lines) - 1):
        x1_1, y1_1, x2_1, y2_1 = lines[i][0]
        x1_2, y1_2, x2_2, y2_2 = lines[i + 1][0]

        # Calculate distance between the endpoints of consecutive lines
        dist = np.linalg.norm([x2_2 - x1_1, y2_2 - y1_1])
        print(f"Distance between lines: {dist}")

# Show the output
cv2.imshow('Line Detection and Spaces', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
