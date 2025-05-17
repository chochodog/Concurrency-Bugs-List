import threading
import time
import random

class InventorySystem:
    def __init__(self):
        # Initialize inventory with product IDs and quantities
        self.inventory = {
            "product_a": 1000,
            "product_b": 500,
            "product_c": 750
        }
        
    def update_inventory(self, product_id, change_amount):
        """
        Update the inventory for a specific product.
        This function simulates a non-atomic operation by breaking it down into steps.
        """
        # Step 1: Read the current inventory level
        current_quantity = self.inventory[product_id]
        
        # Simulate some processing time that might occur in a real system
        # This increases the chance of an atomic violation occurring
        time.sleep(random.uniform(0.001, 0.005))
        
        # Step 2: Calculate the new inventory level
        new_quantity = current_quantity + change_amount
        
        # More simulated processing time
        time.sleep(random.uniform(0.001, 0.005))
        
        # Step 3: Write the new value back to the inventory
        self.inventory[product_id] = new_quantity
        
        # Log the operation for demonstration purposes
        print(f"Thread {threading.current_thread().name}: Updated {product_id} by {change_amount}, " 
              f"Expected: {current_quantity + change_amount}, Set to: {new_quantity}")


def simulate_user_activity(inventory_system, product_id, num_operations):
    """Simulate a user performing multiple inventory updates."""
    for _ in range(num_operations):
        # Randomly decide whether to increase or decrease inventory
        change_amount = random.choice([-5, -3, -1, 1, 3, 5])
        inventory_system.update_inventory(product_id, change_amount)


def run_simulation(num_users, operations_per_user):
    """Run the main simulation with multiple concurrent users."""
    inventory = InventorySystem()
    target_product = "product_a"
    
    # Record the initial state
    initial_quantity = inventory.inventory[target_product]
    print(f"\nSIMULATION START: {target_product} initial quantity: {initial_quantity}")
    
    # Calculate expected final quantity for verification
    expected_changes = []
    
    # Create and start multiple threads to simulate concurrent users
    threads = []
    for i in range(num_users):
        thread = threading.Thread(
            target=simulate_user_activity,
            args=(inventory, target_product, operations_per_user),
            name=f"User-{i+1}"
        )
        threads.append(thread)
    
    # Start all threads
    for thread in threads:
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Record the final state
    final_quantity = inventory.inventory[target_product]
    
    # Get the actual change from log entries
    total_reported_changes = 0
    for line in logged_changes:
        if "Updated product_a by" in line:
            change = int(line.split("by ")[1].split(",")[0])
            total_reported_changes += change
    
    # Print results and analysis
    print(f"\nSIMULATION COMPLETE")
    print(f"Initial quantity: {initial_quantity}")
    print(f"Final quantity: {final_quantity}")
    print(f"Total reported changes: {total_reported_changes}")
    print(f"Expected final quantity: {initial_quantity + total_reported_changes}")
    
    if final_quantity != (initial_quantity + total_reported_changes):
        print("\n*** ATOMIC VIOLATION DETECTED ***")
        print(f"Discrepancy: {final_quantity - (initial_quantity + total_reported_changes)}")
        print("This demonstrates how concurrent updates without proper synchronization")
        print("can lead to incorrect inventory levels and data inconsistency.")
    else:
        print("\nNo atomic violation detected in this run. Try running again with more threads.")


# Capture log output for analysis
logged_changes = []
original_print = print

def log_print(*args, **kwargs):
    message = " ".join(map(str, args))
    logged_changes.append(message)
    original_print(*args, **kwargs)

print = log_print

# Run the simulation
if __name__ == "__main__":
    print("===== INVENTORY ATOMIC VIOLATION SIMULATION =====")
    print("This simulation demonstrates how concurrent inventory updates")
    print("without proper synchronization can lead to data inconsistencies.\n")
    
    # Configure simulation parameters
    NUM_USERS = 10          # Number of concurrent users
    OPERATIONS_PER_USER = 5  # Operations each user performs
    
    # Execute simulation
    run_simulation(NUM_USERS, OPERATIONS_PER_USER)
    
    print("\n===== EXPLANATION =====")
    print("The issue demonstrated is known as a 'race condition' or 'atomic violation':")
    print("1. Multiple threads read the current inventory value before any updates are written")
    print("2. Each thread calculates a new value based on the outdated read")
    print("3. When threads write their calculated values, they overwrite each other's changes")
    print("4. The final inventory count doesn't reflect all the updates that occurred")
    print("\nIn real systems, this leads to inventory discrepancies, potentially causing:")
    print("- Overselling products that aren't actually available")
    print("- Lost sales due to products appearing out of stock when they aren't")
    print("- Financial reconciliation issues")
    print("\nSolution: Use synchronization mechanisms like locks or database transactions")
    print("to ensure inventory updates are atomic operations.")