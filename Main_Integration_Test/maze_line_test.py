import cv2
import numpy as np

def crop_frame(frame):
        frame_height, frame_width = frame.shape[:2]
        crop_width, crop_height = 370, 280
        x_offset, y_offset = 10, -10

        start_x = (frame_width - crop_width) // 2
        end_x = start_x + crop_width
        start_y = (frame_height - crop_height) // 2
        end_y = start_y + crop_height

        return frame[start_y + y_offset:end_y + y_offset, start_x + x_offset:end_x + x_offset]

def find_and_fill_contours(mask, frame):
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    filled_frame = frame.copy()
    for contour in contours:
        area = cv2.contourArea(contour)
        largest_contour = max(contours, key=cv2.contourArea)
    

        x, y, w, h = cv2.boundingRect(largest_contour)
        cx, cy = x + w // 2, y + h // 2
        cv2.drawContours(filled_frame, [largest_contour], -1, (0, 255, 0), thickness=cv2.FILLED)
    return filled_frame, contours

# Open the camera
cap = cv2.VideoCapture(0)  # Change index if using an external camera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)


while True:
    ret, frame = cap.read()
    if not ret:
        break  # Stop if no frame is captured
    
    
    frame = crop_frame(frame)
    cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX)


    


    lower_blue, upper_blue = np.array([166,122,63]), np.array([255,198,166])
    bmask = cv2.inRange(frame, lower_blue, upper_blue)

    gfilled_frame, gcontours = find_and_fill_contours(bmask, frame)

    if gcontours:
        # Get the largest contour
        contour = max(gcontours, key=cv2.contourArea)

        # Approximate the contour for simplicity
        epsilon = 0.001 * cv2.arcLength(contour, False)
        approx = cv2.approxPolyDP(contour, epsilon, False)
        points = approx.reshape(-1, 2)

        # Compute distances between points to get total curve length
        distances = np.cumsum(
            [0] + [np.linalg.norm(points[i] - points[i - 1]) for i in range(1, len(points))]
        )
        total_length = distances[-1]

        # Normalize distances to [0, 1]
        distances /= total_length

        # Interpolate 100 evenly spaced points
        num_points = 400
        evenly_spaced_alphas = np.linspace(0, 1, num_points)
        interpolated_points = []

        for alpha in evenly_spaced_alphas:
            idx = np.searchsorted(distances, alpha)
            if idx == 0:
                interpolated_points.append(points[0])
            elif idx >= len(points):
                interpolated_points.append(points[-1])
            else:
                t = (alpha - distances[idx - 1]) / (distances[idx] - distances[idx - 1])
                interp_point = (1 - t) * points[idx - 1] + t * points[idx]
                interpolated_points.append(interp_point)

        interpolated_points = np.array(interpolated_points, dtype=int)

        # Draw points on the frame
        for (x, y) in interpolated_points:
            cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)

        # Optional: print coordinates
        print("Sampled 100 points:", interpolated_points)

  

    # Show the output
    cv2.imshow('Black Line Detection', frame)
    
    combined_image = cv2.addWeighted(gfilled_frame, 0.5, frame, 0.5, 0)
    cv2.imshow('Combined Filled Contours', combined_image)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
