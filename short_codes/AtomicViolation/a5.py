import threading
import random
import time

class Counter:
    def __init__(self):
        self.value = 0
    
    def increment(self):
        # 락을 사용하지 않고, 대부분 정상적으로 동작하되, 10% 확률로 문제가 발생하게 설정
        current_value = self.value
        if random.random() < 0.0001:
            # 10% 확률로 다른 스레드가 값을 변경할 시간을 줌
            time.sleep(0.01)  # 의도적으로 동기화 문제 발생
        self.value = current_value + 1

def worker(counter):
    for _ in range(100):
        counter.increment()

# 카운터 객체 생성
counter = Counter()

# 스레드 리스트 생성
threads = [threading.Thread(target=worker, args=(counter,)) for _ in range(10)]

# 스레드 시작
for thread in threads:
    thread.start()

# 모든 스레드가 종료될 때까지 대기
for thread in threads:
    thread.join()

print(f'Final counter value: {counter.value}')
