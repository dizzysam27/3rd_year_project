from machine import Pin, UART, ADC # type: ignore
import time

# Define UART Protocol
uart0 = UART(0,
             baudrate=9600,
             bits=8,
             parity=None,
             stop=1,
             tx=Pin(0),
             rx=Pin(1))

# Define Joystick axes and button
xAxis = ADC(27)
yAxis = ADC(26)
JoyButton = Pin(2, Pin.IN, Pin.PULL_UP) # Pulled up signal
led = Pin(25, Pin.OUT)



# Define 7 Segment Display Pins
def segmentDefinition(pinouts):
    return [Pin(pinouts[0], Pin.OUT, value=0),
            Pin(pinouts[1], Pin.OUT, value=0),
            Pin(pinouts[2], Pin.OUT, value=0),
            Pin(pinouts[3], Pin.OUT, value=0)]

thousands = segmentDefinition([20, 28, 22, 21])
hundreds = segmentDefinition([16, 19, 18, 17])
tens = segmentDefinition([12, 15, 14, 13])
units = segmentDefinition([8, 11, 10, 9])
# Further displays can be added easily

# UART Transmit Function
def UARTtx(dataIn, uartName):
    try:
        uartName.write(dataIn)
        print("Sent: ", dataIn)
    except Exception as e:
        print("Error sending data: ", e)

# UART Recieve Function
def UARTrx(uartName):
    try:
        if uartName.any():
            dataOut = uartName.readline().decode("utf-8")
            print("Recieved: ",dataOut)
            return dataOut
    except Exception as e:
        print("Error reading data: ", e)
    return None

# Read Joystick Value Function
def readJoy(axis):
    raw = axis.read_u16()
    return int(((200 * raw)/ 65535)/2)

# Update Values
def counterUpdate(data):
#     data = '1234'
    valueLength = len(data)
    for x in range(valueLength):
        binaryValue = f'{int(data[x]):04b}'
        for y in range(4):
                if x==0: thousands[y].value(int(binaryValue[3-y]))
                elif x==1: hundreds[y].value(int(binaryValue[3-y]))
                elif x==2: tens[y].value(int(binaryValue[3-y]))
                elif x==3: units[y].value(int(binaryValue[3-y]))

# Main loop
while True:
    xValue = readJoy(xAxis)
    print(xValue)
    if xValue <10:
        xValue = ("0"+str(xValue))
    yValue = readJoy(yAxis)
    if yValue <10:
        yValue = ("0"+str(yValue))
    
        
    counterUpdate(str(xValue)+str(yValue))
    
    
    # Update Counter Value
#     counterUpdate(dataRx)

    time.sleep(0.1)