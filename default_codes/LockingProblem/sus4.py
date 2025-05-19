import threading
import time
import random
import queue
from datetime import datetime

class SharedResource:
    def __init__(self, name, use_duration_range=(1, 3)):
        self.name = name
        self.lock = threading.Lock()
        self.use_duration_range = use_duration_range
        self.wait_times = queue.Queue()
        self.contention_events = 0
        
    def use_resource(self, thread_id):
        """Attempt to use the shared resource with lock acquisition"""
        print(f"[{time.time():.3f}] Thread-{thread_id}: Attempting to acquire lock for {self.name}")
        
        start_wait = time.time()
        acquired = self.lock.acquire()
        wait_time = time.time() - start_wait
        
        self.wait_times.put(wait_time)
        
        if wait_time > 0.1:  # Consider it contention if wait time exceeds 100ms
            self.contention_events += 1
            
        print(f"[{time.time():.3f}] Thread-{thread_id}: Lock acquired for {self.name} (waited {wait_time:.3f}s)")
        
        # Simulate using the resource for some time
        use_duration = random.uniform(*self.use_duration_range)
        print(f"[{time.time():.3f}] Thread-{thread_id}: Using {self.name} for {use_duration:.3f}s")
        time.sleep(use_duration)
        
        # Release the lock
        self.lock.release()
        print(f"[{time.time():.3f}] Thread-{thread_id}: Released lock for {self.name}")
        
        return wait_time, use_duration

def worker(resource, thread_id, access_count=3):
    """Worker function that tries to access the resource multiple times"""
    total_wait_time = 0
    total_use_time = 0
    
    for i in range(access_count):
        # Random delay before trying to access the resource
        delay = random.uniform(0.1, 1.0)
        time.sleep(delay)
        
        # Try to use the resource
        wait_time, use_time = resource.use_resource(thread_id)
        total_wait_time += wait_time
        total_use_time += use_time
    
    print(f"[{time.time():.3f}] Thread-{thread_id}: Completed all tasks. " 
          f"Total wait time: {total_wait_time:.3f}s, Total use time: {total_use_time:.3f}s")

def simulate_resource_contention(num_threads=5, resource_use_range=(1, 3), access_count=3):
    """Run a simulation of multiple threads competing for a shared resource"""
    print(f"Starting shared resource contention simulation with {num_threads} threads")
    print(f"Each thread will attempt to access the resource {access_count} times")
    print(f"Resource use time range: {resource_use_range[0]}-{resource_use_range[1]} seconds")
    print("-" * 70)
    
    # Create shared resource
    printer = SharedResource("Printer", resource_use_range)
    
    # Create and start threads
    threads = []
    start_time = time.time()
    
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(printer, i, access_count))
        threads.append(t)
        t.start()
    
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    end_time = time.time()
    total_simulation_time = end_time - start_time
    
    # Calculate statistics
    wait_times = list(printer.wait_times.queue)
    avg_wait_time = sum(wait_times) / len(wait_times) if wait_times else 0
    max_wait_time = max(wait_times) if wait_times else 0
    
    # Print summary
    print("\n" + "=" * 70)
    print("SIMULATION RESULTS")
    print("=" * 70)
    print(f"Total simulation time: {total_simulation_time:.3f} seconds")
    print(f"Number of resource accesses: {num_threads * access_count}")
    print(f"Average wait time: {avg_wait_time:.3f} seconds")
    print(f"Maximum wait time: {max_wait_time:.3f} seconds")
    print(f"Contention events (waits > 100ms): {printer.contention_events}")
    print(f"Contention percentage: {(printer.contention_events / (num_threads * access_count)) * 100:.1f}%")
    
    # Demonstrate potential deadlock scenario
    print("\nPOTENTIAL DEADLOCK SCENARIO:")
    print("In this simulation, we used a single resource with proper lock release.")
    print("However, if multiple resources were involved with nested locks, deadlocks could occur.")
    print("For example, if Thread A holds Resource 1's lock and waits for Resource 2,")
    print("while Thread B holds Resource 2's lock and waits for Resource 1 - this creates a deadlock.")

if __name__ == "__main__":
    # Run simulation with default parameters
    simulate_resource_contention(num_threads=8, resource_use_range=(1, 3), access_count=3)
    
    # Uncomment to run a high-contention scenario
    # print("\n\nRunning high-contention scenario (more threads, longer use times)...")
    # simulate_resource_contention(num_threads=15, resource_use_range=(2, 5), access_count=2)