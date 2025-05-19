import threading

condition = threading.Condition()
shared_resource = False  # 공유 자원 상태

def worker():
    global shared_resource
    with condition:
        print("Worker waiting for resource...")
        while not shared_resource:
            condition.wait()  # shared_resource가 True가 될 때까지 대기
        print("Worker proceeding with resource")

def notifier():
    global shared_resource
    with condition:
        print("Notifier setting resource...")
        shared_resource = True  # 자원 설정
        # condition.notify()를 호출하지 않아 worker 스레드가 계속 대기함 (데드락 발생)

worker_thread = threading.Thread(target=worker)
notifier_thread = threading.Thread(target=notifier)

worker_thread.start()
notifier_thread.start()

worker_thread.join()
notifier_thread.join()
