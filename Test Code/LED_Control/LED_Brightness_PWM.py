from gpiozero import PWMLED
from time import sleep
import numpy as np

led = PWMLED(18, frequency = 2000)

# led.value = 0.1
# sleep(5)
# led.value = 0.5
# sleep(5)
# led.value = 1
# sleep(5)
# led.value=0
while True:
    for x in range(1,179,1):
        y = np.sin(np.deg2rad(x))
        led.value = y   
        sleep(0.01)
