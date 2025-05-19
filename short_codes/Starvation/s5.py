import threading
import time

lock = threading.Lock()

access_count = {
    'priority_thread': 0,
    'starved_thread': 0
}

def priority_thread():
    while access_count['priority_thread'] < 100:
        lock.acquire()
        try:
            access_count['priority_thread'] += 1
            print(f"Priority thread accessed resource {access_count['priority_thread']} times")
            time.sleep(0.01)
        finally:
            lock.release()
        time.sleep(0.005)

def starved_thread():
    while access_count['starved_thread'] < 100:
        if lock.acquire(timeout=0.002):
            try:
                access_count['starved_thread'] += 1
                print(f"Starved thread accessed resource {access_count['starved_thread']} times")
            finally:
                lock.release()
            time.sleep(0.1)

priority = threading.Thread(target=priority_thread)
starved = threading.Thread(target=starved_thread)

priority.start()
starved.start()

priority.join()
starved.join()

print("Final access counts:", access_count)
