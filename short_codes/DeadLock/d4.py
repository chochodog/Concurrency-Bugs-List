import multiprocessing

def worker(conn):
    print("Worker: Waiting to receive data...")
    data = conn.recv()
    print(f"Worker received: {data}")
    conn.send("ACK")
    conn.close()

if __name__ == "__main__":
    parent_conn, child_conn = multiprocessing.Pipe()

    p = multiprocessing.Process(target=worker, args=(child_conn,))
    p.start()

    print("Parent: Waiting to receive data from child...")
    msg = parent_conn.recv()
    print(f"Parent received: {msg}")

    p.join()
