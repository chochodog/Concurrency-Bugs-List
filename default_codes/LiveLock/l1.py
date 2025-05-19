import threading
import time
import random

class Resource:
    def __init__(self, name):
        self.name = name
        self.lock = threading.Lock()
        self.owner = None
    
    def acquire(self, owner):
        """Try to acquire the resource for the given owner"""
        result = self.lock.acquire(blocking=False)
        if result:
            self.owner = owner
            print(f"{time.time():.2f}: {owner} acquired {self.name}")
        return result
    
    def release(self):
        """Release the resource"""
        previous_owner = self.owner
        self.owner = None
        self.lock.release()
        print(f"{time.time():.2f}: {previous_owner} released {self.name}")


class Worker(threading.Thread):
    def __init__(self, name, first_resource, second_resource):
        super().__init__(name=name)
        self.first_resource = first_resource
        self.second_resource = second_resource
        self.active = True
        self.last_progress = time.time()
    
    def run(self):
        while self.active:
            # Try to acquire the first resource
            if self.first_resource.acquire(self.name):
                try:
                    # Simulate some work
                    time.sleep(0.1)
                    
                    # Try to acquire the second resource
                    print(f"{time.time():.2f}: {self.name} is trying to acquire {self.second_resource.name}")
                    attempt_start = time.time()
                    
                    # Keep trying to get the second resource with backoff
                    while self.active:
                        if self.second_resource.acquire(self.name):
                            try:
                                # Update progress time since we successfully got both resources
                                self.last_progress = time.time()
                                print(f"{time.time():.2f}: {self.name} has both resources!")
                                
                                # Do some work with both resources
                                time.sleep(0.2)
                                
                            finally:
                                # Release the second resource
                                self.second_resource.release()
                            break
                        
                        # Wait a bit before retrying (this makes livelock more likely)
                        wait_time = random.uniform(0.1, 0.3)
                        time.sleep(wait_time)
                        
                        # Check if we've been trying too long (for demonstration)
                        if time.time() - attempt_start > 1.0:
                            print(f"{time.time():.2f}: {self.name} giving up on {self.second_resource.name} temporarily")
                            break
                    
                finally:
                    # Always release the first resource
                    self.first_resource.release()
            
            # Small delay before next attempt
            time.sleep(random.uniform(0.05, 0.1))


def detect_livelock(workers, timeout=5):
    """Monitor worker threads to detect livelock condition"""
    start_time = time.time()
    
    while all(worker.is_alive() for worker in workers):
        # Check if any worker has made progress recently
        current_time = time.time()
        stuck_workers = [w for w in workers if current_time - w.last_progress > timeout]
        
        if len(stuck_workers) == len(workers) and current_time - start_time > timeout:
            print(f"\n{'='*60}")
            print(f"LIVELOCK DETECTED! All workers are stuck waiting for resources.")
            print(f"Elapsed time: {current_time - start_time:.2f} seconds")
            print(f"{'='*60}\n")
            
            # Terminate the workers
            for worker in workers:
                worker.active = False
            break
        
        time.sleep(1)


def main():
    # Create the resources
    resource_x = Resource("Resource X")
    resource_y = Resource("Resource Y")
    
    # Create the workers (threads)
    thread_a = Worker("Thread A", resource_x, resource_y)
    thread_b = Worker("Thread B", resource_y, resource_x)
    
    # Start the workers
    print("Starting workers...")
    thread_a.start()
    thread_b.start()
    
    # Start the livelock detection in a separate thread
    detector = threading.Thread(target=detect_livelock, args=([thread_a, thread_b],))
    detector.start()
    
    # Wait for all threads to complete
    detector.join()
    thread_a.join(timeout=1)
    thread_b.join(timeout=1)
    
    print("Simulation completed.")


if __name__ == "__main__":
    main()
