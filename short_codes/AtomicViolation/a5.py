import threading
import random
import time

class Counter:
    def __init__(self):
        self.value = 0
    
    def increment(self):
        current_value = self.value
        if random.random() < 0.0001:
            time.sleep(0.01)
        self.value = current_value + 1

def worker(counter):
    for _ in range(100):
        counter.increment()


counter = Counter()


threads = [threading.Thread(target=worker, args=(counter,)) for _ in range(10)]


for thread in threads:
    thread.start()

# 모든 스레드가 종료될 때까지 대기
for thread in threads:
    thread.join()

print(f'Final counter value: {counter.value}')
