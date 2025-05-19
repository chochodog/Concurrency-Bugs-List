import threading
import time

# 공유 자원에 대한 뮤텍스
mutex = threading.Lock()

# 스레드가 자원에 접근하는 함수
def thread_function(name):
    while True:
        if name == "Thread-1":
            mutex.acquire()
            print(f"{name} has the resource")
            time.sleep(0.1)  # Thread-1은 자원을 더 오래 점유
        elif mutex.acquire(blocking=False):
            print(f"{name} got the resource")
            mutex.release()
        else:
            print(f"{name} is starving")
        time.sleep(0.05)

# 스레드 생성 및 시작
thread1 = threading.Thread(target=thread_function, args=("Thread-1",))
thread2 = threading.Thread(target=thread_function, args=("Thread-2",))
thread1.start()
thread2.start()

# 주로 테스트 환경에서는 스레드를 끝내거나 시간 제한을 두어 실행합니다.
# 이 예에서는 코드가 무한 루프에 있으므로 주의해서 사용하세요.
