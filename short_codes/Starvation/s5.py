import threading
import time

# 공유 자원 접근을 조절하기 위한 Lock
lock = threading.Lock()

# 각 스레드의 자원 접근 횟수를 기록
access_count = {
    'priority_thread': 0,
    'starved_thread': 0
}

# 우선 순위가 높은 스레드
def priority_thread():
    while access_count['priority_thread'] < 100:
        lock.acquire()
        try:
            # 자원을 사용하고 있음을 알림
            access_count['priority_thread'] += 1
            print(f"Priority thread accessed resource {access_count['priority_thread']} times")
            time.sleep(0.01)  # 짧은 작업을 시뮬레이션
        finally:
            lock.release()
        time.sleep(0.005)  # 다음 접근까지 짧은 대기

# 자원에 거의 접근하지 못하는 스레드
def starved_thread():
    while access_count['starved_thread'] < 100:
        if lock.acquire(timeout=0.002):  # timeout을 짧게 설정하여 거의 접근 못하게 함
            try:
                # 자원을 사용하고 있음을 알림
                access_count['starved_thread'] += 1
                print(f"Starved thread accessed resource {access_count['starved_thread']} times")
            finally:
                lock.release()
            time.sleep(0.1)  # 다음 접근까지 긴 대기

# 스레드 시작
priority = threading.Thread(target=priority_thread)
starved = threading.Thread(target=starved_thread)

priority.start()
starved.start()

# 스레드 종료 대기
priority.join()
starved.join()

# 최종 결과 출력
print("Final access counts:", access_count)

# 16:100