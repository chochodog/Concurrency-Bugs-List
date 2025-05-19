import threading
import time

def resource_user(thread_id, hold_time):
    while True:
        with resource_lock:
            print(f"Thread {thread_id} is using the resource.")
            time.sleep(hold_time)  # 자원을 사용하는 시간
            print(f"Thread {thread_id} released the resource.")

resource_lock = threading.Lock()
# 스레드 1은 자원을 0.5초 동안 사용
thread1 = threading.Thread(target=resource_user, args=(1, 0.5))
# 스레드 2는 자원을 0.1초 동안만 사용
thread2 = threading.Thread(target=resource_user, args=(2, 0.1))

thread1.start()
thread2.start()
