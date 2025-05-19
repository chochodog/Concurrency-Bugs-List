import threading
import time
from datetime import datetime

shared_data = None
lock = threading.Lock()

def log(message):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

def writer():
    global shared_data
    log("[Writer] Writing data...")
    time.sleep(1)
    with lock:
        shared_data = "Important Data"
    log("[Writer] Finished writing.")

def reader():
    time.sleep(1)
    with lock:
        if shared_data is None:
            log("[Reader] WARNING: Attempted to read before data was written!")
        else:
            log(f"[Reader] Read data: {shared_data}")

def extra_writer():
    global shared_data
    time.sleep(3)
    log("[Extra Writer] Modifying data...")
    with lock:
        shared_data = "Updated Data"
    log("[Extra Writer] Finished modifying data.")

def extra_reader():
    time.sleep(3)
    with lock:
        if shared_data is None:
            log("[Extra Reader] WARNING: Attempted to read before data was written!")
        else:
            log(f"[Extra Reader] Read updated data: {shared_data}")

thread1 = threading.Thread(target=writer)
thread2 = threading.Thread(target=reader)
thread3 = threading.Thread(target=extra_writer)
thread4 = threading.Thread(target=extra_reader)

thread1.start()
thread2.start()
thread3.start()
thread4.start()

thread1.join()
thread2.join()
thread3.join()
thread4.join()

log("[Main] Program finished.")
