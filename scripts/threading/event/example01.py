import threading

event = threading.Event()

# a client thread can wait for the flag to be set
event.wait()

# a server thread can set or reset it
event.set() # set the flag to true
event.clear() # reset the flag to false

