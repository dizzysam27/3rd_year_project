import cv2
import numpy as np

class MazeSolver:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.kernel = np.ones((15, 15), np.uint8)  # Morphological kernel for cleaning up small gaps
        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            exit()

    def crop_frame(self, frame):
        # Zoom into the region where the line is likely to be
        frame_height, frame_width = frame.shape[:2]
        
        # Adjusted crop area for zooming in on the center
        crop_width = 800   # Smaller width to zoom in
        crop_height = 600  # Smaller height to zoom in
        x_offset = 90      # Offset to adjust where to crop from the left
        y_offset = 100     # Offset to adjust where to crop from the top

        start_x = (frame_width - crop_width) // 2
        end_x = start_x + crop_width
        start_y = (frame_height - crop_height) // 2
        end_y = start_y + crop_height

        return frame[start_y + y_offset : end_y + y_offset, start_x + x_offset : end_x + x_offset]

    def process_frame(self, frame):
        return self.crop_frame(frame)

    def find_line_endpoints(self, frame):
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply binary threshold to focus on the black line (inverted threshold for black line on light background)
        _, thresholded = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)

        # Debug: Show the thresholded image to check if the black line is detected correctly
        cv2.imshow("Thresholded Image", thresholded)
        
        # Morphological operations to clean up the image (close small gaps)
        thresholded = cv2.morphologyEx(thresholded, cv2.MORPH_CLOSE, self.kernel)

        # Debug: Show the cleaned-up thresholded image
        cv2.imshow("Cleaned Threshold", thresholded)

        # Find contours
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Debug: Show contours on the original frame
            frame_with_contours = frame.copy()
            cv2.drawContours(frame_with_contours, contours, -1, (0, 255, 0), 2)
            cv2.imshow("Contours on Image", frame_with_contours)

            # Now, we try to detect the start and end points based on the black line's leftmost and rightmost points
            start_point = None
            end_point = None

            # Iterate over each contour to find the start and end of the black line
            for contour in contours:
                # Sort the contour points by x coordinate to better find the start and end
                contour = sorted(contour, key=lambda point: point[0][0])

                # Find the first and last non-zero pixels (endpoints)
                start_point = contour[0][0]  # First point in the contour
                end_point = contour[-1][0]   # Last point in the contour

            # Return the detected start and end points
            return start_point, end_point, thresholded

        # Return None for both points if no contours found
        return None, None, None

# Initialize the MazeSolver
solver = MazeSolver()

while True:
    ret, frame = solver.cap.read()
    if not ret:
        break

    # Process the frame
    maze = solver.process_frame(frame)
    
    # Find the start and end points of the black line
    start, end, thresholded = solver.find_line_endpoints(maze)

    # Check if start and end points are valid (not None)
    if start is None or end is None:
        print("Could not detect line endpoints.")
    else:
        # Debug: Print the start and end points for verification
        print(f"Start: {start}, End: {end}")

        # Draw a straight line between the start and end points
        cv2.line(maze, start, end, (0, 0, 255), 2)

        # Show the maze with the drawn line
        cv2.imshow('Maze Solver - Line Between Start and End', maze)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

solver.cap.release()
cv2.destroyAllWindows()
