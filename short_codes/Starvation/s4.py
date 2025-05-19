import threading
import time

def resource_user(thread_id, access_interval, use_time):
    for _ in range(10):
        time.sleep(access_interval)  # 스레드가 자원에 접근하기 전 대기하는 시간
        start_time = time.time()  # 자원 점유 시작 시간
        with resource_lock:
            current_time = time.strftime('%H:%M:%S', time.localtime(start_time))
            print(f"{current_time} - Thread {thread_id} is using the resource.")
            time.sleep(use_time)  # 자원을 사용하는 시간
            end_time = time.time()  # 자원 점유 종료 시간
            elapsed_time = end_time - start_time
            current_end_time = time.strftime('%H:%M:%S', time.localtime(end_time))
            print(f"{current_end_time} - Thread {thread_id} released the resource after {elapsed_time:.2f} seconds.")

resource_lock = threading.Lock()

# 스레드 생성
# Thread-1: 높은 우선순위, 빈번한 접근, 긴 사용 시간
thread1 = threading.Thread(target=resource_user, args=(1, 0.1, 0.5))
# Thread-2: 낮은 우선순위, 드문 접근, 짧은 사용 시간
thread2 = threading.Thread(target=resource_user, args=(2, 1.0, 0.1))

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print("Simulation complete.")
