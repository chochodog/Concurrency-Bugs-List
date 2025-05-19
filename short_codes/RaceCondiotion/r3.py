import threading
import time

class BankAccount:
    def __init__(self):
        self.balance = 0
    
    def deposit(self, amount):
        temp = self.balance
        time.sleep(0.1)
        self.balance = temp + amount
    
    def withdraw(self, amount):
        temp = self.balance
        time.sleep(0.1)
        self.balance = temp - amount

def run_transactions():
    account = BankAccount()
    
    def deposit_task():
        for _ in range(5):
            account.deposit(100)
    
    def withdraw_task():
        for _ in range(5):
            account.withdraw(50)
    
    threads = []
    for _ in range(2):
        t1 = threading.Thread(target=deposit_task)
        t2 = threading.Thread(target=withdraw_task)
        threads.extend([t1, t2])
        t1.start()
        t2.start()
    
    for t in threads:
        t.join()
    
    print(f"최종 잔액: {account.balance}")
    print(f"기대 잔액: {2*5*100 - 2*5*50}")

if __name__ == "__main__":
    run_transactions()
