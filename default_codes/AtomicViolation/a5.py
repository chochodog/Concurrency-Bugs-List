import threading
import random
import time
from typing import List, Optional

class ThreadSafeCounter:
    def __init__(self, error_rate: float = 0.0001):
        self.value = 0
        self.error_rate = error_rate
        self._lock = threading.Lock()
        self.total_operations = 0
        self.failed_operations = 0
        
    def increment(self, thread_id: Optional[int] = None) -> None:
        """Increment counter with intentional race condition possibility."""
        self.total_operations += 1
        current_value = self.value
        
        if random.random() < self.error_rate:
            time.sleep(0.01)
            self.failed_operations += 1
            
        self.value = current_value + 1
        
    def increment_safe(self, thread_id: Optional[int] = None) -> None:
        """Thread-safe increment operation."""
        with self._lock:
            self.increment(thread_id)
            
    def get_stats(self) -> dict:
        """Return counter statistics."""
        return {
            'value': self.value,
            'total_operations': self.total_operations,
            'failed_operations': self.failed_operations,
            'failure_rate': self.failed_operations / self.total_operations if self.total_operations > 0 else 0
        }

class ThreadManager:
    def __init__(self, counter: ThreadSafeCounter, num_threads: int = 10, iterations: int = 100):
        self.counter = counter
        self.num_threads = num_threads
        self.iterations = iterations
        self.threads: List[threading.Thread] = []
        
    def worker(self, thread_id: int, use_safe_method: bool = False) -> None:
        """Worker function for thread execution."""
        for _ in range(self.iterations):
            if use_safe_method:
                self.counter.increment_safe(thread_id)
            else:
                self.counter.increment(thread_id)
                
    def run_demo(self, use_safe_method: bool = False) -> dict:
        """Execute thread demonstration."""
        self.threads = [
            threading.Thread(
                target=self.worker,
                args=(i, use_safe_method)
            ) for i in range(self.num_threads)
        ]
        
        start_time = time.time()
        
        for thread in self.threads:
            thread.start()
            
        for thread in self.threads:
            thread.join()
            
        execution_time = time.time() - start_time
        stats = self.counter.get_stats()
        stats['execution_time'] = execution_time
        
        return stats

# Example usage:
if __name__ == "__main__":
    # Unsafe version
    counter = ThreadSafeCounter(error_rate=0.1)
    manager = ThreadManager(counter)
    unsafe_results = manager.run_demo(use_safe_method=False)
    print("\nUnsafe Version Results:", unsafe_results)
    
    # Safe version
    counter = ThreadSafeCounter(error_rate=0.1)
    manager = ThreadManager(counter)
    safe_results = manager.run_demo(use_safe_method=True)
    print("\nSafe Version Results:", safe_results)