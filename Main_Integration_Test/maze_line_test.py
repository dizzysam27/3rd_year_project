import cv2
import numpy as np

# Open the camera
cap = cv2.VideoCapture(0)  # Change index if using an external camera

while True:
    ret, frame = cap.read()
    if not ret:
        break  # Stop if no frame is captured

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Thresholding to detect black line
    _, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if contours:
        # Select the largest contour (assuming it's the line)
        contour = max(contours, key=cv2.contourArea)

        # Approximate the contour to a simpler shape
        poly = cv2.approxPolyDP(contour, epsilon=0.01*cv2.arcLength(contour, True), closed=False)

        # Extract the points and sort by x-coordinate
        points = poly.reshape(-1, 2)
        points = sorted(points, key=lambda p: p[0])  # Sorting left to right

        # Sample 20 evenly spaced points along the line
        num_points = 20
        if len(points) >= num_points:
            step = len(points) // num_points
            sampled_points = points[::step][:num_points]  # Get 20 points
        else:
            sampled_points = points  # If fewer points, take all available

        # Convert to an array of (x, y) coordinates
        line_coordinates = np.array(sampled_points)

        # Draw the detected line
        cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)

        # Draw the sampled points
        for (x, y) in line_coordinates:
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)  # Red points

        # Print coordinates (optional)
        print("Detected points:", line_coordinates)

    # Show the output
    cv2.imshow('Black Line Detection', frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
