import multiprocessing
from multiprocessing import Manager
import time
import random

def add_to_list(shared_list, process_name, items_to_add):
    """
    Process that adds items to a shared list with random delays
    to demonstrate order violations.
    """
    print(f"{process_name} starting")
    
    for item in items_to_add:
        current_length = len(shared_list)

        time.sleep(random.uniform(0.01, 0.05))
        
        shared_list.append(item)
        
        print(f"{process_name} added {item} at position {current_length}, list is now {list(shared_list)}")
    
    print(f"{process_name} finished")

if __name__ == "__main__":
    manager = Manager()
    shared_list = manager.list()
    
    process_a_items = ["A1", "A2", "A3"]
    process_b_items = ["B1", "B2", "B3"]
    
    expected_result = process_a_items + process_b_items
    
    process_a = multiprocessing.Process(
        target=add_to_list, 
        args=(shared_list, "Process A", process_a_items)
    )
    
    process_b = multiprocessing.Process(
        target=add_to_list, 
        args=(shared_list, "Process B", process_b_items)
    )
    
    print("Starting processes...")
    process_a.start()
    process_b.start()
    
    process_a.join()
    process_b.join()
    
    print("\nFinal list:", list(shared_list))
    print("Items added:", len(shared_list))
    print("Expected order if A finished before B:", expected_result)
    
    a_positions = [i for i, item in enumerate(shared_list) if item.startswith("A")]
    b_positions = [i for i, item in enumerate(shared_list) if item.startswith("B")]
    
    print("\nPositions of A items:", a_positions)
    print("Positions of B items:", b_positions)
    
    if any(b_pos < a_pos for a_pos in a_positions for b_pos in b_positions):
        print("\nOrder violation detected! Items were interleaved due to concurrent execution.")
        print("The final order depends on the random timing between processes.")
