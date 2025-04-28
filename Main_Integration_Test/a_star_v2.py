import cv2
import numpy as np
from heapq import heappop, heappush

class MazeSolver:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.kernel = np.ones((11, 11), np.uint8)  # Smaller kernel for morphological operations
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
        #colours changed by archie
        lower_green = np.array([0, 85, 0])#np.array([35, 50, 50])
        upper_green = np.array([140, 196, 117])#np.array([85, 255, 255])
        #lower_green = np.array([40, 50, 50])   # Lower bound of green
        #upper_green = np.array([80, 255, 255]) # Upper bound of green

        # Threshold the image to get the green areas (walls)
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

        # Use additional morphological operations to clean the holes mask and reduce noise
        hole_mask_cleaned = cv2.morphologyEx(hole_mask, cv2.MORPH_CLOSE, self.kernel)
        hole_mask_cleaned = cv2.morphologyEx(hole_mask_cleaned, cv2.MORPH_OPEN, self.kernel)  # Erosion step to remove small noise

        return green_mask_cleaned, hole_mask_cleaned


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

        # Debug: Track progress
        print(f"Processing {current}, f_score={f_score[current]}")

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
start_point = (360, 605)  # (x, y)
end_point = (91, 400)  # (x, y)

while True:
    ret, frame = solver.cap.read()
    if not ret:
        break

    # Process the frame (apply crop)
    maze = solver.process_frame(frame)

    # Find the green walls and holes (masks for green and holes)
    green_mask_cleaned, hole_mask_cleaned = solver.find_green_walls_and_holes(maze)

    # Create grid based on the hole mask (1 = obstacle, 0 = free space)
    grid = np.zeros_like(hole_mask_cleaned)
    grid[hole_mask_cleaned == 255] = 1  # Mark walls as 1 (blocked space)

    # Debug: Visualize the grid (pathfinding)
    grid_visual = np.repeat(grid[:, :, np.newaxis], 3, axis=2) * 255
    cv2.imshow("Pathfinding Grid", grid_visual)

    # Ensure start and end points are free (0) in the grid
    if grid[start_point[0], start_point[1]] == 1:
        print(f"Start point {start_point} is blocked. Trying a nearby free space.")
        # Try adjusting the start point if it's blocked
        start_point = (min(start_point[0] + 1, hole_mask_cleaned.shape[0] - 1), start_point[1])
    if grid[end_point[0], end_point[1]] == 1:
        print(f"End point {end_point} is blocked. Trying a nearby free space.")
        # Try adjusting the end point if it's blocked
        end_point = (min(end_point[0] + 1, hole_mask_cleaned.shape[0] - 1), end_point[1])

    # Debug: Print grid and start/end points to validate
    print("Grid:")
    print(grid)
    print(f"Start: {start_point}, End: {end_point}")

    # Define the start and end points in terms of grid coordinates
    # Ensure the start and end points are inside the bounds of the hole mask
    start_point = (min(max(start_point[0], 0), hole_mask_cleaned.shape[0] - 1),
                  min(max(start_point[1], 0), hole_mask_cleaned.shape[1] - 1))
    
    #added by archie
    cv2.circle(frame, (start_point[0],start_point[1]), 3, (0, 0, 255), -1)

    end_point = (min(max(end_point[0], 0), hole_mask_cleaned.shape[0] - 1),
                min(max(end_point[1], 0), hole_mask_cleaned.shape[1] - 1))

    # Run A* to find the path
    path = astar(start_point, end_point, grid)

    # Draw the path (if any) in blue
    if path:
        for point in path:
            cv2.circle(maze, (point[1], point[0]), 3, (255, 0, 0), -1)  # Blue dots for the path
        cv2.imshow("Maze with Path", maze)
    else:
        print("No path found!")

    # Show the maze with detected green walls and holes
    cv2.imshow("Maze Solver - Green Walls", green_mask_cleaned)
    cv2.imshow("Maze Solver - Holes Detection", hole_mask_cleaned)

    # Exit the program when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

solver.cap.release()
cv2.destroyAllWindows()
