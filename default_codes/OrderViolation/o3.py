import asyncio
import time
import random

# 데이터 준비 여부를 추적하는 글로벌 변수
data_ready = False

async def fetch_data():
    global data_ready
    start_time = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] [Fetcher] Fetching data...")

    # 20% 확률로 fetch_data()가 늦게 실행되도록 설계
    if random.random() < 0.2:
        print(f"[{time.strftime('%H:%M:%S')}] [Fetcher] ⚠️ Random delay occurred!")
        await asyncio.sleep(3)  # 일부러 3초 동안 늦춤
    else:
        await asyncio.sleep(2)  # 정상적인 2초 지연

    end_time = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] [Fetcher] Data fetched in {end_time - start_time:.2f} seconds")

    data_ready = True  # 데이터 준비 완료
    return "Server Response"

async def process_data():
    global data_ready
    print(f"[{time.strftime('%H:%M:%S')}] [Processor] Waiting to fetch data before processing...")

    start_time = time.time()
    
    # 10% 확률로 데이터 없이 바로 처리 시도 (순서 위반 유발)
    if random.random() < 0.1:
        print(f"[{time.strftime('%H:%M:%S')}] 🚨 [ERROR] Order Violation Detected! Trying to process data before fetching!")
        data = "Invalid Data"  # 잘못된 데이터 사용
    else:
        data = await fetch_data()  # 정상적으로 데이터 기다림
    
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
