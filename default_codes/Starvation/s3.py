import threading
import time
import random
import logging
from queue import PriorityQueue
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
)

class FileSystem:
    def __init__(self):
        self.lock = threading.Lock()
        self.waiting_threads = PriorityQueue()
        self.current_owner = None
        # Track execution timeline
        self.execution_history = []
        self.simulation_start_time = time.time()
        
    def request_access(self, thread_id, priority):
        """Request access to the file system resource"""
        start_waiting = time.time()
        
        with self.lock:
            # Add to waiting queue with priority (lower number = higher priority)
            self.waiting_threads.put((priority, thread_id, start_waiting))
            logging.info(f"Thread {thread_id} (priority {priority}) requested access to resource")
        
        # Wait until this thread becomes the owner
        while True:
            with self.lock:
                if self.current_owner is None:
                    # Check if this thread has highest priority
                    if not self.waiting_threads.empty():
                        next_priority, next_id, wait_start = self.waiting_threads.get()
                        if next_id == thread_id:
                            self.current_owner = thread_id
                            wait_time = time.time() - wait_start
                            current_time = time.time() - self.simulation_start_time
                            # Record access time in execution history
                            self.execution_history.append({
                                'thread_id': thread_id,
                                'priority': priority,
                                'action': 'access',
                                'time': current_time,
                                'wait_time': wait_time
                            })
                            logging.info(f"Thread {thread_id} (priority {priority}) gained access after waiting {wait_time:.2f} seconds")
                            return wait_time
                        else:
                            # Put it back, it's not our turn
                            self.waiting_threads.put((next_priority, next_id, wait_start))
            
            # Sleep briefly to prevent CPU hogging
            time.sleep(0.01)
    
    def release_access(self, thread_id, priority):
        """Release access to the file system resource"""
        with self.lock:
            if self.current_owner == thread_id:
                self.current_owner = None
                current_time = time.time() - self.simulation_start_time
                # Record release time in execution history
                self.execution_history.append({
                    'thread_id': thread_id,
                    'priority': priority,
                    'action': 'release',
                    'time': current_time
                })
                logging.info(f"Thread {thread_id} released resource")
            else:
                logging.warning(f"Thread {thread_id} attempted to release resource it doesn't own")

    def visualize_execution(self, thread_info):
        """Generate visualization of resource usage over time"""
        if not self.execution_history:
            logging.warning("No execution history to visualize")
            return
        
        # Group events by thread
        thread_events = defaultdict(list)
        for event in self.execution_history:
            if event['action'] == 'access':
                thread_events[event['thread_id']].append((event['time'], 'start'))
            else:
                thread_events[event['thread_id']].append((event['time'], 'end'))
        
        # Sort threads by priority for visualization
        thread_ids = sorted(thread_events.keys(), 
                           key=lambda tid: next(t.priority for t in thread_info if t.thread_id == tid))
        
        # Colors based on priority group
        colors = {
            'HP': 'green',
            'MP': 'blue',
            'LP': 'red',
        }
        
        plt.figure(figsize=(15, 8))
        
        # Plot resource usage timelines
        y_pos = len(thread_ids)
        for i, thread_id in enumerate(thread_ids):
            events = sorted(thread_events[thread_id])
            
            # Skip threads with only one event (likely never released)
            if len(events) % 2 != 0:
                events = events[:-1]
            
            if not events:
                continue
                
            # Get color based on thread type
            thread_type = thread_id.split('-')[0]
            color = colors.get(thread_type, 'gray')
            
            # Parse events into start/end pairs
            for j in range(0, len(events), 2):
                if j+1 < len(events):  # Make sure we have a complete pair
                    start_time, _ = events[j]
                    end_time, _ = events[j+1]
                    plt.hlines(y=y_pos-i, xmin=start_time, xmax=end_time, 
                              linewidth=10, color=color, alpha=0.7)
        
        # Add a legend
        legend_elements = [
            plt.Line2D([0], [0], color='green', lw=4, label='High Priority'),
            plt.Line2D([0], [0], color='blue', lw=4, label='Medium Priority'),
            plt.Line2D([0], [0], color='red', lw=4, label='Low Priority')
        ]
        plt.legend(handles=legend_elements)
        
        # Set labels and title
        plt.yticks(range(1, len(thread_ids)+1), thread_ids)
        plt.xlabel('Simulation Time (seconds)')
        plt.ylabel('Thread ID')
        plt.title('Resource Access Timeline - Thread Starvation Visualization')
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        
        # Save the visualization
        plt.tight_layout()
        plt.savefig('starvation_visualization.png')
        logging.info("Saved visualization to 'starvation_visualization.png'")
        
        # Create wait time analysis visualization
        self.visualize_wait_times(thread_info)
    
    def visualize_wait_times(self, thread_info):
        """Create a visualization of wait times by priority group"""
        # Extract wait times by priority group
        high_waits = []
        medium_waits = []
        low_waits = []
        
        for event in self.execution_history:
            if event['action'] == 'access' and 'wait_time' in event:
                tid = event['thread_id']
                priority = event['priority']
                
                if priority <= 2:
                    high_waits.append(event['wait_time'])
                elif priority <= 5:
                    medium_waits.append(event['wait_time'])
                else:
                    low_waits.append(event['wait_time'])
        
        # Calculate statistics
        def calc_stats(wait_times):
            if not wait_times:
                return 0, 0, 0
            return np.mean(wait_times), np.median(wait_times), np.max(wait_times)
        
        high_stats = calc_stats(high_waits)
        medium_stats = calc_stats(medium_waits)
        low_stats = calc_stats(low_waits)
        
        # Create bar chart
        plt.figure(figsize=(12, 8))
        groups = ['High Priority', 'Medium Priority', 'Low Priority']
        means = [high_stats[0], medium_stats[0], low_stats[0]]
        medians = [high_stats[1], medium_stats[1], low_stats[1]]
        maxes = [high_stats[2], medium_stats[2], low_stats[2]]
        
        x = np.arange(len(groups))
        width = 0.25
        
        plt.bar(x - width, means, width, label='Mean Wait Time', color='blue')
        plt.bar(x, medians, width, label='Median Wait Time', color='green')
        plt.bar(x + width, maxes, width, label='Max Wait Time', color='red')
        
        plt.ylabel('Wait Time (seconds)')
        plt.title('Resource Wait Times by Priority Group')
        plt.xticks(x, groups)
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        plt.savefig('wait_time_analysis.png')
        logging.info("Saved wait time analysis to 'wait_time_analysis.png'")


