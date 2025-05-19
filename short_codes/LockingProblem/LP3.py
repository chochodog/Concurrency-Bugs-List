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
        
        print(f"Thread {thread_id}: Attempting to acquire lock...")
        self.lock.acquire()
        
        wait_time = time.time() - start_time
        self.wait_times.put(wait_time)
        
        try:
            print(f"Thread {thread_id}: Lock acquired! Wait time: {wait_time:.4f}s")
            
            self.value += 1
            time.sleep(work_time)
            
            print(f"Thread {thread_id}: Work completed (work time: {work_time:.4f}s)")
        finally:
            self.lock.release()
            print(f"Thread {thread_id}: Lock released")

def run_simulation():
    resource = SharedResource()
    threads = []
    
    blocker = threading.Thread(
        target=resource.access, 
        args=("Blocker", 2.0)
    )
    threads.append(blocker)
    
    for i in range(5):
        t = threading.Thread(
            target=resource.access, 
            args=(f"Worker-{i}", 0.1)
        )
        threads.append(t)

    print("=== Starting simulation ===")
    start_time = time.time()
    
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()
    
    total_time = time.time() - start_time
    print(f"\n=== Simulation complete (total time: {total_time:.4f}s) ===")
    
    wait_times = []
    while not resource.wait_times.empty():
        wait_times.append(resource.wait_times.get())
    
    print(f"Average wait time: {statistics.mean(wait_times):.4f}s")
    print(f"Maximum wait time: {max(wait_times):.4f}s")
    print(f"Minimum wait time: {min(wait_times):.4f}s")

if __name__ == "__main__":
    run_simulation()
