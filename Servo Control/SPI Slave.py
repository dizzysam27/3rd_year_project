import spidev
import time

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, Device 0 (CS0)
spi.max_speed_hz = 500000  # Adjust speed as needed
try:
    while True:
        # Send data to Pico and receive response
        data = spi.xfer2([0x01, 0x02, 0x03])  # Example data
        print("Received:", data)
        time.sleep(1)
        print("Sending:", [0x01, 0x02, 0x03])
        data = spi.xfer2([0x01, 0x02, 0x03])
        print("Received:", data)

except KeyboardInterrupt:
    spi.close()
