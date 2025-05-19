import threading
import time
import random
from datetime import datetime

# 공유 사전
shared_dict = {}
# 로그 저장 리스트
log_list = []

# 사전을 업데이트하는 스레드 함수
def update_dictionary(key, value):
    start_time = datetime.now()
    # 작업 전 랜덤 딜레이
    time.sleep(random.random())
    original_value = shared_dict.get(key, None)
    shared_dict[key] = value
    end_time = datetime.now()

    # 로그 저장
    log_entry = {
        'thread': threading.current_thread().name,
        'key': key,
        'original_value': original_value,
        'new_value': value,
        'start_time': start_time.strftime('%Y-%m-%d %H:%M:%S.%f'),
        'end_time': end_time.strftime('%Y-%m-%d %H:%M:%S.%f'),
        'race_condition': original_value is not None and original_value != value
    }
    log_list.append(log_entry)
    print(f"스레드 {threading.current_thread().name} end: {key} = {value}, start: {log_entry['start_time']}, terminated: {log_entry['end_time']}")

# 스레드를 생성하고 실행
threads = []
for i in range(10):
    key = 'test'
    value = random.randint(1, 100)
    thread = threading.Thread(target=update_dictionary, args=(key, value))
    thread.start()
    threads.append(thread)

# 모든 스레드가 종료될 때까지 대기
for thread in threads:
    thread.join()

print("최종 사전 내용:", shared_dict)

# 로그 출력
print("\n스레드 로그:")
for log in log_list:
    race_condition = "data race!" if log['race_condition'] else "no data race."
    print(f"{log['thread']}: {log['key']} was {log['original_value']} -> {log['new_value']}, {race_condition}")
