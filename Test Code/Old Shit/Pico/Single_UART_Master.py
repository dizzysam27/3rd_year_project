import serial
import time


uart3 = serial.Serial('/dev/serial1', 9600, timeout=1)


def send_data_uart3(data):
    uart3.write(data.encode('utf-8'))
    #print("Sent UART3: " ,data)

def read_data_uart3():
    if uart3.in_waiting > 0:
        return uart3.read(uart3.in_waiting).decode('utf-8', errors='ignore')
    return None

# Example usage
try:
    while True:
        # Send data to the Pico
        
        send_data_uart3("Hello from Raspberry Pi on UART3\n")
        
        # Read data from Pico

        response_uart3 = read_data_uart3()
        if response_uart3:
            print(f"Received from Pico on UART3: {response_uart3}")
        
        time.sleep(0.01)  # Delay before sending next message

except KeyboardInterrupt:
    print("Program terminated.")
finally:
    uart3.close()
