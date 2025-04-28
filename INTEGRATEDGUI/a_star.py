# --- Necessary Imports ---
import cv2
import numpy as np
from heapq import heappop, heappush
import time
import math
# Removed: simple_pid, PCA9685, get_flat_values, deque, argparse

# --- Constants ---
NUM_WAYPOINTS = 50 # Number of points to simplify A* path into

# A* Related Constants
HOLE_DARKNESS_THRESHOLD = 85
LOWER_GREEN = np.array([35, 50, 50]); UPPER_GREEN = np.array([85, 255, 255])
HOLE_REPULSION_STRENGTH = 50.0
HOLE_REPULSION_THRESHOLD_NORM = 0.2


# --- Helper Function for Path Simplification ---
def simplify_path_by_sampling(path_points, num_points):
    """Simplifies a path by sampling approximately num_points points."""
    if not path_points or num_points <= 0: return []
    path_len = len(path_points);
    if path_len <= num_points: return path_points
    step = max(1, path_len // num_points)
    simplified = path_points[::step]
    # Ensure the very last point is always included if missed
    # Check using tuples for reliable comparison with list/numpy points
    if tuple(path_points[-1]) != tuple(simplified[-1]):
         simplified.append(path_points[-1])
    print(f"Simplified path from {path_len} to {len(simplified)} waypoints.")
    # Return list of tuples with integer coordinates
    return [tuple(map(int, p)) for p in simplified]


# --- MazeSolver Class ---
class MazeSolver:
    def __init__(self):
        # --- Camera Setup (from reference) ---
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        if not self.cap.isOpened(): print("Error: Could not open webcam."); exit()
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"Camera opened at {self.frame_width}x{self.frame_height}")

        # --- Pathfinding State ---
        self.stored_path_yx = None; self.waypoints_yx = None # Waypoints added
        self.path_found_and_generated = False # Renamed flag
        self.stored_green_mask = None # Store masks from A* frame
        self.stored_hole_mask = None
        self.final_frame = None # Store frame for static display

        # --- Detection Parameters ---
        self.detection_kernel = np.ones((5, 5), np.uint8) # Kernel for walls/holes
        self.hole_darkness_threshold = HOLE_DARKNESS_THRESHOLD
        self.lower_green = LOWER_GREEN; self.upper_green = UPPER_GREEN

        # --- Path Repulsion Parameters (Only used for A* generation) ---
        self.hole_repulsion_strength = HOLE_REPULSION_STRENGTH
        self.hole_repulsion_threshold_norm = HOLE_REPULSION_THRESHOLD_NORM

    # --- UPDATED Crop Frame ---
    def crop_frame(self, frame):
        """Crops frame to user-specified 350x260."""
        frame_height, frame_width = frame.shape[:2]
        crop_width = 330 # User specified << UPDATED
        crop_height = 240 # User specified << UPDATED
        x_offset, y_offset = 0, 0 # Keep centered unless specified otherwise
        start_x = (frame_width - crop_width) // 2 + x_offset
        end_x = start_x + crop_width
        start_y = (frame_height - crop_height) // 2 + y_offset
        end_y = start_y + crop_height
        # Clamp to frame boundaries
        start_y_clamped = max(0, start_y); end_y_clamped = min(frame_height, end_y)
        start_x_clamped = max(0, start_x); end_x_clamped = min(frame_width, end_x)
        if start_y_clamped >= end_y_clamped or start_x_clamped >= end_x_clamped:
             print(f"Warning: Invalid crop {crop_width}x{crop_height}. Using full frame {frame_width}x{frame_height}."); return None
        return frame[start_y_clamped:end_y_clamped, start_x_clamped:end_x_clamped]

    # --- Wall/Hole Feature Detection (A* version's logic) ---
    def detect_features(self, frame):
        # (Logic unchanged)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY); hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV); kernel = self.detection_kernel
        _, dark_regions_mask = cv2.threshold(gray, self.hole_darkness_threshold, 255, cv2.THRESH_BINARY_INV)
        hole_mask_cleaned = cv2.morphologyEx(dark_regions_mask, cv2.MORPH_OPEN, kernel); hole_mask_cleaned = cv2.morphologyEx(hole_mask_cleaned, cv2.MORPH_CLOSE, kernel, iterations=1)
        green_mask = cv2.inRange(hsv, self.lower_green, self.upper_green)
        green_mask_cleaned = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, kernel, iterations=1); green_mask_cleaned = cv2.morphologyEx(green_mask_cleaned, cv2.MORPH_OPEN, kernel, iterations=1)
        not_wall_mask = cv2.bitwise_not(green_mask_cleaned); final_hole_mask = cv2.bitwise_and(hole_mask_cleaned, not_wall_mask)
        return green_mask_cleaned, final_hole_mask

    # --- Find Nearest Valid Point for A* (A* version's logic) ---
    def find_nearest_valid_point(self, point_yx, validation_obstacle_mask):
        # (Logic unchanged)
        r, c = point_yx; h, w = validation_obstacle_mask.shape
        if not (0 <= r < h and 0 <= c < w): return None
        if validation_obstacle_mask[r, c] == 0: return point_yx
        max_search_radius = 30
        for radius_search in range(1, max_search_radius + 1):
            for dr in range(-radius_search, radius_search + 1):
                for dc in range(-radius_search, radius_search + 1):
                    if abs(dr) != radius_search and abs(dc) != radius_search: continue
                    nr, nc = r + dr, c + dc
                    if not (0 <= nr < h and 0 <= nc < w): continue
                    if validation_obstacle_mask[nr, nc] == 0: return (nr, nc)
        print(f"Could not find valid point near {point_yx}."); return None


    # --- Main Run Method (Finds path, prints waypoints, shows static result) ---
    def run(self):

        # --- Define A* start/end points relative to the NEW CROP (350x260) ---
        start_point_yx = (250, 140) # User specified Y, X << UPDATED
        end_point_yx   = (120, 25)  # User specified Y, X << UPDATED
        # ---
        print(f"--- Using A* Start: {start_point_yx}, End: {end_point_yx} (relative to {350}x{260} crop) ---")

        # Loop until path is found or user quits
        while not self.path_found_and_generated:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                time.sleep(0.5); continue

            processed_frame = self.crop_frame(frame)
            if processed_frame is None or processed_frame.size == 0:
                print("Error: Cropping failed. Check camera resolution vs crop size.")
                time.sleep(0.5); continue # Skip this frame

            print("Detecting features and finding/simplifying path...")
            current_green_mask, current_hole_mask = self.detect_features(processed_frame)
            self.stored_green_mask = current_green_mask # Store for final display
            self.stored_hole_mask = current_hole_mask
            validation_obstacle_mask = cv2.bitwise_or(current_green_mask, current_hole_mask)

            free_space_mask_inv_holes = cv2.bitwise_not(current_hole_mask)
            dist_from_holes = cv2.distanceTransform(free_space_mask_inv_holes, cv2.DIST_L2, 5)
            cv2.normalize(dist_from_holes, dist_from_holes, 0, 1.0, cv2.NORM_MINMAX)

            h_crop, w_crop = processed_frame.shape[:2]
            # Use the NEW start/end points, clamped to this crop
            start_r = max(0, min(start_point_yx[0], h_crop - 1)); start_c = max(0, min(start_point_yx[1], w_crop - 1))
            end_r = max(0, min(end_point_yx[0], h_crop - 1)); end_c = max(0, min(end_point_yx[1], w_crop - 1))
            valid_start = self.find_nearest_valid_point((start_r, start_c), validation_obstacle_mask)
            valid_end = self.find_nearest_valid_point((end_r, end_c), validation_obstacle_mask)


            path = None
            if valid_start and valid_end:
                print(f"Running A* from {valid_start} to {valid_end}")
                path = astar_repulsive(valid_start, valid_end, processed_frame.shape[:2],
                                       current_green_mask, dist_from_holes,
                                       self.hole_repulsion_strength,
                                       self.hole_repulsion_threshold_norm)
                if path:
                    self.stored_path_yx = path
                    self.waypoints_yx = simplify_path_by_sampling(self.stored_path_yx, NUM_WAYPOINTS)
                    if not self.waypoints_yx:
                         print("Error: Path simplification failed. Retrying...")
                         time.sleep(1) # Wait before retry
                    else:
                        self.path_found_and_generated = True # Signal success
                        self.final_frame = processed_frame.copy() # Store frame for display
                        print(f"Path Found ({len(self.stored_path_yx)} pts). Simplified to {len(self.waypoints_yx)} Waypoints.")

                        # --- Output Waypoints as Array ---
                        waypoints_np_yx = np.array(self.waypoints_yx, dtype=np.int32)
                        x_coords = waypoints_np_yx[:, 1] # Second column is X
                        y_coords = waypoints_np_yx[:, 0] # First column is Y
                        print("\n--- Generated Waypoint X Coordinates ---")
                        print(f"Array Shape: {x_coords.shape}")
                        print(repr(x_coords)) # Use repr for clear array output
                        print("\n--- Generated Waypoint Y Coordinates ---")
                        print(f"Array Shape: {y_coords.shape}")
                        print(repr(y_coords)) # Use repr for clear array output
                        print("------------------------------------")
                        # --- End Output ---
                        break # Exit pathfinding loop after success
                else:
                    print("A* failed to find a path this frame. Retrying...")
                    time.sleep(1)
            else:
                print("Invalid A* start/end points found. Retrying...")
                time.sleep(1)

        self.cap.release()
        return waypoints_np_yx

        
      

    # --- UPDATED Cleanup Method (No motors) ---
    def cleanup(self):
        # Removed motor centering logic
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("Cleanup complete.")


