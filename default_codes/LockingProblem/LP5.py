import threading
import time

class TaskManager:
    def __init__(self):
        self.shared_resource = 0
        self.lock = threading.Lock()
        self.task_log = []
        self.task_count = {"long": 0, "short": 0}

    def log_task(self, task_name):
        with self.lock:
            self.task_log.append((task_name, time.time()))


    def increment_task_count(self, task_type):
        with self.lock:
            if task_type in self.task_count:
                self.task_count[task_type] += 1

    def long_task(self):
        print(f"Long task started by {threading.current_thread().name}")
        self.log_task("Long task started")
        self.increment_task_count("long")
        with self.lock:
            for _ in range(50_000_000):
                self.shared_resource += 1
        self.log_task("Long task finished")
        print(f"Long task finished by {threading.current_thread().name}")

    def short_task(self):
        print(f"Short task started by {threading.current_thread().name}")
        self.log_task("Short task started")
        self.increment_task_count("short")
        with self.lock:
            for _ in range(1_000_000):
                self.shared_resource += 1
        self.log_task("Short task finished")
        print(f"Short task finished by {threading.current_thread().name}")

    def run_tasks(self):
        threads = []

        for _ in range(2):
            thread = threading.Thread(target=self.long_task)
            threads.append(thread)

        for _ in range(5):
            thread = threading.Thread(target=self.short_task)
            threads.append(thread)

        start_time = time.time()

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        end_time = time.time()

        total_time = end_time - start_time
        print(f"Total execution time: {total_time:.5f} seconds")

    def print_task_log(self):
        print("\nTask Log:")
        for log in self.task_log:
            task_name, timestamp = log
            print(f"{task_name} at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))}")

    def print_task_count(self):
        print("\nTask Counts:")
        for task_type, count in self.task_count.items():
            print(f"{task_type.capitalize()} tasks: {count}")

    def reset_shared_resource(self):
        with self.lock:
            self.shared_resource = 0
        print("Shared resource has been reset.")

if __name__ == "__main__":
    task_manager = TaskManager()
    task_manager.run_tasks()
    print(f"Final value of shared_resource: {task_manager.shared_resource}")
    task_manager.print_task_log()
    task_manager.print_task_count()
    task_manager.reset_shared_resource()
