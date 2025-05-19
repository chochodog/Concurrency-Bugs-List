import threading
import time
import queue
import random
from enum import Enum
from dataclasses import dataclass

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

@dataclass
class Message:
    sender: str
    recipient: str
    priority: Priority
    content: str
    timestamp: float = 0.0
    
    # Add a unique ID to ensure messages are always comparable
    id: int = 0

# Counter for generating unique message IDs
message_counter = 0

class MessageQueue:
    def __init__(self, name):
        self.name = name
        self.queue = queue.PriorityQueue()
        self.lock = threading.Lock()
    
    def enqueue(self, message):
        """Add a message to the queue with priority (lower number = higher priority)"""
        global message_counter
        message.timestamp = time.time()
        message.id = message_counter
        message_counter += 1
        
        # Invert priority for PriorityQueue (which puts lowest values first)
        priority_value = 10 - message.priority.value
        with self.lock:
            # Use a tuple with message ID as secondary sort key
            self.queue.put((priority_value, message.id, message))
    
    def dequeue(self):
        """Get the highest priority message from the queue"""
        try:
            with self.lock:
                if not self.queue.empty():
                    _, _, message = self.queue.get(block=False)
                    return message
                return None
        except queue.Empty:
            return None
    
    def size(self):
        return self.queue.qsize()

class System:
    def __init__(self, name, message_policy):
        """
        Initialize a system that processes messages according to a policy.
        
        Args:
            name: System identifier
            message_policy: Function that determines if a message can be processed
        """
        self.name = name
        self.inbox = MessageQueue(f"{name}_inbox")
        self.message_policy = message_policy
        self.last_processed_time = time.time()
        self.is_running = True
        self.messages_sent = 0
        self.messages_processed = 0
        self.blocked_count = 0
        self.can_receive_high_priority = True
    
    def send_message(self, recipient_queue, priority, content):
        """Send a message to another system's queue"""
        message = Message(self.name, recipient_queue.name.split('_')[0], priority, content)
        recipient_queue.enqueue(message)
        print(f"[{self.name}] Sent {priority.name} priority message to {message.recipient}: {content}")
        self.messages_sent += 1
    
    def process_messages(self):
        """Process messages from the inbox according to policy"""
        while self.is_running:
            message = self.inbox.dequeue()
            if message:
                # Check if this message can be processed according to policy
                if self.message_policy(self, message):
                    print(f"[{self.name}] Processing {message.priority.name} priority message from {message.sender}: {message.content}")
                    self.last_processed_time = time.time()
                    self.messages_processed += 1
                    # Small delay to simulate processing
                    time.sleep(0.1)
                else:
                    # Re-queue the message if it can't be processed now
                    self.inbox.enqueue(message)
                    wait_time = round(time.time() - message.timestamp, 2)
                    self.blocked_count += 1
                    print(f"[{self.name}] BLOCKED {message.priority.name} message from {message.sender} (waiting {wait_time}s): {message.content}")
                    # Small delay before trying again
                    time.sleep(0.1)
            else:
                # No messages to process
                time.sleep(0.1)

def system_a_policy(system, message):
    """
    System A's message processing policy:
    - Will only process LOW priority messages if it has recently processed a HIGH priority one
    """
    if message.priority == Priority.HIGH:
        # System A can always process high priority messages
        system.can_receive_high_priority = False
        return True
    elif message.priority == Priority.LOW:
        # System A will only process low priority messages if it recently processed a high priority one
        return not system.can_receive_high_priority
    return True  # Process all other message types

def system_b_policy(system, message):
    """
    System B's message processing policy:
    - Will only process HIGH priority messages if it has recently processed a LOW priority one
    """
    if message.priority == Priority.LOW:
        # System B can always process low priority messages
        system.can_receive_high_priority = True
        return True
    elif message.priority == Priority.HIGH:
        # System B will only process high priority messages if it recently processed a low priority one
        return system.can_receive_high_priority
    return True  # Process all other message types

def detect_livelock(systems, timeout=5):
    """
    Detect if systems are in a livelock by monitoring processing activity
    """
    while True:
        all_stuck = True
        
        for system in systems:
            time_since_last_processed = time.time() - system.last_processed_time
            
            if time_since_last_processed < timeout:
                all_stuck = False
                break
            
            # Check if there are pending messages (indicating potential livelock)
            if system.inbox.size() > 0 and system.blocked_count > 10:
                print(f"\n[LIVELOCK DETECTION] {system.name} has pending messages but hasn't processed any in {round(time_since_last_processed, 2)}s")
            else:
                all_stuck = False
        
        if all_stuck:
            print("\n===== LIVELOCK DETECTED =====")
            print("All systems have been inactive with pending messages for over 5 seconds.")
            print("Systems are actively working (trying to process messages) but not making progress.")
            for system in systems:
                print(f"{system.name}: Sent {system.messages_sent}, Processed {system.messages_processed}, Blocked {system.blocked_count}")
            print("===============================\n")
            # After detecting livelock, wait before checking again
            time.sleep(5)
            
        time.sleep(1)

def simulate_communication(system_a, system_b):
    """Simulate the communication pattern that leads to livelock"""
    while True:
        # System A sends HIGH priority message to System B
        system_a.send_message(system_b.inbox, Priority.HIGH, "Important request from A")
        
        # System B sends LOW priority message to System A
        system_b.send_message(system_a.inbox, Priority.LOW, "Regular update from B")
        
        # Wait before next communication cycle
        time.sleep(1)

def main():
    # Create the systems with their respective message processing policies
    system_a = System("SystemA", system_a_policy)
    system_b = System("SystemB", system_b_policy)
    
    # Start message processing threads
    process_a = threading.Thread(target=system_a.process_messages)
    process_b = threading.Thread(target=system_b.process_messages)
    
    # Start livelock detection
    detection_thread = threading.Thread(target=detect_livelock, args=([system_a, system_b],))
    
    # Start communication simulation
    comm_thread = threading.Thread(target=simulate_communication, args=(system_a, system_b))
    
    # Start all threads
    process_a.daemon = True
    process_b.daemon = True
    detection_thread.daemon = True
    comm_thread.daemon = True
    
    process_a.start()
    process_b.start()
    detection_thread.start()
    comm_thread.start()
    
    print("Simulation started. Press Ctrl+C to stop.")
    
    try:
        # Let the simulation run for a set time
        time.sleep(30)
        print("\nSimulation completed.")
        
        # Print statistics
        print(f"\nSystemA: Sent {system_a.messages_sent}, Processed {system_a.messages_processed}, Blocked {system_a.blocked_count}")
        print(f"SystemB: Sent {system_b.messages_sent}, Processed {system_b.messages_processed}, Blocked {system_b.blocked_count}")
        
    except KeyboardInterrupt:
        print("\nSimulation interrupted.")
    finally:
        # Cleanup
        system_a.is_running = False
        system_b.is_running = False

if __name__ == "__main__":
    main()