from machine import Pin, UART, ADC # type: ignore
import time
import _thread

# Define UART0 conditions
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

# 7 Segment Display Values
thousands = [Pin(20, Pin.OUT, value=0),
             Pin(28, Pin.OUT, value=0),
             Pin(22, Pin.OUT, value=0),
             Pin(21, Pin.OUT, value=0)
             ]
hundreds = [Pin(16, Pin.OUT, value=0),
            Pin(19, Pin.OUT, value=0),
            Pin(18, Pin.OUT, value=0),
            Pin(17, Pin.OUT, value=0)
            ]
tens = [Pin(12, Pin.OUT, value=0),
        Pin(15, Pin.OUT, value=0),
        Pin(14, Pin.OUT, value=0),
        Pin(13, Pin.OUT, value=0)
        ]
units = [Pin(8, Pin.OUT, value=0),
         Pin(11, Pin.OUT, value=0),
         Pin(10, Pin.OUT, value=0),
         Pin(9, Pin.OUT, value=0)
         ]

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
    return int((200 * raw) / 65535)

# Update Values
def counterUpdate(data):
    valueLength = len(data)
    for x in range(valueLength):
        binaryValue = format(int(data[x]), '#006b')
        print(binaryValue)
        for y in range(4):
            match x:
                case 0: thousands[y].value = int(binaryValue[y+2])
                case 1: hundreds[y].value = int(binaryValue[y+2])
                case 2: tens[y].value = int(binaryValue[y+2])
                case 3: units[y].value = int(binaryValue[y+2])
                case _: print("Counter Update Error")

# Main loop
while True:
    # Read Joystick Values
    xValue = readJoy(xAxis)
    yValue = readJoy(yAxis)
    buttonValue = int ( not JoyButton.value() )

    # Combine to a single string/integer
    dataTx = str(buttonValue + xValue*10 + yValue*10000)

    # Rx/Tx
    dataRx = UARTrx(uart0)
    if dataRx:
        UARTtx(str(dataTx), uart0)
    
    # Update Counter Value
    counterUpdate(dataRx)

    time.sleep(0.1)