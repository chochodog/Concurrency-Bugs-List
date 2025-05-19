import multiprocessing
import time

def increment_counter(counter, iterations):
    for _ in range(iterations):
        value = counter.value
        time.sleep(0.0001)
        counter.value = value + 1

if __name__ == "__main__":
    shared_counter = multiprocessing.Value('i', 0)
    iterations = 100
    
    process1 = multiprocessing.Process(
        target=increment_counter, 
        args=(shared_counter, iterations)
    )
    process2 = multiprocessing.Process(
        target=increment_counter, 
        args=(shared_counter, iterations)
    )

    process1.start()
    process2.start()
    process1.join()
    process2.join()
    

    print(f"Final counter value: {shared_counter.value}")
    print(f"Expected counter value: {iterations * 2}")
