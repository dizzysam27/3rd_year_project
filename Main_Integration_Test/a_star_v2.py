import cv2
import numpy as np
from heapq import heappop, heappush

class MazeSolver:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.kernel = np.ones((15, 15), np.uint8)  # Morphological kernel for cleaning up small gaps
        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            exit()

    def crop_frame(self, frame):
        frame_height, frame_width = frame.shape[:2]
        crop_width, crop_height = 1000, 750  # Updated crop size to 1000x750
        x_offset, y_offset = 10, -10  # Offsets for fine-tuning the crop

        # Calculate the start and end points to center the crop
        start_x = (frame_width - crop_width) // 2
        end_x = start_x + crop_width
        start_y = (frame_height - crop_height) // 2
        end_y = start_y + crop_height

        # Return the cropped frame with applied offsets
        return frame[start_y + y_offset:end_y + y_offset, start_x + x_offset:end_x + x_offset]

    def process_frame(self, frame):
        return self.crop_frame(frame)

    def find_green_walls_and_holes(self, frame):
        # Convert the frame to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define the range for green color (in HSV)
        lower_green = np.array([40, 50, 50])   # Lower bound of green
        upper_green = np.array([80, 255, 255]) # Upper bound of green

        # Threshold the image to get the green areas
        green_mask = cv2.inRange(hsv, lower_green, upper_green)

        # Use morphological operations to clean up small gaps and noise
        green_mask_cleaned = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, self.kernel)

        # Black line detection (inverse thresholding to find the black line)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, black_line_mask = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)

        # Morphological cleanup of the black line mask
        black_line_cleaned = cv2.morphologyEx(black_line_mask, cv2.MORPH_CLOSE, self.kernel)

        # Invert the black line mask to identify areas without the black line
        inverted_black_line_mask = cv2.bitwise_not(black_line_cleaned)

        # The mask of areas considered as holes is the region that is not green (not walls) and not black (no line)
        hole_mask = cv2.bitwise_and(inverted_black_line_mask, cv2.bitwise_not(green_mask_cleaned))

        # Use morphological operations to clean the holes mask
        hole_mask_cleaned = cv2.morphologyEx(hole_mask, cv2.MORPH_CLOSE, self.kernel)

        return green_mask_cleaned, hole_mask_cleaned

    def find_holes_using_contours(self, frame):
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply a Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (15, 15), 0)

        # Use binary thresholding to focus on the distinct features (holes)
        _, thresholded = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)

        # Find contours in the thresholded image
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        valid_circles = []

        for contour in contours:
            # Approximate the contour to a polygon and calculate its area
            contour_area = cv2.contourArea(contour)
            if contour_area < 100:  # Ignore small contours
                continue

            # Fit a circle to the contour
            (x, y), radius = cv2.minEnclosingCircle(contour)
            circle_area = np.pi * (radius ** 2)

            # Check if the contour is circular based on circularity (area / perimeter^2)
            perimeter = cv2.arcLength(contour, True)
            circularity = 4 * np.pi * contour_area / (perimeter ** 2) if perimeter else 0

            # Filter contours by size and circularity
            if 100 < contour_area < 1000 and circularity > 0.8:  # adjust the threshold values as necessary
                valid_circles.append((x, y, radius))
                # Draw the circle and center
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 4)  # Red circle
                cv2.circle(frame, (int(x), int(y)), 2, (0, 128, 255), 3)  # Yellow center

        return frame, valid_circles


# A* algorithm to find the optimal path
def astar(start, end, grid):
    # Heuristic function (Manhattan distance)
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # Initialize open and closed sets
    open_set = []
    heappush(open_set, (0 + heuristic(start, end), 0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_set:
        _, current_g, current = heappop(open_set)

        if current == end:
            # Reconstruct the path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for neighbor in [(current[0] + 1, current[1]), (current[0] - 1, current[1]),
                         (current[0], current[1] + 1), (current[0], current[1] - 1)]:
            if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]):
                if grid[neighbor[0]][neighbor[1]] == 0:  # 0 means free space
                    tentative_g_score = current_g + 1
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                        heappush(open_set, (f_score[neighbor], tentative_g_score, neighbor))

    return None


# Initialize the MazeSolver
solver = MazeSolver()

# Define start and end points
start_point = (272, 668)  # (x, y)
end_point = (77, 367)  # (x, y)

while True:
    ret, frame = solver.cap.read()
    if not ret:
        break

    # Process the frame (apply crop)
    maze = solver.process_frame(frame)

    # Find the green walls and holes (masks for green and holes)
    green_mask_cleaned, hole_mask_cleaned = solver.find_green_walls_and_holes(maze)

    # Debug: Check the output of green_mask_cleaned and hole_mask_cleaned
    print("Green Mask Cleaned:", green_mask_cleaned)
    print("Hole Mask Cleaned:", hole_mask_cleaned)

    # Create grid based on the green walls and holes map (1 = wall, 0 = free space)
    grid = np.zeros_like(green_mask_cleaned)
    grid[green_mask_cleaned == 255] = 1  # Set walls as 1
    grid[hole_mask_cleaned == 255] = 1   # Set holes as 1 (avoid these areas)

    # Debug: Ensure start and end points are within bounds and valid
    print("Grid size:", grid.shape)
    print("Start point:", start_point)
    print("End point:", end_point)

    # Run A* to find the path
    path = astar(start_point, end_point, grid)

    # Debug: Print the found path
    if path:
        print("Path found:", path)
    else:
        print("No path found.")

    # Draw the path (if any) in blue
    if path:
        for point in path:
            cv2.circle(maze, (point[1], point[0]), 3, (255, 0, 0), -1)  # Blue dots for the path

    # Show the maze with detected green walls and holes
    cv2.imshow("Maze Solver - Green Walls", green_mask_cleaned)
    cv2.imshow("Maze Solver - Holes Detection", hole_mask_cleaned)
    cv2.imshow("Maze Solver - Path (A*)", maze)

    # Exit the program when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

solver.cap.release()
cv2.destroyAllWindows()
