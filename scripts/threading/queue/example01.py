# put(): puts an item into the queue
# get(): Removes an item from the queue and returns it
# task_done(): Marks an item that was gotten from the queue as completed/processed
# join(): Blocks until all the items in the queue have been processed

import time
from threading import Thread
from queue import Queue

def make_an_item_available(item: int):
    return item

def producer(queue: Queue):
    for i in range(100):
        item = make_an_item_available(i+1)
        queue.put(item)
        
    print("All item has been queued...")
        
def consumer(queue: Queue):
    # while True:   # Infinite loop. 
    while not queue.empty(): # Stop once the queue is empty
        # item: int = queue.get()
        item: int = queue.get_nowait()
        # do something with the item
        # time.sleep(2)
        print("item is {}".format(item))
        queue.task_done() # mark the item as done
        
queue = Queue()
t1 = Thread(target=producer, args=(queue,))
t2 = Thread(target=consumer, args=(queue,))
t1.start()
# t1.join()
t2.start()