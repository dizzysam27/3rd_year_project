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
