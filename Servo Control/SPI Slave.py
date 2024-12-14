<<<<<<< HEAD
from machine import Pin, SPI

# Initialize SPI (slave mode)
spi = SPI(0, baudrate=500000, polarity=0, phase=0,
          sck=Pin(18), mosi=Pin(19), miso=Pin(16))
cs = Pin(17, Pin.IN)  # Chip select (use appropriate GPIO)

buffer = bytearray(3)  # Buffer size matches master data length

while True:
    if not cs.value():  # Active low
        spi.readinto(buffer)
        print("Received from Master:", buffer)
        # Optionally send a response
        spi.write(b'\xAA\xBB\xCC')  # Example response
=======
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
>>>>>>> 1f1ca834d309594e538bee280b17782bc0aa8864
