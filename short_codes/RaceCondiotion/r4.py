import threading
import multiprocessing
import time
import random

# Shared data for threads
total_sum = 0

# Function for thread operation
def increment_sum_thread():
    global total_sum
    # Read
    current = total_sum
    # Small random delay to increase chance of race condition
    time.sleep(random.random() * 0.01)
    # Write back - potentially overwriting other increments
    total_sum = current + 1

# Function for process operation
def increment_sum_process(counter):
    # Read
    with open("process_counter.txt", "r") as f:
        value = int(f.read().strip())
    
    # Small random delay to increase chance of race condition
    time.sleep(random.random() * 0.01)
    
    # Write back - potentially overwriting other increments
    with open("process_counter.txt", "w") as f:
        f.write(str(value + 1))

if __name__ == "__main__":
    # Initialize process counter file
    with open("process_counter.txt", "w") as f:
        f.write("0")
    
    # Thread example
    threads = []
    for _ in range(10):
        t = threading.Thread(target=increment_sum_thread)
        threads.append(t)
    
    # Start all threads
    for t in threads:
        t.start()
    
    # Wait for threads to complete
    for t in threads:
        t.join()
    
    print(f"Thread counter should be 10, actual value: {total_sum}")
    
    # Process example
    processes = []
    for i in range(5):
        p = multiprocessing.Process(target=increment_sum_process, args=(i,))
        processes.append(p)
    
    # Start all processes
    for p in processes:
        p.start()
    
    # Wait for processes to complete
    for p in processes:
        p.join()
    
    # Read final process counter
    with open("process_counter.txt", "r") as f:
        process_counter = int(f.read().strip())
    
    print(f"Process counter should be 5, actual value: {process_counter}")
    
    # Clean up
    import os
    os.remove("process_counter.txt")