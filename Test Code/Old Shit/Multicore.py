import _thread

def hello():
    print("Core 1: Hello World")

_thread.start_new_thread(hello, ())

print("Core 0: Hello World")