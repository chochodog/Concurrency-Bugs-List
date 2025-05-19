import multiprocessing
import time

def worker(name, first_lock, second_lock):
    while True:
        print(f"{name} trying to acquire first lock")
        if first_lock.acquire(timeout=1):
            print(f"{name} acquired first lock")
            time.sleep(0.1)
            
            print(f"{name} trying to acquire second lock")
            if not second_lock.acquire(timeout=1):
                print(f"{name} couldn't get second lock, releasing first lock")
                first_lock.release()
                time.sleep(0.1)
                continue
            
            print(f"{name} acquired both locks!")
            return

if __name__ == "__main__":
    lock_a = multiprocessing.Lock()
    lock_b = multiprocessing.Lock()
    
    p1 = multiprocessing.Process(target=worker, args=("Worker1", lock_a, lock_b))
    p2 = multiprocessing.Process(target=worker, args=("Worker2", lock_b, lock_a))
    
    p1.start()
    p2.start()
    
    time.sleep(5)
    
    p1.terminate()
    p2.terminate()
    p1.join()
    p2.join()
