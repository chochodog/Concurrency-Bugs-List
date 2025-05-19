import multiprocessing

def worker(conn):
    print("Worker: Waiting to receive data...")
    data = conn.recv()  # 부모 프로세스로부터 데이터를 기다림 (하지만 보내지 않음)
    print(f"Worker received: {data}")
    conn.send("ACK")  # 부모에게 응답 보냄
    conn.close()

if __name__ == "__main__":
    parent_conn, child_conn = multiprocessing.Pipe()

    p = multiprocessing.Process(target=worker, args=(child_conn,))
    p.start()

    print("Parent: Waiting to receive data from child...")
    msg = parent_conn.recv()  # 자식 프로세스의 응답을 기다리지만, 먼저 데이터를 보내지 않음 (데드락 발생)
    print(f"Parent received: {msg}")

    p.join()
