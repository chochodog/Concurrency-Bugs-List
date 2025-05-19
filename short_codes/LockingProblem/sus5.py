import threading
import time
from queue import Queue

# 공유 리소스와 락
shared_resource = 0
lock = threading.Lock()

# 긴 작업: 공유 리소스에 많은 계산 작업 수행
def long_task():
    global shared_resource
    print(f"Long task started by {threading.current_thread().name}")
    with lock:
        for _ in range(50_000_000):  # 긴 연산 수행 (연산량 증가)
            shared_resource += 1
        print(f"Long task finished by {threading.current_thread().name}")

# 짧은 작업: 공유 리소스에 간단한 작업 수행
def short_task():
    global shared_resource
    print(f"Short task started by {threading.current_thread().name}")
    with lock:
        for _ in range(1_000_000):  # 반복 횟수 증가
            shared_resource += 1
        print(f"Short task finished by {threading.current_thread().name}")

# 스레드 관리
def run_tasks():
    threads = []
    
    # 긴 작업 스레드 생성
    for _ in range(2):  # 긴 작업 2개
        thread = threading.Thread(target=long_task)
        threads.append(thread)
    
    # 짧은 작업 스레드 생성
    for _ in range(5):  # 짧은 작업 5개
        thread = threading.Thread(target=short_task)
        threads.append(thread)

    # 시작 시간 기록
    start_time = time.time()

    # 스레드를 순차적으로 시작
    for thread in threads:
        thread.start()

    # 모든 스레드가 종료되길 기다림
    for thread in threads:
        thread.join()

    # 종료 시간 기록
    end_time = time.time()

    # 총 소요 시간 계산 및 출력
    total_time = end_time - start_time
    print(f"Total execution time: {total_time:.5f} seconds")

if __name__ == "__main__":
    run_tasks()
    print(f"Final value of shared_resource: {shared_resource}")
