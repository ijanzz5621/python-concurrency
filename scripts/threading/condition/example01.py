import threading

cond = threading.Condition()

def an_item_is_available():
    return False

def get_an_available_item():
    return True

def make_an_item_available():
    return True

# consumer
# consume one item
cond.acquire()
while not an_item_is_available():
    cond.wait()
    
get_an_available_item()
cond.release()

# producer
# Produce one item
cond.acquire()
make_an_item_available()
cond.notify()
cond.release()