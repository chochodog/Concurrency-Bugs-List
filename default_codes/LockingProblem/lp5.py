import threading
import time

class TaskManager:
    def __init__(self):
        self.shared_resource = 0
        self.lock = threading.Lock()
        self.task_log = []  # 작업 기록을 위한 리스트
        self.task_count = {"long": 0, "short": 0}  # 작업 횟수 추적

    # 작업 기록 추가
    def log_task(self, task_name):
        with self.lock:
            self.task_log.append((task_name, time.time()))

    # 작업 횟수 증가
    def increment_task_count(self, task_type):
        with self.lock:
            if task_type in self.task_count:
                self.task_count[task_type] += 1

    # 긴 작업: 공유 리소스에 많은 계산 작업 수행
    def long_task(self):
        print(f"Long task started by {threading.current_thread().name}")
        self.log_task("Long task started")
        self.increment_task_count("long")
        with self.lock:
            for _ in range(50_000_000):  # 긴 연산 수행 (연산량 증가)
                self.shared_resource += 1
        self.log_task("Long task finished")
        print(f"Long task finished by {threading.current_thread().name}")

    # 짧은 작업: 공유 리소스에 간단한 작업 수행
    def short_task(self):
        print(f"Short task started by {threading.current_thread().name}")
        self.log_task("Short task started")
        self.increment_task_count("short")
        with self.lock:
            for _ in range(1_000_000):  # 반복 횟수 증가
                self.shared_resource += 1
        self.log_task("Short task finished")
        print(f"Short task finished by {threading.current_thread().name}")

    # 스레드 관리
    def run_tasks(self):
        threads = []

        # 긴 작업 스레드 생성
        for _ in range(2):  # 긴 작업 2개
            thread = threading.Thread(target=self.long_task)
            threads.append(thread)

        # 짧은 작업 스레드 생성
        for _ in range(5):  # 짧은 작업 5개
            thread = threading.Thread(target=self.short_task)
            threads.append(thread)

        # 시작 시간 기록
        start_time = time.time()

        # 스레드를 순차적으로 시작
        for thread in threads:
            thread.start()

        # 모든 스레드가 종료되길 기다림
        for thread in threads:
            thread.join()

        # 종료 시간 기록
        end_time = time.time()

        # 총 소요 시간 계산 및 출력
        total_time = end_time - start_time
        print(f"Total execution time: {total_time:.5f} seconds")

    # 작업 로그 출력
    def print_task_log(self):
        print("\nTask Log:")
        for log in self.task_log:
            task_name, timestamp = log
            print(f"{task_name} at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))}")

    # 작업 횟수 출력
    def print_task_count(self):
        print("\nTask Counts:")
        for task_type, count in self.task_count.items():
            print(f"{task_type.capitalize()} tasks: {count}")

    # 공유 리소스 값 초기화
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
