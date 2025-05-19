import multiprocessing
import time
import random

class SharedTask:
    def __init__(self):
        self.progress = 0
        self.last_modified_by = None
        self.required_progress = 100

def worker(name, task, lock, delay):
    attempts = 0
    while attempts < 20:  # Limit attempts to demonstrate livelock
        with lock:
            current_progress = task.progress
            last_modifier = task.last_modified_by
            
            # If the other worker just modified it, undo their work thinking it's wrong
            if last_modifier and last_modifier != name:
                print(f"{name}: Saw {last_modifier}'s changes. Progress at {task.progress}. Undoing...")
                task.progress = max(0, task.progress - 15)
                task.last_modified_by = name
            else:
                # Try to make progress
                print(f"{name}: Attempting to make progress... Currently at {task.progress}")
                task.progress = min(task.required_progress, task.progress + 10)
                task.last_modified_by = name
            
            # Check if task is complete
            if task.progress >= task.required_progress:
                print(f"{name}: Task completed!")
                return
                
        attempts += 1
        # Random delay to simulate varying work times
        time.sleep(delay + random.uniform(0, 0.2))
        
    print(f"{name}: Giving up after {attempts} attempts. Progress stuck at {task.progress}")

if __name__ == "__main__":
    # Create shared objects using Manager
    manager = multiprocessing.Manager()
    task = manager.Namespace()
    task.progress = 0
    task.last_modified_by = None
    task.required_progress = 100
    
    lock = multiprocessing.Lock()
    
    # Create processes with different delays
    process_1 = multiprocessing.Process(
        target=worker,
        args=("Worker-1", task, lock, 0.3)
    )
    process_2 = multiprocessing.Process(
        target=worker,
        args=("Worker-2", task, lock, 0.4)
    )
    
    print("Starting workers...")
    start_time = time.time()
    
    # Start processes
    process_1.start()
    process_2.start()
    
    # Wait for processes to complete
    process_1.join()
    process_2.join()
    
    # Report final status
    elapsed_time = time.time() - start_time
    print(f"\nSimulation completed in {elapsed_time:.2f} seconds")
    print(f"Final progress: {task.progress}")
    print(f"Last modified by: {task.last_modified_by}")
    
    if task.progress < task.required_progress:
        print("Livelock detected: Workers kept undoing each other's progress!")
    else:
        print("Task completed successfully!")