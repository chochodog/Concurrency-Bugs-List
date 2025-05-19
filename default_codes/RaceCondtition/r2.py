import threading
import time
from typing import List

class Counter:
    def __init__(self):
        self.count = 0
    
    def increment(self):
        # Deliberately make the race condition more likely by breaking
        # the increment operation into multiple steps
        current = self.count  # Read
        time.sleep(0.0001)   # Simulate some processing time
        self.count = current + 1  # Write

def worker(counter: Counter, iterations: int):
    """Worker function that increments the counter multiple times"""
    for _ in range(iterations):
        counter.increment()

def run_experiment(num_threads: int, iterations_per_thread: int) -> int:
    """
    Run the experiment with specified number of threads and iterations.
    Returns the final counter value.
    """
    counter = Counter()
    threads: List[threading.Thread] = []
    
    # Create and start threads
    for _ in range(num_threads):
        thread = threading.Thread(
            target=worker,
            args=(counter, iterations_per_thread)
        )
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    return counter.count

def main():
    num_threads = 4
    iterations_per_thread = 500
    expected_count = num_threads * iterations_per_thread
    
    print(f"Running experiment with:")
    print(f"- Number of threads: {num_threads}")
    print(f"- Iterations per thread: {iterations_per_thread}")
    print(f"- Expected final count: {expected_count}")
    print("\nExecuting...\n")
    
    # Run multiple trials to demonstrate the inconsistency
    for trial in range(3):
        final_count = run_experiment(num_threads, iterations_per_thread)
        missing_counts = expected_count - final_count
        print(f"Trial {trial + 1}:")
        print(f"- Final count: {final_count}")
        print(f"- Missing increments: {missing_counts}")
        print(f"- Error percentage: {(missing_counts / expected_count) * 100:.2f}%\n")

if __name__ == "__main__":
    main()