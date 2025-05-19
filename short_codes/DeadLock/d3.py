import threading
import time

sem = threading.Semaphore(1)

def task():
    print("Trying to acquire semaphore...")
    sem.acquire()
    print("Semaphore acquired")
    time.sleep(2)  # 임의의 작업
    print("Trying to acquire semaphore again...")  
    sem.acquire()  # 이미 획득한 세마포어를 다시 획득하려 함 -> 데드락 발생
    print("Semaphore acquired again (never reached)")
    sem.release()
    sem.release()

t = threading.Thread(target=task)
t.start()
t.join()
