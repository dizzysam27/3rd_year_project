from LCD_Module import LCD1602
import time
import threading

lcd = LCD1602(16,2)

# Define the Welcome Message
message_line1 = "Welcome"
message_line2 = "Group 12"

flag=0

# Function to update the messages
def update_messages(new_message_line1, new_message_line2):

    global message_line1, message_line2, flag
    flag=1
    message_line1 = new_message_line1
    message_line2 = new_message_line2
    print(message_line1)
    print(message_line2)

# Pad the messages for smooth scrolling if the message is longer than 16 letters
def pad_messages():
    padded_line1 = message_line1 + " " * 16
    padded_line2 = message_line2 + " " * 16
    return padded_line1, padded_line2

# Find the maximum scroll length for both messages
def get_max_scroll_length(padded_line1, padded_line2):
    return max(len(padded_line1), len(padded_line2)) - 15

# Function to scroll line 1
def scroll_line1(padded_line1, max_scroll):
    global flag
    flag=0
    if len(message_line1)<17:
        lcd.setCursor(0, 0)
        lcd.printout(message_line1)
    else:
        for i in range(max_scroll):
            if flag ==0:
                segment_line1 = padded_line1[i:i + 16] if i < len(padded_line1) else " " * 16
                lcd.setCursor(0, 0)
                lcd.printout(segment_line1)
                time.sleep(0.2)
            else:
                lcd.clear()
                break

# Function to scroll line 2
def scroll_line2(padded_line2, max_scroll):
    global flag
    flag=0
    if len(message_line2)<17:
        lcd.setCursor(0, 1)
        lcd.printout(message_line2)
        
    else:
        for i in range(max_scroll):
            if flag == 0:
                segment_line2 = padded_line2[i:i + 16] if i < len(padded_line2) else " " * 16
                lcd.setCursor(0, 1)
                lcd.printout(segment_line2)
                time.sleep(0.2)
            else:
                lcd.clear()
                break
            
# Function to run both threads - one for the top line and one for the bottom
def run_threads(padded_line1, padded_line2, max_scroll):
    # Start scrolling line 1 and line 2 simultaneously
    thread1 = threading.Thread(target=scroll_line1, args=(padded_line1, max_scroll))
    thread2 = threading.Thread(target=scroll_line2, args=(padded_line2, max_scroll))

    thread1.start()
    thread2.start()
    time.sleep(2)

    # Sync both threads
    thread1.join()
    thread2.join()

# Function to run the scrolling task in the background to allow for other processes to continue
def display_thread_function():
    global message_line1, message_line2
    while True:
        # Pad the messages for smooth scrolling
        padded_line1, padded_line2 = pad_messages()
        max_scroll = get_max_scroll_length(padded_line1, padded_line2)
        run_threads(padded_line1, padded_line2, max_scroll)
        
def main():
    display_thread = threading.Thread(target=display_thread_function, daemon=True)
    display_thread.start()
    while True:
        lcd = LCD1602(16,2)
        time.sleep(5)
        update_messages("New York is the Worst", "San Jose is the best")
        time.sleep(7)
        update_messages("Choose","1      2      3")
        time.sleep(5)
        update_messages("Hello","Everyone")
      
if __name__ == "__main__":
    lcd.setRGB(255,255,255)
    main()
