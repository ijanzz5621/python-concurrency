import threading

semaphore = threading.Semaphore()

# example 1
semaphore.acquire() # decrement the counter
# access the shared resource
semaphore.release() # increment the counter

# example 2
semaphore.acquire() # decrements the counter
# .... up to 3 threads can access the shared resource at a time
semaphore.release() # increment the counter

# example 3
num_permits = 3
semaphore = threading.BoundedSemaphore(num_permits)
semaphore.acquire() # decrement the counter
# ... up to 3 threads can access the shared resource at a time
semaphore.release()