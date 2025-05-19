import multiprocessing
import time
import random

def increment_counter(counter, process_id, iterations, delay_range):
    """Increment a shared counter with random delays."""
    print(f"Process {process_id} starting")
    
    for i in range(iterations):
        time.sleep(random.uniform(0.01, delay_range))
        
        current_value = counter.value
        time.sleep(random.uniform(0.01, 0.05))
        
        counter.value = current_value + 1
        
        print(f"Process {process_id}: iteration {i+1}, set counter to {counter.value}")
    
    print(f"Process {process_id} finished")

if __name__ == "__main__":
    shared_counter = multiprocessing.Value('i', 0)
    
    iterations = 10
    
    p1 = multiprocessing.Process(target=increment_counter, 
                                args=(shared_counter, 1, iterations, 0.03))
    p2 = multiprocessing.Process(target=increment_counter, 
                                args=(shared_counter, 2, iterations, 0.02))
    
    print(f"Initial counter value: {shared_counter.value}")
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
    
    print(f"Final counter value: {shared_counter.value}")
    print(f"Expected value if no order violations: {iterations * 2}")
    print(f"Missing increments due to order violations: {iterations * 2 - shared_counter.value}")
