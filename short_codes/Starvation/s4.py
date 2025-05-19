import threading
import time

def resource_user(thread_id, access_interval, use_time):
    for _ in range(10):
        time.sleep(access_interval)
        start_time = time.time()
        with resource_lock:
            current_time = time.strftime('%H:%M:%S', time.localtime(start_time))
            print(f"{current_time} - Thread {thread_id} is using the resource.")
            time.sleep(use_time)
            end_time = time.time()
            elapsed_time = end_time - start_time
            current_end_time = time.strftime('%H:%M:%S', time.localtime(end_time))
            print(f"{current_end_time} - Thread {thread_id} released the resource after {elapsed_time:.2f} seconds.")

resource_lock = threading.Lock()

thread1 = threading.Thread(target=resource_user, args=(1, 0.1, 0.5))
thread2 = threading.Thread(target=resource_user, args=(2, 1.0, 0.1))

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print("Simulation complete.")
