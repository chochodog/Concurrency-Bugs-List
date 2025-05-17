import threading
import time
import random

class NetworkNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.lock = threading.Lock()
        self.input_buffer = threading.Semaphore(1)
        self.output_buffer = threading.Semaphore(1)

class Packet(threading.Thread):
    def __init__(self, packet_id, route, deadlock_prob=0.2):
        threading.Thread.__init__(self)
        self.packet_id = packet_id
        self.route = route
        self.deadlock_prob = deadlock_prob

    def run(self):
        try:
            for i in range(len(self.route) - 1):
                current_node = self.route[i]
                next_node = self.route[i + 1]

                # Simulate high deadlock probability scenario
                if random.random() < self.deadlock_prob:
                    # Attempt to acquire both current and next node locks
                    current_node.lock.acquire()
                    time.sleep(random.uniform(0.1, 0.3))
                    next_node.lock.acquire()
                    print(f"Potential Deadlock: Packet {self.packet_id} locked nodes {current_node.node_id} and {next_node.node_id}")
                else:
                    # Normal routing with buffer semaphores
                    current_node.input_buffer.acquire()
                    next_node.output_buffer.acquire()
                    
                    current_node.lock.acquire()
                    next_node.lock.acquire()

                try:
                    print(f"Packet {self.packet_id} routing from node {current_node.node_id} to {next_node.node_id}")
                    time.sleep(random.uniform(0.1, 0.3))
                
                finally:
                    # Release locks
                    current_node.lock.release()
                    next_node.lock.release()
                    
                    current_node.input_buffer.release()
                    next_node.output_buffer.release()

        except Exception as e:
            print(f"Packet {self.packet_id} routing error: {e}")

def create_network_topology(num_nodes=6):
    return [NetworkNode(i) for i in range(num_nodes)]

def simulate_network_traffic(num_packets=30):
    network = create_network_topology()
    packets = []

    for i in range(num_packets):
        # Create routes with high potential for lock contention
        route = random.sample(network, random.randint(3, len(network)))
        packet = Packet(i, route)
        packets.append(packet)
        packet.start()

    for packet in packets:
        packet.join()

if __name__ == "__main__":
    simulate_network_traffic()