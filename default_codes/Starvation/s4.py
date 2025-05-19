import heapq
import random
import time
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
import matplotlib.pyplot as plt
import numpy as np

class Priority(Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    
    def __str__(self):
        return self.name

@dataclass
class Request:
    id: int
    priority: Priority
    creation_time: float
    duration: float
    start_time: Optional[float] = None
    completion_time: Optional[float] = None
    
    def wait_time(self) -> float:
        """Calculate how long request waited before being processed"""
        if self.start_time is None:
            return time.time() - self.creation_time
        return self.start_time - self.creation_time
    
    def is_complete(self) -> bool:
        """Check if request has been completed"""
        return self.completion_time is not None
    
    def __lt__(self, other):
        return self.priority.value < other.priority.value

class ResourceManager:
    def __init__(self, preemption_enabled=True, starvation_threshold=10.0):
        self.request_queue = []
        self.all_requests = []
        self.current_request = None
        self.current_execution_start = 0
        self.time_elapsed = 0
        self.preemption_enabled = preemption_enabled
        self.starvation_threshold = starvation_threshold
        self.request_counter = 0
        
    def add_request(self, priority: Priority, duration: float) -> int:
        """Add a new request to the queue"""
        self.request_counter += 1
        request = Request(
            id=self.request_counter,
            priority=priority,
            creation_time=self.time_elapsed,
            duration=duration
        )
        heapq.heappush(self.request_queue, request)
        self.all_requests.append(request)
        print(f"[{self.time_elapsed:.2f}] New request #{request.id} added with {priority} priority, duration: {duration:.2f}")
        return request.id
    
    def check_starvation(self) -> List[Request]:
        """Identify starving requests in the queue"""
        starving = []
        for req in self.request_queue:
            wait_time = self.time_elapsed - req.creation_time
            if wait_time > self.starvation_threshold:
                starving.append(req)
        return starving
    
    def step(self, time_step: float = 1.0) -> None:
        """Simulate one time step in the resource allocation system"""
        self.time_elapsed += time_step
        
        if self.current_request:
            time_spent = self.time_elapsed - self.current_execution_start

            if time_spent >= self.current_request.duration:
                self.current_request.completion_time = self.time_elapsed
                print(f"[{self.time_elapsed:.2f}] Request #{self.current_request.id} ({self.current_request.priority}) completed. " +
                      f"Wait time: {self.current_request.wait_time():.2f}, Total time: {self.time_elapsed - self.current_request.creation_time:.2f}")
                self.current_request = None
            

            elif self.preemption_enabled and self.request_queue and self.request_queue[0].priority.value < self.current_request.priority.value:
                next_request = self.request_queue[0]
                print(f"[{self.time_elapsed:.2f}] Request #{self.current_request.id} ({self.current_request.priority}) " +
                      f"preempted by #{next_request.id} ({next_request.priority})")
                

                self.current_request.duration -= time_spent
                heapq.heappush(self.request_queue, self.current_request)
                self.current_request = None
        

        if not self.current_request and self.request_queue:
            self.current_request = heapq.heappop(self.request_queue)
            self.current_request.start_time = self.time_elapsed
            self.current_execution_start = self.time_elapsed
            print(f"[{self.time_elapsed:.2f}] Started processing request #{self.current_request.id} " +
                  f"({self.current_request.priority}). Wait time: {self.current_request.wait_time():.2f}")
        

        starving = self.check_starvation()
        if starving:
            priorities = {}
            for req in starving:
                if req.priority not in priorities:
                    priorities[req.priority] = 0
                priorities[req.priority] += 1
            
            print(f"[{self.time_elapsed:.2f}] STARVATION ALERT: {len(starving)} requests starving!")
            for priority, count in priorities.items():
                print(f"  - {priority}: {count} requests")
            
            worst = max(starving, key=lambda r: self.time_elapsed - r.creation_time)
            print(f"  - Worst case: Request #{worst.id} ({worst.priority}) waiting for {self.time_elapsed - worst.creation_time:.2f} units")
    
    def simulate(self, steps: int, generation_probability: float = 0.3) -> None:
        """Run the simulation for a specified number of steps"""
        for _ in range(steps):
            if random.random() < generation_probability:
                priority_weights = [0.6, 0.3, 0.1]
                priority = random.choices(list(Priority), weights=priority_weights)[0]
                duration = random.uniform(1.0, 5.0)
                self.add_request(priority, duration)
            
            self.step()
    
    def generate_statistics(self):
        """Generate statistics about request processing"""
        if not self.all_requests:
            return "No requests processed."
        
        stats = {
            "total_requests": len(self.all_requests),
            "completed": sum(1 for r in self.all_requests if r.is_complete()),
            "in_progress": 1 if self.current_request else 0,
            "waiting": len(self.request_queue),
            "by_priority": {p: 0 for p in Priority},
            "avg_wait_time": 0,
            "avg_wait_by_priority": {p: 0 for p in Priority}
        }
        
        wait_times = []
        wait_by_priority = {p: [] for p in Priority}
        
        for req in self.all_requests:
            stats["by_priority"][req.priority] += 1
            if req.is_complete():
                wait_time = req.start_time - req.creation_time
                wait_times.append(wait_time)
                wait_by_priority[req.priority].append(wait_time)
        
        if wait_times:
            stats["avg_wait_time"] = sum(wait_times) / len(wait_times)
            
        for p in Priority:
            if wait_by_priority[p]:
                stats["avg_wait_by_priority"][p] = sum(wait_by_priority[p]) / len(wait_by_priority[p])
        
        starving = self.check_starvation()
        stats["starving_requests"] = len(starving)
        stats["starving_by_priority"] = {p: 0 for p in Priority}
        for req in starving:
            stats["starving_by_priority"][req.priority] += 1
            
        return stats
    
    def plot_wait_times(self):
        """Generate a plot showing wait times by priority"""
        completed_requests = [r for r in self.all_requests if r.is_complete()]
        if not completed_requests:
            print("No completed requests to plot.")
            return
        
        plt.figure(figsize=(12, 8))
        plt.subplot(2, 2, 1)
        priorities = [p for p in Priority]
        for priority in priorities:
            requests = [r for r in completed_requests if r.priority == priority]
            if requests:
                x = [r.id for r in requests]
                y = [r.wait_time() for r in requests]
                plt.scatter(x, y, label=str(priority), alpha=0.7)
        
        plt.xlabel('Request ID')
        plt.ylabel('Wait Time')
        plt.title('Wait Time by Priority')
        plt.legend()
        plt.subplot(2, 2, 2)
        avg_wait = {}
        for priority in priorities:
            requests = [r for r in completed_requests if r.priority == priority]
            if requests:
                avg_wait[priority] = sum(r.wait_time() for r in requests) / len(requests)
        
        if avg_wait:
            priorities_str = [str(p) for p in avg_wait.keys()]
            wait_times = list(avg_wait.values())
            plt.bar(priorities_str, wait_times)
            plt.xlabel('Priority')
            plt.ylabel('Average Wait Time')
            plt.title('Average Wait Time by Priority')
        
        plt.subplot(2, 1, 2)
        for req in completed_requests:
            color = 'green' if req.priority == Priority.HIGH else ('orange' if req.priority == Priority.MEDIUM else 'red')
            plt.plot([req.creation_time, req.start_time, req.completion_time], 
                     [req.id, req.id, req.id], 
                     marker='o', 
                     color=color,
                     alpha=0.7)
            
            plt.plot([req.creation_time, req.start_time], 
                     [req.id, req.id], 
                     linewidth=2, 
                     color='blue',
                     alpha=0.5)
            
            plt.plot([req.start_time, req.completion_time], 
                     [req.id, req.id], 
                     linewidth=2, 
                     color='green',
                     alpha=0.5)
        
        plt.xlabel('Time')
        plt.ylabel('Request ID')
        plt.title('Request Timeline (Blue: Waiting, Green: Processing)')
        
        plt.tight_layout()
        plt.show()


def run_simple_demo():
    print("=== RESOURCE ALLOCATION SIMULATION ===")
    print("This simulation demonstrates priority-based resource allocation with preemption")
    print("High priority requests will always be served before lower priority ones")
    print("This can lead to starvation of low priority requests")
    print("\nRunning simulation with preemption enabled...\n")
    
    manager = ResourceManager(preemption_enabled=True, starvation_threshold=15.0)
    manager.add_request(Priority.LOW, 8.0)
    manager.add_request(Priority.LOW, 6.0)
    manager.add_request(Priority.MEDIUM, 4.0)
    manager.simulate(50, generation_probability=0.3)
    
    print("\n=== SIMULATION STATISTICS ===")
    stats = manager.generate_statistics()
    print(f"Total requests: {stats['total_requests']}")
    print(f"Completed: {stats['completed']}")
    print(f"In progress: {stats['in_progress']}")
    print(f"Waiting: {stats['waiting']}")
    print("\nRequests by priority:")
    for p in Priority:
        print(f"  - {p}: {stats['by_priority'][p]}")
    
    print(f"\nAverage wait time: {stats['avg_wait_time']:.2f}")
    print("Average wait time by priority:")
    for p in Priority:
        if stats['avg_wait_by_priority'][p] > 0:
            print(f"  - {p}: {stats['avg_wait_by_priority'][p]:.2f}")
    
    print(f"\nStarving requests: {stats['starving_requests']}")
    if stats['starving_requests'] > 0:
        print("Starving requests by priority:")
        for p in Priority:
            if stats['starving_by_priority'][p] > 0:
                print(f"  - {p}: {stats['starving_by_priority'][p]}")
    
    manager.plot_wait_times()


def run_comparative_demo():
    """Run a comparative demo showing systems with and without preemption"""
    print("\n=== SIMULATION WITH PREEMPTION (SHOWS STARVATION) ===\n")
    manager1 = ResourceManager(preemption_enabled=True, starvation_threshold=15.0)
    seed = int(time.time())
    random.seed(seed)
    
    manager1.add_request(Priority.LOW, 5.0)
    manager1.add_request(Priority.LOW, 5.0)
    manager1.add_request(Priority.LOW, 5.0)
    
    manager1.simulate(50, generation_probability=0.3)
    stats1 = manager1.generate_statistics()
    

    print("\n=== SIMULATION WITHOUT PREEMPTION (MORE FAIR) ===\n")
    manager2 = ResourceManager(preemption_enabled=False, starvation_threshold=15.0)
    random.seed(seed)
    

    manager2.add_request(Priority.LOW, 5.0)
    manager2.add_request(Priority.LOW, 5.0)
    manager2.add_request(Priority.LOW, 5.0)
    
    manager2.simulate(50, generation_probability=0.3)
    stats2 = manager2.generate_statistics()
    

    print("\n=== COMPARISON ===")
    print(f"{'Metric':<25} {'With Preemption':<20} {'Without Preemption':<20}")
    print("-" * 65)
    print(f"{'Completed requests':<25} {stats1['completed']:<20} {stats2['completed']:<20}")
    print(f"{'Starving requests':<25} {stats1['starving_requests']:<20} {stats2['starving_requests']:<20}")
    print(f"{'Avg wait time':<25} {stats1['avg_wait_time']:.2f:<20} {stats2['avg_wait_time']:.2f:<20}")
    
    for p in Priority:
        wait1 = stats1['avg_wait_by_priority'][p]
        wait2 = stats2['avg_wait_by_priority'][p]
        if wait1 > 0 or wait2 > 0:
            print(f"{'Avg wait - ' + str(p):<25} {wait1:.2f if wait1 > 0 else 'N/A':<20} {wait2:.2f if wait2 > 0 else 'N/A':<20}")
    

    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 1, 1)
    completed1 = [r for r in manager1.all_requests if r.is_complete()]
    for req in completed1:
        color = 'green' if req.priority == Priority.HIGH else ('orange' if req.priority == Priority.MEDIUM else 'red')
        plt.plot([req.creation_time, req.start_time, req.completion_time], 
                 [req.id, req.id, req.id], 
                 marker='o', 
                 color=color,
                 alpha=0.7)
    plt.title('Request Timeline WITH Preemption')
    plt.xlabel('Time')
    plt.ylabel('Request ID')
    plt.text(0.02, 0.9, 'Color: Green=HIGH, Orange=MEDIUM, Red=LOW', transform=plt.gca().transAxes)
    
    plt.subplot(2, 1, 2)
    completed2 = [r for r in manager2.all_requests if r.is_complete()]
    for req in completed2:
        color = 'green' if req.priority == Priority.HIGH else ('orange' if req.priority == Priority.MEDIUM else 'red')
        plt.plot([req.creation_time, req.start_time, req.completion_time], 
                 [req.id, req.id, req.id], 
                 marker='o', 
                 color=color,
                 alpha=0.7)
    plt.title('Request Timeline WITHOUT Preemption')
    plt.xlabel('Time')
    plt.ylabel('Request ID')
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    run_simple_demo()
