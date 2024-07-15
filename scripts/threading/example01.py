import threading

def do_some_work(val):
    print("doing some work in thread")
    print("echo: {}".format(val))
    return

val = "text"
t = threading.Thread(target=do_some_work, args=(val,))
t.start() # start execution
t.join() # waiting for the thread to complete

