import threading
import time
from queue import Queue

shared_resource = 0
lock = threading.Lock()

def long_task():
    global shared_resource
    print(f"Long task started by {threading.current_thread().name}")
    with lock:
        for _ in range(50_000_000):
            shared_resource += 1
        print(f"Long task finished by {threading.current_thread().name}")

def short_task():
    global shared_resource
    print(f"Short task started by {threading.current_thread().name}")
    with lock:
        for _ in range(1_000_000):
            shared_resource += 1
        print(f"Short task finished by {threading.current_thread().name}")

def run_tasks():
    threads = []
    
    for _ in range(2):
        thread = threading.Thread(target=long_task)
        threads.append(thread)
    
    for _ in range(5):
        thread = threading.Thread(target=short_task)
        threads.append(thread)

    start_time = time.time()

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()

    total_time = end_time - start_time
    print(f"Total execution time: {total_time:.5f} seconds")

if __name__ == "__main__":
    run_tasks()
    print(f"Final value of shared_resource: {shared_resource}")
