import threading
import time

class Resource:
    def __init__(self, name):
        self.name = name
        self.lock = threading.Lock()
        self.owner = None
    
    def acquire(self, owner):
        if self.lock.acquire(False):
            self.owner = owner
            print(f"{owner} acquired {self.name}")
            return True
        return False
    
    def release(self):
        if self.owner:
            print(f"{self.owner} released {self.name}")
            self.owner = None
            self.lock.release()


def worker(name, first, second):
    attempts = 0
    
    while attempts < 5:
        attempts += 1
        
        if not first.acquire(name):
            print(f"{name} waiting for {first.name}...")
            time.sleep(0.1)
            continue
        
        time.sleep(0.1)
        
        if not second.acquire(name):
            print(f"{name} couldn't get {second.name}, releasing {first.name}")
            first.release()
            time.sleep(0.2)
            continue
        
        print(f"{name} got both resources!")
        time.sleep(0.5)
        second.release()
        first.release()
        return
    
    print(f"{name} gave up after {attempts} attempts - LIVELOCK!")

resource_A = Resource("Resource A")
resource_B = Resource("Resource B")

thread1 = threading.Thread(target=worker, args=("Thread-1", resource_A, resource_B))
thread2 = threading.Thread(target=worker, args=("Thread-2", resource_B, resource_A))

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print("Simulation finished")