class FileSystemThread(threading.Thread):
    def __init__(self, thread_id, filesystem, priority, access_count=5):
        super().__init__()
        self.thread_id = thread_id
        self.filesystem = filesystem
        self.priority = priority  # Lower number = higher priority
        self.access_count = access_count
        self.total_wait_time = 0
        self.successful_accesses = 0
        self.wait_times = []
        self.start_time = None
        self.end_time = None
        
    def run(self):
        self.start_time = time.time()
        for i in range(self.access_count):
            try:
                # Request access to resource
                wait_time = self.filesystem.request_access(self.thread_id, self.priority)
                self.total_wait_time += wait_time
                self.wait_times.append(wait_time)
                self.successful_accesses += 1
                
                # Simulate using the resource
                usage_time = random.uniform(0.1, 0.3)
                if self.priority <= 2:  # High priority threads use resources longer
                    usage_time *= 3
                time.sleep(usage_time)
                
                # Release the resource
                self.filesystem.release_access(self.thread_id, self.priority)
                
                # High priority threads request again immediately
                # Low priority threads wait a bit
                if self.priority > 3:
                    time.sleep(random.uniform(0.1, 0.3))
                
            except Exception as e:
                logging.error(f"Thread {self.thread_id} encountered error: {e}")
        self.end_time = time.time()


