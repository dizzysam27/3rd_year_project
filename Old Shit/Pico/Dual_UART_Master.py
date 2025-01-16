import serial
import time

# Open UART0 (ttyAMA0) on the Raspberry Pi (ensure UART is enabled)
uart0 = serial.Serial('/dev/serial1', 9600, timeout=1)
uart3 = serial.Serial('/dev/ttyAMA3', 9600, timeout=1)

# Function to send data to Pico
def send_data_uart0(data):
    uart0.write(data.encode('utf-8'))
    #print("Sent UART0: " ,data)

def send_data_uart3(data):
    uart3.write(data.encode('utf-8'))
    #print("Sent UART3: " ,data)

# Function to read data from Pico
def read_data_uart0():
    if uart0.in_waiting > 0:
        return uart0.readline(uart0.in_waiting).decode('utf-8')
    return None

def read_data_uart3():
    if uart3.in_waiting > 0:
        return uart3.read(uart3.in_waiting).decode('utf-8', errors='ignore')
    return None

# Example usage
try:
    while True:
        # Send data to the Pico
        send_data_uart0("Hello from Raspberry Pi on UART0\n")
        send_data_uart3("Hello from Raspberry Pi on UART3\n")
        
        # Read data from Pico
        response_uart0 = read_data_uart0()
        response_uart3 = read_data_uart3()
        if response_uart0:
            print(f"Received from Pico on UART0: {response_uart0}")
        if response_uart3:
            print(f"Received from Pico on UART3: {response_uart3}")
        
        time.sleep(0.01)  # Delay before sending next message

except KeyboardInterrupt:
    print("Program terminated.")
finally:
    uart0.close()
    uart3.close()
