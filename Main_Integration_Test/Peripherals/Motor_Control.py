#!/usr/bin/python

import time
import math
import smbus

# ============================================================================
# Raspi PCA9685 16-Channel PWM Servo Driver
# ============================================================================

class PCA9685:

  # Registers/etc.
  __SUBADR1            = 0x02
  __SUBADR2            = 0x03
  __SUBADR3            = 0x04
  __MODE1              = 0x00
  __PRESCALE           = 0xFE
  __LED0_ON_L          = 0x06
  __LED0_ON_H          = 0x07
  __LED0_OFF_L         = 0x08
  __LED0_OFF_H         = 0x09
  __ALLLED_ON_L        = 0xFA
  __ALLLED_ON_H        = 0xFB
  __ALLLED_OFF_L       = 0xFC
  __ALLLED_OFF_H       = 0xFD

  def __init__(self, address=0x40, debug=False):
    self.bus = smbus.SMBus(1)
    self.address = address
    self.debug = debug
    if (self.debug):
      print("Reseting PCA9685")
    self.write(self.__MODE1, 0x00)
    self.calibrate()
    self.motorAngle(0,0)

    #self.motorAngle(0,0)
    #time.sleep(2)
    #self.motorAngle(100,100)
    #time.sleep(2)
    #self.motorAngle(0,0)
    #time.sleep(2)
	
  def write(self, reg, value):
    "Writes an 8-bit value to the specified register/address"
    self.bus.write_byte_data(self.address, reg, value)
    if (self.debug):
      print("I2C: Write 0x%02X to register 0x%02X" % (value, reg))
	  
  def read(self, reg):
    "Read an unsigned byte from the I2C device"
    result = self.bus.read_byte_data(self.address, reg)
    if (self.debug):
      print("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" % (self.address, result & 0xFF, reg))
    return result
	
  def setPWMFreq(self, freq):
    "Sets the PWM frequency"
    prescaleval = 25000000.0    # 25MHz
    prescaleval /= 4096.0       # 12-bit
    prescaleval /= float(freq)
    prescaleval -= 1.0
    if (self.debug):
      print("Setting PWM frequency to %d Hz" % freq)
      print("Estimated pre-scale: %d" % prescaleval)
    prescale = math.floor(prescaleval + 0.5)
    if (self.debug):
      print("Final pre-scale: %d" % prescale)

    oldmode = self.read(self.__MODE1);
    newmode = (oldmode & 0x7F) | 0x10        # sleep
    self.write(self.__MODE1, newmode)        # go to s
    self.write(self.__MODE1, newmode)        # go to sleep
    self.write(self.__PRESCALE, int(math.floor(prescale)))
    self.write(self.__MODE1, oldmode)
    time.sleep(0.005)
    self.write(self.__MODE1, oldmode | 0x80)

  def setPWM(self, channel, on, off):
    "Sets a single PWM channel"
    self.write(self.__LED0_ON_L+4*channel, on & 0xFF)
    self.write(self.__LED0_ON_H+4*channel, on >> 8)
    self.write(self.__LED0_OFF_L+4*channel, off & 0xFF)
    self.write(self.__LED0_OFF_H+4*channel, off >> 8)
    if (self.debug):
      print("channel: %d  LED_ON: %d LED_OFF: %d" % (channel,on,off))
	  
  def setServoPulse(self, channel, pulse):
    "Sets the Servo Pulse,The PWM frequency must be 50HZ"
    pulse = pulse*4096/20000        #PWM frequency is 50HZ,the period is 20000us
    self.setPWM(channel, 0, int(pulse))

  def motorAngle(self, motor1,motor2):

    self.setServoPulse(1, self.x_centre + self.x_offset + (motor1 / 100.0) * self.x_maxtilt)
    self.setServoPulse(0, self.y_centre + self.y_offset + (motor2 / 100.0) * self.y_maxtilt)
    self.previous_motor1_angle = motor1
    self.previous_motor2_angle = motor2
  
  def calibrate(self):

    self.setPWMFreq(50)

    self.x_offset = 0
    self.y_offset = 20
    self.x_maxtilt = 30
    self.y_maxtilt = 30
    self.x_centre = 1915
    self.y_centre = 1915

    self.motorAngle(0,0)
    
    self.previous_motor1_angle = 0
    self.previous_motor2_angle = 0
  
  def smoothMotorAngle(self, motor1_target, motor2_target):

    motor1_start = self.previous_motor1_angle
    motor2_start = self.previous_motor2_angle
    steps = abs(int(motor1_target - motor1_start)+10)
    print(steps)

    for step in range(steps + 1):
        motor1_step = motor1_start + (motor1_target - motor1_start) * step / steps
        motor2_step = motor2_start + (motor2_target - motor2_start) * step / steps
        self.motorAngle(motor1_step, motor2_step)
    
  def readMotorPulse(self, channel):
    """Reads the pulse width for the specified channel."""
    # Read the ON and OFF registers
    on_l = self.read(self.__LED0_ON_L + 4 * channel)
    on_h = self.read(self.__LED0_ON_H + 4 * channel)
    off_l = self.read(self.__LED0_OFF_L + 4 * channel)
    off_h = self.read(self.__LED0_OFF_H + 4 * channel)

    # Combine high and low bytes to get the full ON and OFF counts
    on_count = (on_h << 8) | on_l
    off_count = (off_h << 8) | off_l

    # The pulse width is the difference between ON and OFF counts
    pulse_width = off_count - on_count

    if self.debug:
        print(f"Channel {channel}: ON={on_count}, OFF={off_count}, Pulse Width={pulse_width}")

    return pulse_width

  def run(self):
    pwm = PCA9685(0x40, debug=False)
    pwm.setPWMFreq(50)
    pwm.motorAngle(0,0)
    time.sleep(2)
    pwm.motorAngle(100,100)
    time.sleep(2)

    while True:
      
      for i in range(-100, 101, 1):  
        pwm.setServoPulse(0, 1915 + (i / 100.0) * 85)  
  
      for i in range(-100, 101, 1):  
        pwm.setServoPulse(1, 1915 + (i / 100.0) * 85)  
        time.sleep(0.02)

      for i in range(100, -101, -1):  
        pwm.setServoPulse(0, 1915 + (i / 100.0) * 85)   
      for i in range(100, -101, -1):  
        pwm.setServoPulse(1, 1915 + (i / 100.0) * 85) 
        time.sleep(0.02)   

# hello = PCA9685()
# while True:
#    hello.run()
# hello.calibrate() 