def run_simulation(duration=15):
    # Create shared file system
    filesystem = FileSystem()
    
    # Create threads with different priorities
    threads = []
    
    # High priority threads (1-2)
    for i in range(3):
        thread = FileSystemThread(
            thread_id=f"HP-{i+1}",
            filesystem=filesystem,
            priority=1,
            access_count=20
        )
        threads.append(thread)
    
    # Medium priority threads (3-5)
    for i in range(4):
        thread = FileSystemThread(
            thread_id=f"MP-{i+1}",
            filesystem=filesystem,
            priority=3,
            access_count=10
        )
        threads.append(thread)
    
    # Low priority threads (6-10)
    for i in range(5):
        thread = FileSystemThread(
            thread_id=f"LP-{i+1}",
            filesystem=filesystem,
            priority=9,
            access_count=8
        )
        threads.append(thread)
    
    # Start all threads
    start_time = time.time()
    for thread in threads:
        thread.start()
    
    # Run for specified duration
    time.sleep(duration)
    
    # Collect statistics
    active_threads = sum(1 for thread in threads if thread.is_alive())
    completed_threads = sum(1 for thread in threads if not thread.is_alive())
    
    # Print statistics so far
    logging.info(f"\n----- SIMULATION STATISTICS AFTER {duration} SECONDS -----")
    logging.info(f"Active threads: {active_threads}, Completed threads: {completed_threads}")
    
    # Group threads by priority class
    high_priority = [t for t in threads if t.priority <= 2]
    medium_priority = [t for t in threads if 2 < t.priority <= 5]
    low_priority = [t for t in threads if t.priority > 5]
    
    # Calculate statistics by priority group
    def calculate_group_stats(group, name):
        if not group:
            return
        
        total_accesses = sum(t.successful_accesses for t in group)
        avg_wait = sum(t.total_wait_time for t in group) / max(total_accesses, 1)
        
        logging.info(f"{name} Priority Group:")
        logging.info(f"  - Total successful accesses: {total_accesses}")
        logging.info(f"  - Average wait time: {avg_wait:.2f} seconds")
        for t in group:
            logging.info(f"  - Thread {t.thread_id}: {t.successful_accesses} accesses, "
                        f"avg wait {(t.total_wait_time / max(t.successful_accesses, 1)):.2f}s")
    
    calculate_group_stats(high_priority, "High")
    calculate_group_stats(medium_priority, "Medium")
    calculate_group_stats(low_priority, "Low")
    
    # Visualize execution timeline
    filesystem.visualize_execution(threads)
    
    # Calculate starvation metrics
    starvation_metrics = {}
    for group_name, group in [("High", high_priority), ("Medium", medium_priority), ("Low", low_priority)]:
        completion_rate = sum(t.successful_accesses for t in group) / sum(t.access_count for t in group)
        avg_wait = sum(t.total_wait_time for t in group) / max(sum(t.successful_accesses for t in group), 1)
        starvation_metrics[group_name] = {
            "completion_rate": completion_rate,
            "avg_wait": avg_wait
        }
    
    logging.info("\n----- STARVATION METRICS -----")
    for group, metrics in starvation_metrics.items():
        logging.info(f"{group} Priority Group:")
        logging.info(f"  - Task Completion Rate: {metrics['completion_rate']*100:.2f}%")
        logging.info(f"  - Average Wait Time: {metrics['avg_wait']:.2f}s")
    
    # Calculate resource domination
    total_events = len(filesystem.execution_history)
    group_access_counts = {"High": 0, "Medium": 0, "Low": 0}
    
    for event in filesystem.execution_history:
        if event['action'] == 'access':
            priority = event['priority']
            if priority <= 2:
                group_access_counts["High"] += 1
            elif priority <= 5:
                group_access_counts["Medium"] += 1
            else:
                group_access_counts["Low"] += 1
    
    logging.info("\n----- RESOURCE ACCESS DISTRIBUTION -----")
    for group, count in group_access_counts.items():
        if total_events > 0:
            percentage = (count / (total_events/2)) * 100  # Divide by 2 because each access has a corresponding release
            logging.info(f"{group} Priority Group: {count} accesses ({percentage:.2f}% of total)")
    
    # Gracefully terminate the simulation
    logging.info("\nSimulation complete. Waiting for remaining threads to finish...")
    for thread in threads:
        thread.join(timeout=2)
    
    # Count any threads that didn't complete their work
    starved_threads = sum(1 for t in threads if t.successful_accesses < t.access_count)
    logging.info(f"Threads that couldn't complete all accesses (likely starved): {starved_threads}")
    
    # Record exact starvation count by priority group
    starvation_by_group = {
        "High": sum(1 for t in high_priority if t.successful_accesses < t.access_count),
        "Medium": sum(1 for t in medium_priority if t.successful_accesses < t.access_count),
        "Low": sum(1 for t in low_priority if t.successful_accesses < t.access_count)
    }
    
    logging.info("\n----- STARVED THREADS BY PRIORITY -----")
    for group, count in starvation_by_group.items():
        group_size = len(locals()[f"{group.lower()}_priority"])
        if group_size > 0:
            starvation_percentage = (count / group_size) * 100
            logging.info(f"{group} Priority: {count}/{group_size} threads starved ({starvation_percentage:.2f}%)")


if __name__ == "__main__":
    logging.info("Starting file system starvation simulation...")
    # Note: You may need to install matplotlib: pip install matplotlib numpy
    run_simulation(duration=20)
    logging.info("Simulation ended.")