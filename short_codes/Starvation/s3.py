import threading
import time

def resource_user(thread_id, hold_time):
    while True:
        with resource_lock:
            print(f"Thread {thread_id} is using the resource.")
            time.sleep(hold_time)
            print(f"Thread {thread_id} released the resource.")

resource_lock = threading.Lock()
thread1 = threading.Thread(target=resource_user, args=(1, 0.5))
thread2 = threading.Thread(target=resource_user, args=(2, 0.1))

thread1.start()
thread2.start()
