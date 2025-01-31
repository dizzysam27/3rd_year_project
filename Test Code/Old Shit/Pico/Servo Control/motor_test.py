import pantilthat
import time

# Function to set pan and tilt angles
def set_pan_tilt():
    while True:
        try:
            # Get user input for pan angle
            pan = float(input("Enter pan angle (-90 to 90): "))
            if not -90 <= pan <= 90:
                print("Pan angle must be between -90 and 90 degrees.")
                continue

            # Get user input for tilt angle
            tilt = float(input("Enter tilt angle (-90 to 90): "))
            if not -90 <= tilt <= 90:
                print("Tilt angle must be between -90 and 90 degrees.")
                continue

            # Set the pan and tilt angles
            pantilthat.pan(pan)
            pantilthat.tilt(tilt)
            print(f"Pan set to {pan}, Tilt set to {tilt}")

        except ValueError:
            print("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\nExiting...")
            break

# Main program
if __name__ == "__main__":
    print("Pan-Tilt Control Started")
    print("Press Ctrl+C to exit.")
    set_pan_tilt()
