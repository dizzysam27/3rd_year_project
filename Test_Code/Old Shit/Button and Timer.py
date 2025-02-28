import RPi.GPIO as GPIO
import time
import serial

BUTTON_PIN_1 = 23
BUTTON_PIN_2 = 18
BUTTON_PIN_3 = 21
# BUTTON_PIN_4 = 12
GPIO.setmode(GPIO.BCM)

ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

GPIO.setup(BUTTON_PIN_1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_PIN_2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_PIN_3,GPIO.IN,pull_up_down=GPIO.PUD_UP)
# GPIO.setup(BUTTON_PIN_4,GPIO.IN,pull_up_down=GPIO.PUD_UP)

# GPIO.wait_for_edge(BUTTON_PIN,GPIO.BOTH)
# print("Button has been pressed")

def button1_released_callback(channel):
    print("Button1 has just been released")
    ser.write(b'Clear')
def button2_released_callback(channel):
    print("Button2 has just been released")
    ser.write(b'Start')



def button3_released_callback(channel):
    print("Button3 has just been released")
    # Initialize UART on /dev/serial0


    ser.write(b'Stop')





def button4_released_callback(channel):
    print("Button4 has just been released")
    ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

    try:
        ser.write(b'Start')
        time.sleep(1)
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            print("Received:", data)
    except KeyboardInterrupt:
        ser.close()



GPIO.add_event_detect(BUTTON_PIN_1,GPIO.RISING,callback=button1_released_callback,bouncetime=50)
GPIO.add_event_detect(BUTTON_PIN_2,GPIO.FALLING,callback=button2_released_callback,bouncetime=500)
GPIO.add_event_detect(BUTTON_PIN_3,GPIO.FALLING,callback=button3_released_callback,bouncetime=500)
# GPIO.add_event_detect(BUTTON_PIN_4,GPIO.RISING,callback=button4_released_callback,bouncetime=50)

try:
    while True:
        time.sleep(0.01)
except KeyboardInterrupt:
    GPIO.cleanup()
