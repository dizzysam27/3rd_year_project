from machine import Pin, UART, ADC  # type: ignore
import time

# UART Protocol
uart0 = UART(0, baudrate=9600, bits=8, parity=None, stop=1, tx=Pin(0), rx=Pin(1))

# Joystick and Button
xAxis = ADC(27)
yAxis = ADC(26)
JoyButton = Pin(2, Pin.IN, Pin.PULL_UP)

# UART Transmit Function
def UARTtx(dataIn, uartName):
    try:
        uartName.write(dataIn + "\n")
        print("Sent:", dataIn)
    except Exception as e:
        print("Error sending data:", e)

# Read Joystick Value
def readJoy(axis):
    raw = axis.read_u16()
    return int(((200 * raw)) / 65535)

# Main loop
while True:
    
    joyx = readJoy(xAxis)
    joyy = readJoy(yAxis)
    # Read Joystick and Button
    print(joyx)
    print(joyy)
    
    #deadzone
    #sensitivity = 80
    
    if (joyx < 100):
        xValue = joyx
    elif (joyx > 100):
        xValue = joyx
    
    
    if (joyy < 100):
        yValue = joyy 
    elif (joyy > 100):
        yValue = joyy 
    
    level_compensationx = 21
    level_compensationy = 50
        
    xValue = int(xValue) - level_compensationx
    yValue - int(yValue) - level_compensationy
    
    buttonValue = int(not JoyButton.value())

    # Pack Data
    dataTx = f"{xValue},{yValue},{buttonValue}"

    # Transmit Data
    UARTtx(dataTx, uart0)
    time.sleep(0.1)
