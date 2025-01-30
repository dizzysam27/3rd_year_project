import smbus

global bus,arduino_address
bus = smbus.SMBus(1)
arduino_address = 0x47

class ARDUINO:


    def write_to_arduino(self,value):
        try:
            bus.write_byte(arduino_address, value)
            print(f"Sent {value} to Arduino")
        except Exception as e:
            print(f"Error: {e}")
        