import threading
import time
import random

class BankAccount:
    def __init__(self, account_id, balance=1000):
        self.account_id = account_id
        self.balance = balance
        self.lock = threading.Lock()
        self.access_times = []
    
    def transfer(self, amount, destination, customer_id, processing_time):
        """Transfer money to another account with simulated processing time"""
        print(f"Customer {customer_id}: Requesting transfer of ${amount}...")
        start_time = time.time()
        
        # Try to lock the account
        self.lock.acquire()
        wait_time = time.time() - start_time
        self.access_times.append(wait_time)
        
        try:
            print(f"Customer {customer_id}: Processing transfer (wait: {wait_time:.2f}s)")
            
            # Simulate processing time (verification, authorization, etc.)
            time.sleep(processing_time)
            
            # Execute transfer
            if self.balance >= amount:
                self.balance -= amount
                destination.balance += amount
                print(f"Customer {customer_id}: Transferred ${amount} to account {destination.account_id}")
            else:
                print(f"Customer {customer_id}: Insufficient funds")
        finally:
            print(f"Customer {customer_id}: Transaction completed")
            self.lock.release()
        
        return wait_time

# Run simulation
if __name__ == "__main__":
    # Create accounts
    account1 = BankAccount("A001")
    account2 = BankAccount("A002")
    
    # Create threads for different customers
    threads = []
    
    # One customer doing a complex transaction (takes long time)
    complex_txn = threading.Thread(
        target=account1.transfer,
        args=(200, account2, "VIP-Customer", 3.0)  # Complex transaction takes 3 seconds
    )
    threads.append(complex_txn)
    
    # Regular customers doing simple transactions
    for i in range(5):
        t = threading.Thread(
            target=account1.transfer,
            args=(50, account2, f"Regular-{i}", 0.2)  # Regular transactions take 0.2 seconds
        )
        threads.append(t)
    
    # Start all threads with slight delay for predictable ordering
    print("=== Starting Bank Simulation ===")
    for t in threads:
        t.start()
        time.sleep(0.05)
    
    # Wait for all transactions to complete
    for t in threads:
        t.join()
    
    # Print statistics
    print("\n=== Transaction Statistics ===")
    print(f"Average wait time: {sum(account1.access_times)/len(account1.access_times):.2f}s")
    print(f"Maximum wait time: {max(account1.access_times):.2f}s")
    print(f"Final balance in account {account1.account_id}: ${account1.balance}")
    print(f"Final balance in account {account2.account_id}: ${account2.balance}")