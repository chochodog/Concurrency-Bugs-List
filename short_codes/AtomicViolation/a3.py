import multiprocessing

def increment(shared_number):
    for _ in range(1000):
        shared_number.value += 1

def decrement(shared_number):
    for _ in range(1000):
        shared_number.value -= 1

if __name__ == '__main__':
    shared_number = multiprocessing.Value('i', 0)

    p1 = multiprocessing.Process(target=increment, args=(shared_number,))
    p2 = multiprocessing.Process(target=decrement, args=(shared_number,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print(f"The final value of shared_number is {shared_number.value}")
