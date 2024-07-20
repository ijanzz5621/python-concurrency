import multiprocessing

def do_some_work(val):
    print("doing some work in thread")
    print("echo: {}".format(val))
    return

if __name__ == '__main__':
    val = "text"
    t = multiprocessing.Process(target=do_some_work, args=(val,))
    t.start()
    t.join()
    
    