import threading
import time
import random
from enum import Enum
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('DatabaseLivelock')

class LockStatus(Enum):
    UNLOCKED = 0
    LOCKED = 1

class DataItem:
    def __init__(self, item_id):
        self.item_id = item_id
        self.lock_status = LockStatus.UNLOCKED
        self.lock_holder = None
        self.lock = threading.Lock()
    
    def try_lock(self, transaction_id):
        with self.lock:
            if self.lock_status == LockStatus.UNLOCKED:
                self.lock_status = LockStatus.LOCKED
                self.lock_holder = transaction_id
                logger.info(f"Transaction {transaction_id} acquired lock on data item {self.item_id}")
                return True
            else:
                logger.info(f"Transaction {transaction_id} failed to lock data item {self.item_id} (held by Transaction {self.lock_holder})")
                return False
    
    def unlock(self, transaction_id):
        with self.lock:
            if self.lock_status == LockStatus.LOCKED and self.lock_holder == transaction_id:
                self.lock_status = LockStatus.UNLOCKED
                prev_holder = self.lock_holder
                self.lock_holder = None
                logger.info(f"Transaction {prev_holder} released lock on data item {self.item_id}")
                return True
            return False

class Transaction(threading.Thread):
    def __init__(self, transaction_id, data_items, lock_sequence, database, max_attempts=20):
        super().__init__(name=f"Transaction-{transaction_id}")
        self.transaction_id = transaction_id
        self.data_items = data_items
        self.lock_sequence = lock_sequence
        self.database = database
        self.locked_items = []
        self.completed = False
        self.deadlocked = False
        self.attempts = 0
        self.max_attempts = max_attempts
        self.last_progress_time = time.time()
    
    def run(self):
        logger.info(f"Transaction {self.transaction_id} started")
        
        while not self.completed and self.attempts < self.max_attempts:
            self.attempts += 1
            
            # Try to acquire all locks in sequence
            all_locked = True
            for item_id in self.lock_sequence:
                if item_id not in self.locked_items:
                    if self.database.data_items[item_id].try_lock(self.transaction_id):
                        self.locked_items.append(item_id)
                        self.last_progress_time = time.time()
                    else:
                        all_locked = False
                        # Simulate livelock condition by adding random backoff
                        backoff = random.uniform(0.1, 0.5)
                        time.sleep(backoff)
                        break
            
            if all_locked:
                # Process data (simulated)
                logger.info(f"Transaction {self.transaction_id} processing data...")
                time.sleep(0.2)  # Simulate data processing
                
                # Release all locks
                for item_id in self.locked_items:
                    self.database.data_items[item_id].unlock(self.transaction_id)
                self.locked_items = []
                self.completed = True
                logger.info(f"Transaction {self.transaction_id} completed successfully")
            else:
                # Check for livelock condition (no progress for a while)
                if time.time() - self.last_progress_time > 5:  # 5 seconds without progress
                    self.deadlocked = True
                    logger.warning(f"Transaction {self.transaction_id} might be in a livelock situation")
        
        # If not completed, release any acquired locks
        if not self.completed:
            for item_id in self.locked_items:
                self.database.data_items[item_id].unlock(self.transaction_id)
            logger.warning(f"Transaction {self.transaction_id} failed to complete after {self.attempts} attempts")

class Database:
    def __init__(self, num_items=5):
        self.data_items = {i: DataItem(i) for i in range(num_items)}
        self.transactions = []
        self.livelock_detector = None
    
    def add_transaction(self, transaction_id, lock_sequence):
        transaction = Transaction(transaction_id, self.data_items, lock_sequence, self)
        self.transactions.append(transaction)
        return transaction
    
    def start_transactions(self):
        for transaction in self.transactions:
            transaction.start()
    
    def check_livelock(self):
        """Monitor transactions for livelock conditions"""
        livelock_threshold = 10  # Time in seconds to consider as livelock
        check_interval = 1
        
        while any(t.is_alive() for t in self.transactions):
            time.sleep(check_interval)
            
            active_transactions = [t for t in self.transactions if t.is_alive()]
            if not active_transactions:
                break
                
            # Check if all active transactions have been stuck for a while
            current_time = time.time()
            potential_livelock = all(
                current_time - t.last_progress_time > livelock_threshold 
                for t in active_transactions
            )
            
            if potential_livelock and len(active_transactions) > 1:
                logger.critical(f"LIVELOCK DETECTED: {len(active_transactions)} transactions are stuck!")
                logger.critical("Transactions involved in livelock:")
                for t in active_transactions:
                    logger.critical(f"  - Transaction {t.transaction_id} holding: {t.locked_items}, waiting for: "
                               f"{[i for i in t.lock_sequence if i not in t.locked_items]}")
                
                # Livelock resolution strategy - kill random transaction
                victim = random.choice(active_transactions)
                logger.warning(f"Resolving livelock by aborting Transaction {victim.transaction_id}")
                victim.deadlocked = True
                
                # Force release of locks
                for item_id in victim.locked_items:
                    self.data_items[item_id].unlock(victim.transaction_id)
                victim.locked_items = []

    def start_livelock_detector(self):
        """Start livelock detection in a separate thread"""
        self.livelock_detector = threading.Thread(target=self.check_livelock, name="LivelockDetector")
        self.livelock_detector.daemon = True
        self.livelock_detector.start()

def run_simulation(create_livelock=True):
    """
    Run the database transaction simulation
    
    Args:
        create_livelock: If True, creates a lock pattern likely to cause livelock
    """
    db = Database(num_items=5)
    
    if create_livelock:
        # Create transactions with overlapping lock patterns to encourage livelock
        # Each transaction tries to lock resources in a circular pattern
        db.add_transaction(1, [0, 1, 2])
        db.add_transaction(2, [1, 2, 3])
        db.add_transaction(3, [2, 3, 4])
        db.add_transaction(4, [3, 4, 0])
        db.add_transaction(5, [4, 0, 1])
    else:
        # Create transactions with non-overlapping lock patterns
        db.add_transaction(1, [0, 1])
        db.add_transaction(2, [2, 3])
        db.add_transaction(3, [4])
    
    # Start livelock detection
    db.start_livelock_detector()
    
    # Start all transactions
    db.start_transactions()
    
    # Wait for all transactions to complete
    for transaction in db.transactions:
        transaction.join()
    
    # Check results
    completed = sum(1 for t in db.transactions if t.completed)
    deadlocked = sum(1 for t in db.transactions if t.deadlocked)
    
    logger.info(f"\nSimulation complete:")
    logger.info(f"Total transactions: {len(db.transactions)}")
    logger.info(f"Completed successfully: {completed}")
    logger.info(f"Potentially livelocked: {deadlocked}")
    
    if db.livelock_detector:
        db.livelock_detector.join(timeout=1)

if __name__ == "__main__":
    logger.info("Starting Database Livelock Simulation...")
    logger.info("This simulation demonstrates how transactions can get into a livelock situation")
    logger.info("=================================================================")
    
    run_simulation(create_livelock=True)