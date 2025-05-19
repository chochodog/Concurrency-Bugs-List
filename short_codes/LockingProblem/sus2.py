import threading
import time

def work(name, duration):
    print(f"{name}: Waiting for lock")
    start = time.time()
    with lock:
        print(f"{name}: Got lock after {time.time()-start:.2f}s")
        time.sleep(duration)  # Simulate work
    print(f"{name}: Released lock")

lock = threading.Lock()

# First thread gets lock and holds it for a long time
threading.Thread(target=work, args=("LongTask", 3)).start()

# Small delay to ensure first thread gets lock
time.sleep(0.1)

# These threads will be suspended waiting for the lock
for i in range(3):
    threading.Thread(target=work, args=(f"Worker-{i}", 0.2)).start()