import threading
import time
import random

data = {}

def initialize_data():
    global data
    time.sleep(1)
    data['key'] = 'value'
    print("Data initialized.")

def process_data():
    global data
    if random.random() < 0.1:
        time.sleep(0)
    else:
        time.sleep(2)
    if 'key' in data:
        print(f"Processing data: {data['key']}")
    else:
        print("Data not ready.")

t1 = threading.Thread(target=process_data)
t2 = threading.Thread(target=initialize_data)

t1.start()
t2.start()

t1.join()
t2.join()
