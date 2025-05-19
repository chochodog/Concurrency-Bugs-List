import multiprocessing
import time

def increment(shared_list, index):
    for _ in range(100):
        time.sleep(0.01)
        shared_list[index] += 1

def decrement(shared_list, index):
    for _ in range(100):
        time.sleep(0.01)
        shared_list[index] -= 1

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    shared_list = manager.list([0])


    processes = []
    for _ in range(5):
        p_inc = multiprocessing.Process(target=increment, args=(shared_list, 0))
        p_dec = multiprocessing.Process(target=decrement, args=(shared_list, 0))
        processes.append(p_inc)
        processes.append(p_dec)


    for p in processes:
        p.start()

    # 프로세스 종료 대기
    for p in processes:
        p.join()

    # 최종 결과 출력
    print(f"The final state of the first element in the shared_list is {shared_list[0]}")
