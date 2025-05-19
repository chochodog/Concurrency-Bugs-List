import threading
import time

class ResourceAllocator:
    def __init__(self):
        self.lock = threading.Lock()
        self.access_count = {
            'priority_thread': 0,
            'starved_thread': 0
        }
        self.resource_usage_log = []

    def priority_thread(self):
        """high priority_thread."""
        while self.access_count['priority_thread'] < 500:
            self.lock.acquire()
            try:
                self.access_count['priority_thread'] += 1
                self.resource_usage_log.append(f"Priority thread accessed at count {self.access_count['priority_thread']}")
                print(f"Priority thread accessed resource {self.access_count['priority_thread']} times")
                time.sleep(0.01)
            finally:
                self.lock.release()
            time.sleep(0.005)

    def starved_thread(self):
        """starved_thread."""
        while self.access_count['starved_thread'] < 500:
            if self.lock.acquire(timeout=0.002):
                try:
                    self.access_count['starved_thread'] += 1
                    self.resource_usage_log.append(f"Starved thread accessed at count {self.access_count['starved_thread']}")
                    print(f"Starved thread accessed resource {self.access_count['starved_thread']} times")
                finally:
                    self.lock.release()
                time.sleep(0.1)

    def simulate_starvation(self):
        """resource access simulation."""
        priority = threading.Thread(target=self.priority_thread)
        starved = threading.Thread(target=self.starved_thread)

        priority.start()
        starved.start()

        priority.join()
        starved.join()

        print("Final access counts:", self.access_count)
        self.log_resource_usage()

    def log_resource_usage(self):
        """resource usage Log"""
        print("\nResource Usage Log:")
        for log_entry in self.resource_usage_log:
            print(log_entry)

if __name__ == "__main__":
    allocator = ResourceAllocator()
    allocator.simulate_starvation()

# 79:500
