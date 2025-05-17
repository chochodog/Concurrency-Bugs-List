import threading
import time
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

class DatabaseRecord:
    def __init__(self, record_id):
        self.record_id = record_id
        self.lock = threading.Lock()
        self.value = 0

class TransactionManager:
    def __init__(self, records_count=10):
        self.records = [DatabaseRecord(i) for i in range(records_count)]
        self.deadlock_counter = 0

class Transaction(threading.Thread):
    def __init__(self, transaction_id, manager):
        threading.Thread.__init__(self)
        self.transaction_id = transaction_id
        self.manager = manager
    
    def run(self):
        # Increase deadlock probability by selecting more records and randomizing lock order
        num_records = random.randint(2, 5)
        selected_records = random.sample(self.manager.records, num_records)
        
        # Shuffle records to increase deadlock chance
        random.shuffle(selected_records)

        logging.info(f"Transaction {self.transaction_id} attempting to lock records: {[r.record_id for r in selected_records]}")

        try:
            # Acquire locks with high potential for circular wait
            for record in selected_records:
                # Introduce longer hold times and higher contention
                if not record.lock.acquire(timeout=0.5):
                    logging.info(f"Transaction {self.transaction_id} couldn't acquire lock")
                    return
                
                time.sleep(random.uniform(0.1, 0.3))  # Increased processing time
                record.value += random.randint(1, 5)
                logging.info(f"Transaction {self.transaction_id} modified record {record.record_id}")
        
        except Exception as e:
            logging.error(f"Transaction {self.transaction_id} error: {e}")
        
        finally:
            # Release locks
            for record in reversed(selected_records):
                record.lock.release()
        
        logging.info(f"Transaction {self.transaction_id} completed")

def simulate_database_transactions(num_transactions=50):
    manager = TransactionManager()
    transactions = []

    for i in range(num_transactions):
        transaction = Transaction(i, manager)
        transactions.append(transaction)
        transaction.start()

    for transaction in transactions:
        transaction.join()

    logging.info("\nFinal Record States:")
    for record in manager.records:
        logging.info(f"Record {record.record_id}: Value = {record.value}")

if __name__ == "__main__":
    simulate_database_transactions()