import threading
import time
import random

# 공유 데이터
data = {}

def initialize_data():
    global data
    # 항상 일정한 지연을 주어 데이터를 초기화
    time.sleep(1)  # 데이터 초기화에 시간이 걸린다고 가정
    data['key'] = 'value'
    print("Data initialized.")

def process_data():
    global data
    # 10% 확률로 지연 없이 실행
    if random.random() < 0.1:
        time.sleep(0)  # 지연 없음
    else:
        # 나머지 90%의 경우에는 충분한 지연을 줌
        time.sleep(2)
    if 'key' in data:
        print(f"Processing data: {data['key']}")
    else:
        print("Data not ready.")

# 스레드 생성
t1 = threading.Thread(target=process_data)
t2 = threading.Thread(target=initialize_data)

# 스레드 시작
t1.start()
t2.start()

# 스레드 종료 대기
t1.join()
t2.join()
