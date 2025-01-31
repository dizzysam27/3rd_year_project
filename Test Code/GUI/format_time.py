import time

def format_time(elapsed_time):
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    milliseconds = int((elapsed_time % 1) * 1000)
    return f"{minutes:02}:{seconds:02}:{milliseconds:03}"

start_time = time.time()

while True:

    elapsed_time = time.time() - start_time
    formatted_time = format_time(elapsed_time)
   
    print(f"Elapsed time: {formatted_time}",flush=True)