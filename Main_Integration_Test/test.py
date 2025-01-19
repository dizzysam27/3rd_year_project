from Timer import TIMER
import time
def timer_update(value):
    print(value)

timer = TIMER(update_callback=timer_update)

timer.start_timer()
time.sleep(60)  # Simulate a 5-second run
timer.stop_timer()
