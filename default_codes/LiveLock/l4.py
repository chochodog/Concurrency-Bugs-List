import threading
import time
import random
from enum import Enum
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('RobotSimulation')

class ResourceType(Enum):
    CHARGER = "Charging Station"
    TOOL = "Tool"
    WORKSTATION = "Workstation"

class Resource:
    def __init__(self, resource_id, resource_type):
        self.id = resource_id
        self.type = resource_type
        self.lock = threading.Lock()
        self.owner = None
        self.requested_by = []
    
    def try_acquire(self, robot):
        """Attempt to acquire the resource without blocking"""
        if self.lock.acquire(blocking=False):
            self.owner = robot
            logger.info(f"Robot {robot.id} acquired {self.type.value} {self.id}")
            return True
        else:
            if robot not in self.requested_by:
                self.requested_by.append(robot)
            logger.info(f"Robot {robot.id} waiting for {self.type.value} {self.id} (owned by Robot {self.owner.id if self.owner else 'None'})")
            return False
    
    def release(self, robot):
        """Release the resource if owned by the robot"""
        if self.owner == robot:
            self.owner = None
            if robot in self.requested_by:
                self.requested_by.remove(robot)
            self.lock.release()
            logger.info(f"Robot {robot.id} released {self.type.value} {self.id}")
            return True
        return False
    
    def __str__(self):
        return f"{self.type.value} {self.id}"

class Robot:
    def __init__(self, robot_id, resources_needed):
        self.id = robot_id
        self.resources_needed = resources_needed  # List of resources this robot needs
        self.resources_held = []
        self.status = "idle"
        self.last_progress_time = time.time()
        self.give_up_resource_probability = 0.0  # Probability to give up a resource to break livelock
    
    def run(self):
        """Main robot operation loop"""
        while True:
            # Try to acquire all needed resources
            all_acquired = True
            
            # First, check if we should release a resource to potentially break livelock
            if random.random() < self.give_up_resource_probability and self.resources_held:
                resource = random.choice(self.resources_held)
                logger.warning(f"Robot {self.id} strategically releasing {resource} to avoid livelock")
                resource.release(self)
                self.resources_held.remove(resource)
                time.sleep(random.uniform(0.5, 1.5))  # Wait a bit after releasing
                
            # Try to acquire all needed resources
            for resource in self.resources_needed:
                if resource not in self.resources_held:
                    if resource.try_acquire(self):
                        self.resources_held.append(resource)
                        self.last_progress_time = time.time()
                    else:
                        all_acquired = False
            
            # If all resources acquired, perform work
            if all_acquired and len(self.resources_held) == len(self.resources_needed):
                old_status = self.status
                self.status = "working"
                if old_status != "working":
                    logger.info(f"Robot {self.id} is now working with all required resources")
                self.last_progress_time = time.time()
                time.sleep(random.uniform(0.5, 2.0))  # Simulating work
                
                # Release all resources after work is done
                for resource in self.resources_held.copy():
                    resource.release(self)
                    self.resources_held.remove(resource)
                
                self.status = "idle"
                logger.info(f"Robot {self.id} completed work cycle and released all resources")
                time.sleep(random.uniform(0.2, 1.0))  # Rest between work cycles
            else:
                self.status = "waiting"
                time.sleep(0.1)  # Small wait while trying to acquire resources

class LivelockMonitor:
    def __init__(self, robots, livelock_threshold=5.0):
        self.robots = robots
        self.livelock_threshold = livelock_threshold
        self.livelock_detected = False
    
    def check_for_livelock(self):
        """Checks if all robots have been waiting without progress for longer than the threshold"""
        current_time = time.time()
        all_waiting = True
        all_exceeded_threshold = True
        
        for robot in self.robots:
            if robot.status != "waiting":
                all_waiting = False
                break
            
            time_since_progress = current_time - robot.last_progress_time
            if time_since_progress < self.livelock_threshold:
                all_exceeded_threshold = False
        
        if all_waiting and all_exceeded_threshold and not self.livelock_detected:
            self.livelock_detected = True
            logger.critical("LIVELOCK DETECTED: All robots are waiting for resources held by other robots")
            self._print_dependency_chain()
            return True
        
        # Reset livelock detection if robots aren't all waiting
        if not all_waiting:
            self.livelock_detected = False
            
        return False
    
    def _print_dependency_chain(self):
        """Prints the circular dependency chain that caused the livelock"""
        dependency_messages = []
        for robot in self.robots:
            waiting_for = []
            for resource in robot.resources_needed:
                if resource not in robot.resources_held and resource.owner:
                    waiting_for.append(f"{resource} (held by Robot {resource.owner.id})")
            
            holding = [str(resource) for resource in robot.resources_held]
            
            dependency_messages.append(
                f"Robot {robot.id} holds [{', '.join(holding)}] and waits for [{', '.join(waiting_for)}]"
            )
        
        logger.critical("Dependency Chain:")
        for msg in dependency_messages:
            logger.critical(msg)
    
    def run(self):
        """Run the livelock detection loop"""
        while True:
            self.check_for_livelock()
            time.sleep(1.0)  # Check for livelock every second

def introduce_livelock_condition(robots):
    """Adjust robot behaviors to increase livelock probability"""
    for robot in robots:
        # Start with zero probability
        robot.give_up_resource_probability = 0.0

def livelock_resolution_strategy(robots):
    """Implement a strategy to resolve the livelock after detection"""
    logger.warning("Activating livelock resolution strategy")
    # Increase the probability that robots will release resources
    for robot in robots:
        robot.give_up_resource_probability = 0.3
    return True

def simulate_production_line(duration=60):
    """Set up and run the simulation"""
    # Create shared resources
    charger1 = Resource(1, ResourceType.CHARGER)
    charger2 = Resource(2, ResourceType.CHARGER)
    tool1 = Resource(1, ResourceType.TOOL)
    tool2 = Resource(2, ResourceType.TOOL)
    workstation = Resource(1, ResourceType.WORKSTATION)
    
    # Create robots with cyclical dependencies to encourage livelock
    # Robot 1 needs charger1 and tool1
    # Robot 2 needs charger1 and tool2
    # Robot 3 needs charger2 and tool1
    # This creates potential for cyclic waiting
    
    robot1 = Robot(1, [charger1, tool1, workstation])
    robot2 = Robot(2, [charger1, tool2, workstation])
    robot3 = Robot(3, [charger2, tool1, workstation])
    
    robots = [robot1, robot2, robot3]
    
    # Create monitor
    monitor = LivelockMonitor(robots)
    
    # Start robot threads
    threads = []
    for robot in robots:
        thread = threading.Thread(target=robot.run)
        thread.daemon = True
        threads.append(thread)
        thread.start()
    
    # Start monitor thread
    monitor_thread = threading.Thread(target=monitor.run)
    monitor_thread.daemon = True
    monitor_thread.start()
    
    # Create a flag to track if we've introduced the livelock resolution
    resolution_introduced = False
    
    # Introduce conditions that make livelock more likely
    introduce_livelock_condition(robots)
    
    # Run simulation for specified duration
    start_time = time.time()
    while time.time() - start_time < duration:
        if monitor.livelock_detected and not resolution_introduced:
            # Wait 5 seconds to observe the livelock before resolving
            time.sleep(5)
            resolution_introduced = livelock_resolution_strategy(robots)
        time.sleep(0.5)
    
    logger.info("Simulation completed")

if __name__ == "__main__":
    logger.info("Starting robot production line simulation")
    simulate_production_line(duration=120)  # Run for 2 minutes