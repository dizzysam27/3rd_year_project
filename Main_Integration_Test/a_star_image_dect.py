import cv2
import numpy as np
import heapq
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
        self.change = 50
        self.gx, self.gy = 510, 390  # Goal position

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
        hsv = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)

        # Detect obstacles (black regions)
        gray = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)[1]
        _, bcontours = self.find_and_fill_contours(thresh, cropped_frame)

        # Detect ball position
        ball_center = self.detect_ball(cropped_frame)

        return bcontours, ball_center

    def find_and_fill_contours(self, mask, frame):
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > self.min_contour_area:
                x, y, w, h = cv2.boundingRect(contour)
                cx, cy = x + w // 2, y + h // 2
                self.line_coordinates.append((cx, cy))
        return contours

    def detect_ball(self, cropped_frame):
        gray = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
        cleaned_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 6)
        circles = cv2.HoughCircles(cleaned_thresh, cv2.HOUGH_GRADIENT, 1, 20, param1=130, param2=20, minRadius=2, maxRadius=20)
        
        if circles is not None:
            circles = circles[0, :]
            largest_circle = max(circles, key=lambda c: c[2], default=None)
            if largest_circle is not None:
                return (int(largest_circle[0]), int(largest_circle[1]))  # Convert to integer
        return None

    def create_maze_grid(self, frame_size):
        """Creates a binary grid representing the maze (0 = open, 1 = obstacle)."""
        height, width = frame_size
        grid = np.zeros((height, width), dtype=np.uint8)

        for (x, y) in self.line_coordinates:
            if 0 <= x < width and 0 <= y < height:
                grid[y, x] = 1  # Mark obstacles

        return grid

    def heuristic(self, a, b):
        """Calculate Euclidean distance heuristic."""
        return np.linalg.norm(np.array(a) - np.array(b))

    def astar(self, grid, start, goal):
        """A* pathfinding algorithm."""
        rows, cols = grid.shape
        open_set = []
        heapq.heappush(open_set, (0, start))  # Priority queue (F-score, node)

        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:  # 4 directions
                neighbor = (current[0] + dx, current[1] + dy)

                if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor] == 0:
                    tentative_g_score = g_score[current] + 1  # Cost to move

                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None  # No path found

    def move_along_path(self, path):
        """Moves motors based on A* computed path."""
        if path:
            for px, py in path:
                offset_x = self.gx - px
                offset_y = self.gy - py

                if abs(offset_x) > 20:
                    self.adjust_motor(1, 100 if offset_x > 0 else -100)

                if abs(offset_y) > 20:
                    self.adjust_motor(0, 100 if offset_y > 0 else -100)

                time.sleep(0.1)  # Small delay for smooth movement

    def adjust_motor(self, motor_index, change):
        if motor_index == 0:
            self.motors.setServoPulse(0, self.defaulty + change)
        elif motor_index == 1:
            self.motors.setServoPulse(1, self.defaultx + change)

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break

            bcontours, ball_center = self.process_frame(frame)
            
            if ball_center:
                maze_grid = self.create_maze_grid(frame.shape[:2])
                start = (ball_center[1], ball_center[0])  # Flip (x, y) -> (row, col)
                goal = (self.gy, self.gx)

                path = self.astar(maze_grid, start, goal)

                if path:
                    self.move_along_path(path)
                else:
                    print("No valid path found!")

            cv2.imshow('Processed Frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cleanup()

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()
        print("Process stopped.")

# Run the processor
processor = ImageProcessor()
processor.run()
