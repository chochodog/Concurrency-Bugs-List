import threading
import time

sem = threading.Semaphore(1)

def task():
    print("Trying to acquire semaphore...")
    sem.acquire()
    print("Semaphore acquired")
    time.sleep(2)
    print("Trying to acquire semaphore again...")  
    sem.acquire()
    print("Semaphore acquired again (never reached)")
    sem.release()
    sem.release()

t = threading.Thread(target=task)
t.start()
t.join()
