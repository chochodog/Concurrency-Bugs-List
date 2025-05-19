import threading
import time

def resource_user(thread_id, lock, delay):
    print(f"Thread {thread_id}: waiting for lock")
    start = time.time()
    
    with lock:
        wait_time = time.time() - start
        print(f"Thread {thread_id}: acquired lock after {wait_time:.2f} seconds")
        print(f"Thread {thread_id}: using resource for {delay} seconds")
        time.sleep(delay)
    
    print(f"Thread {thread_id}: released lock")

lock = threading.Lock()

hog = threading.Thread(target=resource_user, args=("HOG", lock, 8))

waiting_threads = [
    threading.Thread(target=resource_user, args=(i, lock, 0.5)) 
    for i in range(3)
]

hog.start()
time.sleep(0.1)
for t in waiting_threads:
    t.start()

for t in waiting_threads:
    t.join()
hog.join()


