import threading
import time
import random

class Philosopher:
    def __init__(self, name, left_fork, right_fork):
        self.name = name
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.eaten = False
    
    def try_to_eat(self):
        attempts = 0
        while not self.eaten and attempts < 10:
            # 철학자가 포크를 집으려고 시도
            print(f"{self.name}이(가) 왼쪽 포크를 집으려고 합니다.")
            if self.left_fork.acquire(blocking=False):
                print(f"{self.name}이(가) 왼쪽 포크를 집었습니다.")
                time.sleep(0.1)  # 잠시 기다림
                
                print(f"{self.name}이(가) 오른쪽 포크를 집으려고 합니다.")
                if self.right_fork.acquire(blocking=False):
                    print(f"{self.name}이(가) 오른쪽 포크를 집었습니다.")
                    print(f"{self.name}이(가) 식사를 합니다.")
                    time.sleep(0.5)
                    self.eaten = True
                    self.right_fork.release()
                    print(f"{self.name}이(가) 오른쪽 포크를 내려놓았습니다.")
                else:
                    # 오른쪽 포크를 얻지 못했다면, 왼쪽 포크도 내려놓음 (여기서 라이브락 발생)
                    print(f"{self.name}이(가) 오른쪽 포크를 얻지 못했습니다. 왼쪽 포크를 내려놓습니다.")
                    self.left_fork.release()
                    time.sleep(random.uniform(0.1, 0.3))  # 무작위 시간 대기 (약간의 불규칙성)
            else:
                print(f"{self.name}이(가) 왼쪽 포크를 얻지 못했습니다.")
                time.sleep(random.uniform(0.1, 0.3))  # 무작위 시간 대기
            
            attempts += 1
            
        if self.eaten:
            print(f"{self.name}이(가) 성공적으로 식사를 마쳤습니다.")
        else:
            print(f"{self.name}이(가) 식사를 하지 못했습니다. 라이브락 상황!")

def simulate_livelock():
    # 두 포크 생성
    fork1 = threading.Lock()
    fork2 = threading.Lock()
    
    # 두 철학자 생성
    philosopher1 = Philosopher("철학자1", fork1, fork2)
    philosopher2 = Philosopher("철학자2", fork2, fork1)  # 주목: 포크 순서가 반대
    
    # 스레드 생성 및 시작
    t1 = threading.Thread(target=philosopher1.try_to_eat)
    t2 = threading.Thread(target=philosopher2.try_to_eat)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    if not philosopher1.eaten or not philosopher2.eaten:
        print("라이브락이 발생했습니다!")
    else:
        print("두 철학자 모두 식사를 마쳤습니다!")

if __name__ == "__main__":
    print("라이브락 시뮬레이션 시작")
    simulate_livelock()
    print("시뮬레이션 종료")