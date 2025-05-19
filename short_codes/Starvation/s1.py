import threading
import time
import queue

priority_queue = queue.PriorityQueue()

def access_resource(priority, thread_id):
    attempt_count = 0
    while attempt_count < 20:
        priority_queue.put((priority, thread_id))
        got_resource = False
        while not priority_queue.empty() and not got_resource:
            current_prio, tid = priority_queue.get()
            if tid == thread_id:
                current_time = time.strftime('%H:%M:%S', time.localtime())
                print(f"[{current_time}] Thread {thread_id} with priority {current_prio} is accessing the resource.")
                time.sleep(0.2)
                print(f"[{current_time}] Thread {thread_id} with priority {current_prio} has released the resource.")
                got_resource = True
                if priority > 1:
                    time.sleep(0.3)
            else:
                priority_queue.put((current_prio, tid))
                time.sleep(0.1)
        attempt_count += 1
        if not got_resource:
            current_time = time.strftime('%H:%M:%S', time.localtime())
            print(f"[{current_time}] Thread {thread_id} with priority {priority} is waiting and could be starving.")
        time.sleep(0.1)
threads = []
priorities = [5, 1]
for i, priority in enumerate(priorities):
    thread = threading.Thread(target=access_resource, args=(priority, i+1))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("Simulation complete.")
