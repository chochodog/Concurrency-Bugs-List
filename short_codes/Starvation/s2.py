import threading
import time

mutex = threading.Lock()

def thread_function(name):
    while True:
        if name == "Thread-1":
            mutex.acquire()
            print(f"{name} has the resource")
            time.sleep(0.1)
        elif mutex.acquire(blocking=False):
            print(f"{name} got the resource")
            mutex.release()
        else:
            print(f"{name} is starving")
        time.sleep(0.05)

thread1 = threading.Thread(target=thread_function, args=("Thread-1",))
thread2 = threading.Thread(target=thread_function, args=("Thread-2",))
thread1.start()
thread2.start()
