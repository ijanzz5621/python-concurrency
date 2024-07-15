# using Lock

import threading

lock = threading.Lock()

lock.acquire()
try:
    # accessing resources...
    print("test")
finally:
    lock.release()
    
# OR
# using with
# acquire and release automatically
with lock:
    print("test")    

