import multiprocessing

def list_append(shared_list, value, index):
    for _ in range(100000):
        shared_list[index] += value

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    shared_list = manager.list([0])

    process1 = multiprocessing.Process(target=list_append, args=(shared_list, 1, 0))
    process2 = multiprocessing.Process(target=list_append, args=(shared_list, -1, 0))
    process1.start()
    process2.start()

    process1.join()
    process2.join()

    print(f"The final value of the first item in the shared_list is {shared_list[0]}")
