import serial
import time

# Initialize serial connection to match the Pico's UART configuration
serial_port = "/dev/serial0"  # Use "/dev/serial0" for Raspberry Pi's UART
baud_rate = 9600
timeout = 1  # 1-second timeout

try:
    # Open the serial connection
    ser = serial.Serial(serial_port, baud_rate, timeout=timeout)
    print(f"Serial connection established on {serial_port} at {baud_rate} baud.")
except Exception as e:
    print(f"Failed to open serial connection: {e}")
    exit()

def send_data(data):
    """Send data over UART."""
    try:
        ser.write(data.encode('utf-8'))
        print("Sent:", data)
    except Exception as e:
        print("Error sending data:", e)

def read_data():
    """Read data from UART."""
    try:
        if ser.in_waiting > 0:
            received_data = ser.readline().decode('utf-8').strip()
            print("Received:", received_data)
            return received_data
    except Exception as e:
        print("Error reading data:", e)
    return None

# Main loop
try:
    while True:
        # Check for incoming data
        data = read_data()
        
        if data:
            # Respond to the Pico
            response = "Hello from Raspberry Pi 5\n"
            send_data(response)
        
        time.sleep(1)  # Avoid spamming the serial interface
except KeyboardInterrupt:
    print("\nExiting program.")
finally:
    ser.close()
    print("Serial connection closed.")
