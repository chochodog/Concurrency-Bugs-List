import threading
import time
from queue import Queue
import statistics

class SharedResource:
    def __init__(self):
        self.lock = threading.Lock()
        self.value = 0
        self.wait_times = Queue()

    def access(self, thread_id, work_time):
        """Access the shared resource"""
        start_time = time.time()
        
        # Try to acquire the lock
        print(f"Thread {thread_id}: Attempting to acquire lock...")
        self.lock.acquire()
        
        # Calculate waiting time after lock acquisition
        wait_time = time.time() - start_time
        self.wait_times.put(wait_time)
        
        try:
            print(f"Thread {thread_id}: Lock acquired! Wait time: {wait_time:.4f}s")
            
            # Simulate using the resource
            self.value += 1
            time.sleep(work_time)
            
            print(f"Thread {thread_id}: Work completed (work time: {work_time:.4f}s)")
        finally:
            # Release the lock
            self.lock.release()
            print(f"Thread {thread_id}: Lock released")

def run_simulation():
    # Create shared resource
    resource = SharedResource()
    threads = []
    
    # Create one thread that will hold the lock for a long time
    blocker = threading.Thread(
        target=resource.access, 
        args=("Blocker", 2.0)  # Holds lock for 2 seconds
    )
    threads.append(blocker)
    
    # Create regular worker threads
    for i in range(5):
        t = threading.Thread(
            target=resource.access, 
            args=(f"Worker-{i}", 0.1)  # Works for 0.1 seconds
        )
        threads.append(t)
    
    # Start all threads
    print("=== Starting simulation ===")
    start_time = time.time()
    
    for t in threads:
        t.start()
    
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    total_time = time.time() - start_time
    print(f"\n=== Simulation complete (total time: {total_time:.4f}s) ===")
    
    # Print waiting time statistics
    wait_times = []
    while not resource.wait_times.empty():
        wait_times.append(resource.wait_times.get())
    
    print(f"Average wait time: {statistics.mean(wait_times):.4f}s")
    print(f"Maximum wait time: {max(wait_times):.4f}s")
    print(f"Minimum wait time: {min(wait_times):.4f}s")

if __name__ == "__main__":
    run_simulation()