import threading
import time

def work(name, duration):
    print(f"{name}: Waiting for lock")
    start = time.time()
    with lock:
        print(f"{name}: Got lock after {time.time()-start:.2f}s")
        time.sleep(duration)
    print(f"{name}: Released lock")

lock = threading.Lock()

threading.Thread(target=work, args=("LongTask", 3)).start()

time.sleep(0.1)

for i in range(3):
    threading.Thread(target=work, args=(f"Worker-{i}", 0.2)).start()
