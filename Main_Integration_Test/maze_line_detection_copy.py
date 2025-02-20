import cv2
import numpy as np
from Peripherals.Motor_Control import PCA9685
import time

class IMAGEPROCESSING:
    
    def __init__(self):
        motors = PCA9685()
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: Could not open webcam.")
            exit()

        # Create a window for display
        #cv2.namedWindow('Video')
        # List to store coordinates
        line_coordinates = []
        # Define the minimum area threshold for contours
        min_contour_area = 1000  # Adjust this value to fit your needs
        # Kernel for morphological operations (size can be adjusted)
        kernel = np.ones((15, 15), np.uint8)  # Larger kernels will help close larger gaps

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break

            # Get frame dimensions
            frame_height, frame_width = frame.shape[:2]
            crop_width = 1000
            crop_height = 700
            x_offset = 30
            y_offset = 30

            # Calculate start and end coordinates for the central region
            start_x = (frame_width - crop_width) // 2
            end_x = start_x + crop_width

            start_y = (frame_height - crop_height) // 2
            end_y = start_y + crop_height

            # Perform the actual cropping
            cropped_frame = frame[start_y + y_offset :end_y + y_offset, start_x + x_offset :end_x + x_offset]

            # Convert to HSV (Hue, Saturation, Value)
            hsv = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)

            # Define the range of green color in HSV
            lower_green = np.array([35, 50, 50])  # Lower bound of green
            upper_green = np.array([85, 255, 255])  # Upper bound of green

            # Threshold the image to isolate green regions
            gmask = cv2.inRange(hsv, lower_green, upper_green)
            #cv2.imshow('Green Mask', gmask)  # Show the green mask

            # Find contours on the mask
            gcontours, ghierarchy = cv2.findContours(gmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # Fill contours with black color
            gfilled_frame = cropped_frame.copy()  # Create a copy to fill contours on

            gfilled_frame2 = np.zeros_like(cropped_frame)  # Create a copy to fill contours on

            for contour in gcontours:
                # Get the area of the contour
                area = cv2.contourArea(contour)

                # Only consider contours larger than the minimum area
                if area > min_contour_area:
                    # Get the bounding box of the contour
                    x, y, w, h = cv2.boundingRect(contour)

                    # Store the center coordinates of the green region
                    cx, cy = x + w // 2, y + h // 2
                    line_coordinates.append((cx, cy))

                    # Fill the contour with green
                    cv2.drawContours(gfilled_frame, [contour], -1, (0, 0, 255), thickness=cv2.FILLED)

                    # Only contours
                    cv2.drawContours(gfilled_frame2, [contour], -1, (0, 0, 255), thickness=cv2.FILLED)

            # Apply morphological operations to close gaps after finding contours
            gclosed_thresh = cv2.morphologyEx(gfilled_frame2, cv2.MORPH_CLOSE, kernel)
            #cv2.imshow('g Closed Image', gclosed_thresh)  # Show the closed image

            # Display the filled frame
            #cv2.imshow('g Filled Contours', gfilled_frame)

            # Display the closed frame
            #cv2.imshow('g Filled Contours After Morphology', gclosed_thresh)

            # Convert to grayscale
            gray = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
            #cv2.imshow('Grayscale', gray)  # Show grayscale image
            # Threshold to isolate black regions
            ret, thresh = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)



            
                # Convert the cropped frame to HSV color space
            hsv = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)

            # Define HSV range for detecting silver-like regions
            # Experiment with these values to match the ball's appearance
            lower_silver = np.array([0, 0, 160])  # Low saturation, high brightness
            upper_silver = np.array([180, 50, 255])  # Adjust for lighting variations

            # Create a mask for silver regions
            silver_mask = cv2.inRange(hsv, lower_silver, upper_silver)

            # Apply morphological operations to clean up the mask
            kernel = np.ones((5, 5), np.uint8)
            silver_mask_cleaned = cv2.morphologyEx(silver_mask, cv2.MORPH_CLOSE, kernel)

            # Show the silver mask
            #cv2.imshow('Silver Mask', silver_mask_cleaned)


            # Convert the cropped frame to grayscale
            cropped_frame_gray = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)


                # Apply adaptive thresholding
            threshball = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 6
                
            )

            # Morphological operations to clean noise
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            cleaned_thresh = cv2.morphologyEx(threshball, cv2.MORPH_OPEN, kernel)

            # Filter contours by size to remove noise
            contours, _ = cv2.findContours(threshball, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            final_mask = np.zeros_like(threshball)

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 10:  # Adjust the size threshold based on your noise characteristics
                    cv2.drawContours(final_mask, [cnt], -1, 255, -1)

            # Final cleaned binary image
            cleaned_image = final_mask

            #cv2.imshow('cleaned ball 1', cleaned_thresh)  # Show cleaned image
            #cv2.imshow('Cleaned Ball 2', cleaned_image)  # Show cleaned image


            #cv2.imshow('Thresholded Ball', threshball)  # Show thresholded image

            #cv2.imshow('Thresholded', thresh)  # Show thresholded image
            # Find contours on the thresholded image
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # Fill contours with black color
            filled_frame = cropped_frame.copy()  # Create a copy to fill contours on
            filled_frame2 = np.zeros_like(cropped_frame)  # Create a copy to fill contours on

            for contour in contours:
                # Get the area of the contour
                area = cv2.contourArea(contour)

                # Only consider contours larger than the minimum area
                if area > min_contour_area:
                    # Get the bounding box of the contour
                    x, y, w, h = cv2.boundingRect(contour)

                    # Store the center coordinates of the black line segment
                    cx, cy = x + w // 2, y + h // 2
                    line_coordinates.append((cx, cy))

                    # Fill the contour with green
                    cv2.drawContours(filled_frame, [contour], -1, (57, 255, 20), thickness=cv2.FILLED)

                    # Only contours
                    cv2.drawContours(filled_frame2, [contour], -1, (57, 255, 20), thickness=cv2.FILLED)

            # FIND BALL
        
            ballx = -1
            bally = -1
            
            # Detect circles using HoughCircles
            # Detect circles using HoughCircles
            circles = cv2.HoughCircles(cleaned_thresh, cv2.HOUGH_GRADIENT, 1, 20, param1=130, param2=20, minRadius=2, maxRadius=20)

            

            if circles is not None:
                circles = circles[0, :]  # First element (list of detected circles)

                # Initialize variables for the largest circle
                largest_circle = None
                largest_radius = 0

                for circle in circles:
                    # Get precise (floating-point) center values
                    x, y, r = circle[0], circle[1], circle[2]

                    # Check if the current circle has the largest radius
                    if r > largest_radius:
                        largest_radius = r
                        largest_circle = (x, y, r)

                # If a largest circle was found, save its center coordinates (floating point precision)
                if largest_circle:
                    x, y, r = largest_circle  # Largest circle's center (x, y) and radius
                    
                    # Format to 2 decimal places for display
                    print(f"Largest Circle Center: ({x:.2f}, {y:.2f}), Radius: {r:.2f}")

                    # Draw the largest circle on the frame (convert to integers only for drawing)
                    cv2.circle(filled_frame, (int(x), int(y)), int(r), (255, 0, 0), 2)  # Blue circle outline
                    cv2.circle(filled_frame, (int(x), int(y)), 2, (0, 255, 0), 3)  # Green center dot

                    # Ball's center coordinates
                    ball_center = (x, y)

                    gx = 510
                    gy = 390

                    cv2.circle(filled_frame, (int(gx), int(gy)), 2, (0, 0, 255), 3) 

                    bx, by = ball_center

                    # Calculate the x and y offset between the ball and the green center
                    offset_x = gx - bx
                    offset_y = gy - by

                    print(f"Ball offset: x={offset_x}, y={offset_y}")
                    changex = 300
                    changey = 300
                    defaultx = 1870
                    defaulty = 1925
                    change = 50
                    # Control logic to move motors based on the offsets
                    if offset_x > 20:  # Threshold for moving motor on X axis
                        
                        changex = 100

                    if offset_x < -20:  # Threshold for moving motor on X axis
                        
                        changex = -100
                    if offset_y > 20:  #Threshold for moving motor on Y axis
                        
                        changey = 100
                    if offset_y < -20:  # Threshold for moving motor on Y axis
                        
                        changey = -100
                    print(changex,changey)
                    if changex == 300:
                        if changey != 300:
                            if changey < 0:
                                motors.setServoPulse(0,defaulty-change)
                            if changey > 0:
                                motors.setServoPulse(0,defaulty+change)
                    elif changey == 300:
                        if changex != 300:
                            if changex > 0:
                                motors.setServoPulse(1,defaultx+change)
                            if changex < 0:
                                motors.setServoPulse(1,defaultx-change)
                    elif changex != 300 and changey != 300:
                        #motors.motorAngle(changex,changey)
                        if changey < 0:
                            if changex > 0:
                                motors.setServoPulse(1,defaultx+change)
                                motors.setServoPulse(0,defaulty-change)
                            if changex < 0:
                                motors.setServoPulse(1,defaultx-change)
                                motors.setServoPulse(0,defaulty-change)
                        if changey > 0:
                            if changex > 0:
                                motors.setServoPulse(1,defaultx+change)
                                motors.setServoPulse(0,defaulty+change)
                            if changex < 0:
                                motors.setServoPulse(1,defaultx-change)
                                motors.setServoPulse(0,defaulty+change)
                    else:
                        motors.setServoPulse(1,defaultx)
                        motors.setServoPulse(0,defaulty)
                else:
                    motors.setServoPulse(1,defaultx)
                    motors.setServoPulse(0,defaulty)
            else:
                motors.setServoPulse(1,defaultx)
                motors.setServoPulse(0,defaulty)

            time.sleep(0.001)
                    
                        








            
            # Apply morphological operations to close gaps after finding contours
            closed_thresh = cv2.morphologyEx(filled_frame2, cv2.MORPH_CLOSE, kernel)
            #cv2.imshow('Closed Image', closed_thresh)  # Show the closed image
            # Display the filled frame
            cv2.imshow('Filled Contours', filled_frame)
            # Display the closed frame
            #cv2.imshow('Filled Contours After Morphology', closed_thresh)
            # Combine the green and black filled contours after morphology
            combined_image = cv2.addWeighted(gclosed_thresh, 0.5, closed_thresh, 0.5, 0)
            # Display the combined image
            #cv2.imshow('Combined Filled Contours After Morphology', combined_image)
            print('hello')
            #cv2.imshow('Video', cropped_frame_gray)
            # Break the loop on 'q' key press

            #cv2.imshow('cleaned ball 1', cleaned_thresh)  # Show cleaned image


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Save coordinates to a file (optional)
        with open('line_coordinates.txt', 'w') as f:
            for coord in line_coordinates:
                f.write(f"{coord}\n")

        # Release the webcam and close windows
        cap.release()
        cv2.destroyAllWindows()

        print("Coordinates of black line segments have been saved to 'line_coordinates.txt'.")

run = IMAGEPROCESSING()