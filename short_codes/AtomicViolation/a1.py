import threading
import time

inventory = {"product_a": 2}
orders = []

def process_order(user_id, product_id, quantity):
    current_stock = inventory.get(product_id, 0)
    print(f"[user {user_id}] current stock : {current_stock}")
    time.sleep(0.1)
    
    if current_stock >= quantity:
        inventory[product_id] = current_stock - quantity
        orders.append(f"user {user_id} orders {product_id} {quantity}")
        print(f"[user {user_id}] order success! remained stock: {inventory[product_id]}")
        return True
    else:
        print(f"[user {user_id}] order fail: insufficient stock")
        return False

def simulate_concurrent_orders():
    threads = []
    
    for i in range(1, 4):
        thread = threading.Thread(target=process_order, args=(i, "product_a", 1))
        threads.append(thread)
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print("\n=== result ===")
    print(f"final stock: {inventory['product_a']}")
    print(f"total number of order: {len(orders)}")
    print("list of order:", orders)

if __name__ == "__main__":
    simulate_concurrent_orders()