# --- A* Function (keep separate) ---
def astar_repulsive(start, end, grid_shape, green_wall_mask, dist_from_holes, repulsion_strength, repulsion_threshold_norm):
    # (A* logic unchanged)
    def heuristic(a, b): return abs(a[0] - b[0]) + abs(a[1] - b[1])
    open_set = []; heappush(open_set, (heuristic(start, end), 0, start))
    came_from = {}; g_score = {start: 0}; f_score = {start: heuristic(start, end)}
    while open_set:
        current_f, current_g, current = heappop(open_set)
        if current_f > f_score.get(current, float('inf')): continue
        if current == end:
            path = []; temp = current
            while temp in came_from: path.append(temp); temp = came_from[temp]
            path.append(start); return path[::-1]
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy); r, c = neighbor
            if not (0 <= r < grid_shape[0] and 0 <= c < grid_shape[1]): continue
            if green_wall_mask[r, c] == 255: continue
            base_cost = 1.0; repulsion_cost = 0.0
            if repulsion_strength > 0 and 0 <= r < dist_from_holes.shape[0] and 0 <= c < dist_from_holes.shape[1]:
                 dist_norm = dist_from_holes[r, c]
                 if dist_norm < repulsion_threshold_norm:
                    penalty_factor = (repulsion_threshold_norm - dist_norm) / repulsion_threshold_norm
                    repulsion_cost = repulsion_strength * penalty_factor
            movement_cost = base_cost + repulsion_cost
            tentative_g_score = current_g + movement_cost
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current; g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                heappush(open_set, (f_score[neighbor], tentative_g_score, neighbor))
    print("No path found!"); return None


# --- Main Execution ---
if __name__ == "__main__":
    solver = MazeSolver()
    try:
        # Run the simplified process: find path, print waypoints, display static result
        solver.run()
    except KeyboardInterrupt:
        print("\nManual interruption detected.")
    finally:
        # Ensure cleanup happens
        solver.cleanup()