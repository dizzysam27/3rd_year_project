import RPi.GPIO as GPIO
import time

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pin configuration
SERVO_PIN = 18  # Choose the GPIO pin connected to the servo motor

# Initialize PWM parameters
FREQ = 50  # Servo frequency in Hz (most servos operate at 50 Hz)

# Setup GPIO pin as output
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Create PWM instance
pwm = GPIO.PWM(SERVO_PIN, FREQ)
pwm.start(0)  # Start PWM with 0% duty cycle

def set_angle(angle):
    """Set the servo angle.

    Args:
        angle (float): Desired angle between 0 and 180 degrees.
    """
    if 0 <= angle <= 180:
        duty_cycle = 2.5 + (angle / 180.0) * 10  # Map angle to duty cycle
        pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.5)  # Allow time for the servo to move to the position
    else:
        print("Angle out of range. Please enter a value between 0 and 180.")

def servo_sweep():
    """Sweep the servo back and forth between 0 and 180 degrees."""
    try:
        while True:
            for angle in range(0, 181, 1):  # Sweep from 0 to 180 degrees
                set_angle(angle)
            for angle in range(180, -1, -1):  # Sweep from 180 to 0 degrees
                set_angle(angle)
    except KeyboardInterrupt:
        print("\nExiting sweep...")

try:
    # Start servo sweep
    print("Starting servo sweep. Press Ctrl+C to stop.")
    servo_sweep()
except KeyboardInterrupt:
    print("\nExiting program...")
finally:
    pwm.stop()
    GPIO.cleanup()

