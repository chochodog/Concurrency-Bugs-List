import threading
import time
import random

class BankAccount:
    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance
    
    def withdraw(self, amount):
        # Read the current balance
        current_balance = self.balance
        
        # Simulate some processing time, making race conditions more likely
        time.sleep(0.001)
        
        # Update the balance if sufficient funds
        if current_balance >= amount:
            # Write the new balance
            self.balance = current_balance - amount
            return True
        return False
    
    def deposit(self, amount):
        # Read the current balance
        current_balance = self.balance
        
        # Simulate some processing time
        time.sleep(0.001)
        
        # Write the new balance
        self.balance = current_balance + amount
        return True


def transfer(from_account, to_account, amount):
    """Transfer money between accounts without synchronization"""
    # This function is not atomic - it consists of two separate operations
    # that can be interrupted by other threads between them
    if from_account.withdraw(amount):
        to_account.deposit(amount)
        return True
    return False


def run_transfers(from_account, to_account, num_transfers):
    """Perform multiple transfers between accounts"""
    for _ in range(num_transfers):
        amount = random.randint(10, 50)
        transfer(from_account, to_account, amount)


def main():
    # Setup: Create two bank accounts with initial balances
    account_a = BankAccount("A", 1000)
    account_b = BankAccount("B", 1000)
    
    # Print initial state
    print(f"Initial balances:")
    print(f"Account A: ${account_a.balance}")
    print(f"Account B: ${account_b.balance}")
    print(f"Total money in system: ${account_a.balance + account_b.balance}")
    print("\nStarting transfers...\n")
    
    # Create multiple threads to simulate concurrent transfers
    threads = []
    
    # Half of the threads transfer from A to B
    for i in range(5):
        thread = threading.Thread(target=run_transfers, args=(account_a, account_b, 20))
        threads.append(thread)
    
    # Half of the threads transfer from B to A
    for i in range(5):
        thread = threading.Thread(target=run_transfers, args=(account_b, account_a, 20))
        threads.append(thread)
    
    # Start all threads
    for thread in threads:
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Print final state
    print("All transfers completed!")
    print(f"Final balances:")
    print(f"Account A: ${account_a.balance}")
    print(f"Account B: ${account_b.balance}")
    print(f"Total money in system: ${account_a.balance + account_b.balance}")
    
    # Check for system invariant violation
    initial_total = 2000  # $1000 in each account
    final_total = account_a.balance + account_b.balance
    
    if final_total != initial_total:
        print(f"\n⚠️ ATOMIC VIOLATION DETECTED! ⚠️")
        print(f"Money was created or destroyed in the system.")
        print(f"Expected total: ${initial_total}")
        print(f"Actual total: ${final_total}")
        print(f"Discrepancy: ${final_total - initial_total}")
    else:
        print("\nSystem integrity maintained (this is rare without synchronization!)")
    
    # Check for negative balances
    if account_a.balance < 0 or account_b.balance < 0:
        print(f"\n⚠️ NEGATIVE BALANCE DETECTED! ⚠️")
        if account_a.balance < 0:
            print(f"Account A has gone negative: ${account_a.balance}")
        if account_b.balance < 0:
            print(f"Account B has gone negative: ${account_b.balance}")


if __name__ == "__main__":
    main()
