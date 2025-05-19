import asyncio
import time
import random

data_ready = False

async def fetch_data():
    global data_ready
    start_time = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] [Fetcher] Fetching data...")

    if random.random() < 0.2:
        print(f"[{time.strftime('%H:%M:%S')}] [Fetcher] ⚠️ Random delay occurred!")
        await asyncio.sleep(3)
    else:
        await asyncio.sleep(2)

    end_time = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] [Fetcher] Data fetched in {end_time - start_time:.2f} seconds")

    data_ready = True
    return "Server Response"

async def process_data():
    global data_ready
    print(f"[{time.strftime('%H:%M:%S')}] [Processor] Waiting to fetch data before processing...")

    start_time = time.time()
    

    if random.random() < 0.1:
        print(f"[{time.strftime('%H:%M:%S')}] 🚨 [ERROR] Order Violation Detected! Trying to process data before fetching!")
        data = "Invalid Data"
    else:
        data = await fetch_data()
    
    end_time = time.time()

    print(f"[{time.strftime('%H:%M:%S')}] [Processor] Processed data: {data}")
    print(f"[{time.strftime('%H:%M:%S')}] [Processor] Processing took {end_time - start_time:.2f} seconds")

async def check_execution_order():
    print(f"[{time.strftime('%H:%M:%S')}] [Checker] Checking execution order...")
    start_time = time.time()
    await process_data()
    end_time = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] [Checker] Execution completed in {end_time - start_time:.2f} seconds")

asyncio.run(check_execution_order())
