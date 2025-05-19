import random

def packet_simulation():
    # Create packets to be sent (in order)
    packet_count = 10
    original_packets = [(i, f"Data_{i}") for i in range(1, packet_count + 1)]
    
    print("Original packet order:")
    for seq, data in original_packets:
        print(f"Packet {seq}: {data}")
    
    # Simulate packet shuffling during network transmission
    transmitted_packets = original_packets.copy()
    random.shuffle(transmitted_packets)
    
    print("\nPackets received out of order on the network:")
    for seq, data in transmitted_packets:
        print(f"Packet {seq}: {data} (original order: {seq})")
    
    # Simulate reception and reordering
    receive_buffer = {}
    expected_seq = 1
    final_received_data = []
    
    print("\nReceiving process simulation:")
    for seq, data in transmitted_packets:
        print(f"Received packet: {seq}", end="")
        if seq > expected_seq:
            print(f"  ⚠ Out-of-order packet detected! (expected: {expected_seq})")
        else:
            print()
        receive_buffer[seq] = data
        
        # Check if the expected packet has arrived
        while expected_seq in receive_buffer:
            data = receive_buffer.pop(expected_seq)
            final_received_data.append((expected_seq, data))
            print(f"  > Packet {expected_seq} processed")
            expected_seq += 1
    
    print("\nFinal reordered data:")
    for seq, data in final_received_data:
        print(f"Packet {seq}: {data}")
    
    # Remaining packets in buffer (not yet processable due to missing earlier packets)
    if receive_buffer:
        print("\nUnprocessed packets (due to order violation):")
        for seq, data in sorted(receive_buffer.items()):
            print(f"Packet {seq}: {data}")

packet_simulation()
