import smbus

class ARDUINO:
    
    def __int__(self):
        self.bus = smbus.SMBus(1)
        self.arduino_address = 0x08

    def write_to_arduino(self,value):
        try:
            self.bus.write_byte(self.arduino_address, value)
            print(f"Sent {value} to Arduino")
        except Exception as e:
            print(f"Error: {e}")
        
arduino = ARDUINO()
arduino.write_to_arduino(42) 
