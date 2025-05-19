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
            print(f"{self.name} try to pick left fort.")
            if self.left_fork.acquire(blocking=False):
                print(f"{self.name} pick left fork")
                time.sleep(0.1)
                
                print(f"{self.name} try to pick right fort.")
                if self.right_fork.acquire(blocking=False):
                    print(f"{self.name} pick right fork.")
                    print(f"{self.name} have a meal.")
                    time.sleep(0.5)
                    self.eaten = True
                    self.right_fork.release()
                    print(f"{self.name} drop right fork.")
                else:
                    print(f"{self.name} didn`t get right fork. he drop left fork.")
                    self.left_fork.release()
                    time.sleep(random.uniform(0.1, 0.3))
            else:
                print(f"{self.name} didn`t get left fork.")
                time.sleep(random.uniform(0.1, 0.3))
            
            attempts += 1
            
        if self.eaten:
            print(f"{self.name} end having meal successfully.")
        else:
            print(f"{self.name} didn`t have a meal. live lock detected!!!")

def simulate_livelock():
    fork1 = threading.Lock()
    fork2 = threading.Lock()
    
    philosopher1 = Philosopher("철학자1", fork1, fork2)
    philosopher2 = Philosopher("철학자2", fork2, fork1)
    
    t1 = threading.Thread(target=philosopher1.try_to_eat)
    t2 = threading.Thread(target=philosopher2.try_to_eat)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    if not philosopher1.eaten or not philosopher2.eaten:
        print("LIVE LOCK!!!")
    else:
        print("all people finished having a meal")

if __name__ == "__main__":
    print("simulation start")
    simulate_livelock()
    print("시뮬레이션 종료")
