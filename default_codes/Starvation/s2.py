import threading
import time
import random
import queue
import logging
from dataclasses import dataclass, field
from typing import List, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
)

@dataclass(order=True)
class ResourceRequest:
    priority: int
    request_time: float
    thread_id: int = field(compare=False)
    wait_time: float = field(default=0.0, compare=False)

class SharedResource:
    def __init__(self, name: str):
        self.name = name
        self.in_use = False
        self.lock = threading.Lock()
    
    def use_resource(self, thread_id: int, duration: float):
        """Simulate using the resource for a specific duration"""
        with self.lock:
            self.in_use = True
            
        logging.info(f"Thread {thread_id} is using {self.name} for {duration:.2f} seconds")
        time.sleep(duration)
        
        with self.lock:
            self.in_use = False
            
        logging.info(f"Thread {thread_id} released {self.name}")

class PriorityBasedResourceManager:
    def __init__(self, resource: SharedResource, starvation_threshold: float = 10.0):
        self.resource = resource
        self.request_queue = queue.PriorityQueue()  # (priority, request_time, request)
        self.lock = threading.Lock()
        self.cv = threading.Condition(self.lock)
        self.active = True
        self.starvation_threshold = starvation_threshold
        self.wait_times: Dict[int, List[float]] = {}
        
        # Start the resource allocation thread
        self.allocation_thread = threading.Thread(target=self._allocate_resources)
        self.allocation_thread.daemon = True
        self.allocation_thread.start()
    
    def request_resource(self, thread_id: int, priority: int, use_duration: float) -> float:
        """Request access to the resource and return the wait time"""
        request_time = time.time()
        
        with self.lock:
            # Create a request
            request = ResourceRequest(priority, request_time, thread_id)
            
            # Add request to queue - lower number = higher priority
            self.request_queue.put(request)
            
            logging.info(f"Thread {thread_id} (priority {priority}) requested resource")
            
            # Wait until it's our turn
            while self.active:
                # Check if we're at the front of the queue
                if not self.request_queue.empty():
                    top_request = self.request_queue.queue[0]
                    if top_request.thread_id == thread_id:
                        break
                
                # Check for starvation
                current_wait = time.time() - request_time
                if current_wait > self.starvation_threshold:
                    logging.warning(f"Thread {thread_id} is experiencing starvation! Waiting for {current_wait:.2f} seconds")
                
                # Wait for a notification
                self.cv.wait(timeout=1.0)
        
        # We've been granted access
        wait_time = time.time() - request_time
        
        # Record wait time
        if thread_id not in self.wait_times:
            self.wait_times[thread_id] = []
        self.wait_times[thread_id].append(wait_time)
        
        logging.info(f"Thread {thread_id} granted access after waiting {wait_time:.2f} seconds")
        
        # Use the resource
        self.resource.use_resource(thread_id, use_duration)
        
        return wait_time
    
    def _allocate_resources(self):
        """Thread that handles resource allocation"""
        while self.active:
            with self.lock:
                if not self.request_queue.empty() and not self.resource.in_use:
                    try:
                        # Get the highest priority request
                        request = self.request_queue.get_nowait()
                        logging.info(f"Allocating resource to thread {request.thread_id} with priority {request.priority}")
                        # Notify all waiters
                        self.cv.notify_all()
                    except queue.Empty:
                        logging.error("Queue was unexpectedly empty.")
            
            time.sleep(0.1)  # Small sleep to prevent CPU hogging
    
    def stop(self):
        """Stop the resource manager"""
        self.active = False
        self.allocation_thread.join(timeout=1.0)
    
    def get_statistics(self) -> Dict:
        """Get statistics about wait times"""
        stats = {}
        for thread_id, times in self.wait_times.items():
            stats[thread_id] = {
                "min_wait": min(times),
                "max_wait": max(times),
                "avg_wait": sum(times) / len(times),
                "total_waits": len(times)
            }
        return stats

def worker_thread(thread_id: int, priority: int, manager: PriorityBasedResourceManager, iterations: int):
    """Worker thread that repeatedly requests the resource"""
    for i in range(iterations):
        # Random duration for using the resource
        use_duration = random.uniform(0.1, 0.5)
        
        # Request and use the resource
        wait_time = manager.request_resource(thread_id, priority, use_duration)
        
        # Random think time between requests
        think_time = random.uniform(0.1, 1.0)
        time.sleep(think_time)

def run_simulation(num_threads: int = 5, runtime_seconds: int = 30):
    """Run the starvation simulation"""
    # Create shared resource
    resource = SharedResource("Database Connection")
    
    # Create resource manager
    manager = PriorityBasedResourceManager(resource, starvation_threshold=5.0)
    
    # Create threads with different priorities
    # High-priority threads (1-2), medium priority (3-4), low priority (5)
    threads = []
    priorities = {}
    
    for i in range(num_threads):
        # Assign priorities to demonstrate starvation
        # Lower number means higher priority
        if i < 2:
            priority = 1  # High priority
        elif i < 4:
            priority = 3  # Medium priority
        else:
            priority = 5  # Low priority
        
        priorities[i] = priority
        thread = threading.Thread(
            target=worker_thread,
            args=(i, priority, manager, 100)  # High iteration count
        )
        thread.daemon = True
        threads.append(thread)
    
    # Start all threads
    logging.info(f"Starting simulation with {num_threads} threads")
    logging.info(f"Thread priorities: {priorities}")
    start_time = time.time()
    
    for thread in threads:
        thread.start()
    
    # Run for specified time
    try:
        while time.time() - start_time < runtime_seconds:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Simulation interrupted")
    
    # Cleanup and report
    manager.stop()
    
    # Wait for threads to finish (they should be daemon threads)
    for thread in threads:
        thread.join(timeout=0.5)
    
    # Display statistics
    stats = manager.get_statistics()
    logging.info("\n----- Simulation Results -----")
    for thread_id, thread_stats in stats.items():
        priority_level = "High" if priorities[thread_id] == 1 else "Medium" if priorities[thread_id] == 3 else "Low"
        logging.info(f"Thread {thread_id} (Priority: {priority_level}):")
        logging.info(f"  Min wait: {thread_stats['min_wait']:.2f}s")
        logging.info(f"  Max wait: {thread_stats['max_wait']:.2f}s")
        logging.info(f"  Avg wait: {thread_stats['avg_wait']:.2f}s")
        logging.info(f"  Resource accesses: {thread_stats['total_waits']}")

if __name__ == "__main__":
    run_simulation(num_threads=5, runtime_seconds=30)



# 코드 수정했음 (답변 제작 이후, traceBack 로그 출력되어 import 수정)