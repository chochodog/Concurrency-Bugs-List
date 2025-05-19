import threading
import multiprocessing
import time
import random

total_sum = 0

def increment_sum_thread():
    global total_sum
    current = total_sum
    time.sleep(random.random() * 0.01)
    total_sum = current + 1

def increment_sum_process(counter):
    with open("process_counter.txt", "r") as f:
        value = int(f.read().strip())
    
    time.sleep(random.random() * 0.01)

    with open("process_counter.txt", "w") as f:
        f.write(str(value + 1))

if __name__ == "__main__":
    with open("process_counter.txt", "w") as f:
        f.write("0")
    
    threads = []
    for _ in range(10):
        t = threading.Thread(target=increment_sum_thread)
        threads.append(t)
    
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"Thread counter should be 10, actual value: {total_sum}")
    
    processes = []
    for i in range(5):
        p = multiprocessing.Process(target=increment_sum_process, args=(i,))
        processes.append(p)
    
    for p in processes:
        p.start()

    for p in processes:
        p.join()

    with open("process_counter.txt", "r") as f:
        process_counter = int(f.read().strip())
    
    print(f"Process counter should be 5, actual value: {process_counter}")
    import os
    os.remove("process_counter.txt")
