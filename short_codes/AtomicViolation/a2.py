import multiprocessing

def list_append(shared_list, value, index):
    for _ in range(100000):
        shared_list[index] += value

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    shared_list = manager.list([0])  # 초기 값이 0인 공유 리스트

    # 프로세스 생성
    process1 = multiprocessing.Process(target=list_append, args=(shared_list, 1, 0))
    process2 = multiprocessing.Process(target=list_append, args=(shared_list, -1, 0))

    # 프로세스 시작
    process1.start()
    process2.start()

    # 프로세스가 종료될 때까지 기다림
    process1.join()
    process2.join()

    # 최종 결과 출력
    print(f"The final value of the first item in the shared_list is {shared_list[0]}")
