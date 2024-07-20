import multiprocessing

print("outer: this will print when run and when imported")

def func():
    print("func: this will print only when run")
    return

if __name__=='__main__':
    print("main: this will print only when run")
    p = multiprocessing.Process(target=func)
    p.start()
    p.join()