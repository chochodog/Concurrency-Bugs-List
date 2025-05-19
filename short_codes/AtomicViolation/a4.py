import multiprocessing
import time

def increment(shared_list, index):
    for _ in range(100):
        time.sleep(0.01)  # 다른 프로세스가 접근할 수 있는 시간 제공
        shared_list[index] += 1

def decrement(shared_list, index):
    for _ in range(100):
        time.sleep(0.01)  # 다른 프로세스가 접근할 수 있는 시간 제공
        shared_list[index] -= 1

if __name__ == '__main__':
    # 멀티프로세싱 매니저를 통해 공유 리스트 생성
    manager = multiprocessing.Manager()
    shared_list = manager.list([0])

    # 프로세스 생성
    processes = []
    for _ in range(5):  # 5개의 증가 프로세스와 5개의 감소 프로세스 생성
        p_inc = multiprocessing.Process(target=increment, args=(shared_list, 0))
        p_dec = multiprocessing.Process(target=decrement, args=(shared_list, 0))
        processes.append(p_inc)
        processes.append(p_dec)

    # 프로세스 시작
    for p in processes:
        p.start()

    # 프로세스 종료 대기
    for p in processes:
        p.join()

    # 최종 결과 출력
    print(f"The final state of the first element in the shared_list is {shared_list[0]}")
