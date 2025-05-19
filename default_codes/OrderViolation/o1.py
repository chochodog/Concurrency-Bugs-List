import asyncio
import random
import time

class EventProcessor:
    def __init__(self):
        self.events = []
        self.results = []

    async def process_event(self, event_id, delay, start_order):
        # 이벤트 처리 준비 시간 기록
        prepare_time = time.time()
        # 지연 시간을 모방하여 비동기 대기
        await asyncio.sleep(delay)
        # 이벤트 처리 완료 시간 기록
        finish_time = time.time()
        # 결과 리스트에 이벤트 정보 추가
        self.results.append({
            'event_id': event_id,
            'prepare_time': prepare_time,
            'finish_time': finish_time,
            'start_order': start_order,
            'delay': delay
        })

    async def run_simulation(self, num_events=10):
        for i in range(num_events):
            delay = random.uniform(0.1, 1.0)  # 랜덤 지연 시간 설정
            event = self.process_event(i, delay, i)
            self.events.append(event)
        
        # 모든 이벤트를 비동기적으로 처리
        await asyncio.gather(*self.events)

        # 이벤트 결과를 종료 시간에 따라 정렬
        self.results.sort(key=lambda x: x['finish_time'])

        # 결과 출력
        self.display_results()

    def display_results(self):
        print("Event ID | Prepare Time | Finish Time | Original Order | Processed Order | Delay | Order Violation")
        processed_order = 0
        for result in self.results:
            order_violation = "Yes" if result['start_order'] != processed_order else "No"
            print(f"{result['event_id']:8} | {result['prepare_time']:13.4f} | {result['finish_time']:12.4f} | {result['start_order']:14} | {processed_order:15} | {result['delay']:5.2f} | {order_violation}")
            processed_order += 1

# 시뮬레이션 시작
processor = EventProcessor()
asyncio.run(processor.run_simulation())
