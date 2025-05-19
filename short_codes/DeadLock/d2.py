import threading

condition = threading.Condition()
shared_resource = False
def worker():
    global shared_resource
    with condition:
        print("Worker waiting for resource...")
        while not shared_resource:
            condition.wait()
        print("Worker proceeding with resource")

def notifier():
    global shared_resource
    with condition:
        print("Notifier setting resource...")
        shared_resource = True

worker_thread = threading.Thread(target=worker)
notifier_thread = threading.Thread(target=notifier)

worker_thread.start()
notifier_thread.start()

worker_thread.join()
notifier_thread.join()
