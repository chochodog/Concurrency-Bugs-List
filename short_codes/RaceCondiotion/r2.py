import multiprocessing
import os

def update_counter_in_file(filename, iterations):
    for _ in range(iterations):
        # Read current value
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                try:
                    count = int(f.read().strip())
                except ValueError:
                    count = 0
        else:
            count = 0
            
        # Write incremented value
        with open(filename, 'w') as f:
            f.write(str(count + 1))

if __name__ == "__main__":
    counter_file = "counter.txt"
    # Initialize or reset the counter file
    with open(counter_file, 'w') as f:
        f.write("0")
    
    iterations = 50
    
    # Create two processes
    p1 = multiprocessing.Process(target=update_counter_in_file, args=(counter_file, iterations))
    p2 = multiprocessing.Process(target=update_counter_in_file, args=(counter_file, iterations))
    
    # Start processes
    p1.start()
    p2.start()
    
    # Wait for completion
    p1.join()
    p2.join()
    
    # Check final value
    with open(counter_file, 'r') as f:
        final_count = int(f.read().strip())
    
    print(f"Final count: {final_count}")
    print(f"Expected count: {iterations * 2}")
    print(f"Lost updates: {iterations * 2 - final_count}")
    
    # Clean up
    os.remove(counter_file)