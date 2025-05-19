import threading
import time
import random
import logging
from datetime import datetime
from enum import Enum
from collections import defaultdict
from queue import Queue

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(message)s'
)

class SeatStatus(Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    BOOKED = "booked"

class BookingError(Exception):
    pass

class Seat:
    def __init__(self, seat_id):
        self.seat_id = seat_id
        self.status = SeatStatus.AVAILABLE
        self.customer_id = None
        self.booking_time = None
        self.price = random.uniform(50, 200)

class Customer:
    def __init__(self, customer_id, name, budget):
        self.customer_id = customer_id
        self.name = name
        self.budget = budget
        self.booked_seats = []
        self.booking_attempts = 0
        self.successful_bookings = 0

class TicketBookingSystem:
    def __init__(self, total_seats):
        self.seats = {i: Seat(i) for i in range(1, total_seats + 1)}
        self.booking_history = []
        self.revenue = 0
        self.failed_bookings = 0
        self.customer_stats = defaultdict(lambda: {"attempts": 0, "successes": 0})
        self.notifications_queue = Queue()
        
    def get_seat_status(self):
        status_count = defaultdict(int)
        for seat in self.seats.values():
            status_count[seat.status] += 1
        return dict(status_count)
    
    def get_available_seats(self):
        return [seat_id for seat_id, seat in self.seats.items() 
                if seat.status == SeatStatus.AVAILABLE]
    
    def calculate_total_cost(self, seat_ids):
        return sum(self.seats[seat_id].price for seat_id in seat_ids)
    
    def check_seat_availability(self, seat_ids):
        return all(
            self.seats[seat_id].status == SeatStatus.AVAILABLE 
            for seat_id in seat_ids
        )
    
    def process_payment(self, customer, total_cost):
        time.sleep(random.uniform(0.1, 0.3))
        if customer.budget >= total_cost:
            customer.budget -= total_cost
            self.revenue += total_cost
            return True
        return False
    
    def log_booking_attempt(self, customer_id, seat_ids, success):
        timestamp = datetime.now()
        self.booking_history.append({
            "timestamp": timestamp,
            "customer_id": customer_id,
            "seat_ids": seat_ids,
            "success": success
        })
        
        if not success:
            self.failed_bookings += 1
    
    def notify_customer(self, customer_id, message):
        self.notifications_queue.put((customer_id, message))
    
    def book_seats(self, seat_ids, customer):
        logging.info(f"Customer {customer.name} attempting to book seats {seat_ids}")
        customer.booking_attempts += 1
        self.customer_stats[customer.customer_id]["attempts"] += 1
        
        try:
            if not self.check_seat_availability(seat_ids):
                raise BookingError("Some seats are not available")
            
            total_cost = self.calculate_total_cost(seat_ids)
            time.sleep(random.uniform(0.2, 0.5))
            
            if not self.process_payment(customer, total_cost):
                raise BookingError("Insufficient funds")
            
            for seat_id in seat_ids:
                seat = self.seats[seat_id]
                seat.status = SeatStatus.BOOKED
                seat.customer_id = customer.customer_id
                seat.booking_time = datetime.now()
                customer.booked_seats.append(seat_id)
            
            customer.successful_bookings += 1
            self.customer_stats[customer.customer_id]["successes"] += 1
            
            self.notify_customer(
                customer.customer_id,
                f"Successfully booked seats {seat_ids} for ${total_cost:.2f}"
            )
            
            logging.info(
                f"Customer {customer.name} successfully booked seats {seat_ids} "
                f"for ${total_cost:.2f}"
            )
            
            self.log_booking_attempt(customer.customer_id, seat_ids, True)
            return True
            
        except BookingError as e:
            self.notify_customer(customer.customer_id, f"Booking failed: {str(e)}")
            logging.warning(
                f"Customer {customer.name} failed to book seats {seat_ids}: {str(e)}"
            )
            self.log_booking_attempt(customer.customer_id, seat_ids, False)
            return False

def customer_booking_process(booking_system, customer, num_seats):
    """Simulate customer booking behavior"""
    while True:
        available_seats = booking_system.get_available_seats()
        if len(available_seats) < num_seats:
            logging.info(f"Customer {customer.name} cannot find enough seats")
            break
            
        selected_seats = random.sample(available_seats, num_seats)
        
        booking_system.book_seats(selected_seats, customer)
        

        time.sleep(random.uniform(0.5, 1.5))

def notification_processor(booking_system):
    """Process customer notifications"""
    while True:
        customer_id, message = booking_system.notifications_queue.get()
        logging.info(f"Notification to customer {customer_id}: {message}")
        time.sleep(0.1)

def generate_booking_report(booking_system):
    """Generate a summary report of booking activity"""
    status_count = booking_system.get_seat_status()
    
    print("\n=== Booking System Report ===")
    print(f"Total Revenue: ${booking_system.revenue:.2f}")
    print(f"Failed Bookings: {booking_system.failed_bookings}")
    print("\nSeat Status:")
    for status, count in status_count.items():
        print(f"  {status.value}: {count}")
        
    print("\nCustomer Statistics:")
    for customer_id, stats in booking_system.customer_stats.items():
        success_rate = (stats["successes"] / stats["attempts"] * 100 
                       if stats["attempts"] > 0 else 0)
        print(f"Customer {customer_id}:")
        print(f"  Attempts: {stats['attempts']}")
        print(f"  Successes: {stats['successes']}")
        print(f"  Success Rate: {success_rate:.1f}%")

def main():
    booking_system = TicketBookingSystem(20)
    
    customers = [
        Customer(i, f"Customer_{i}", random.uniform(300, 1000))
        for i in range(10)
    ]
    
    notification_thread = threading.Thread(
        target=notification_processor,
        args=(booking_system,),
        daemon=True
    )
    notification_thread.start()
    
    threads = []
    for customer in customers:
        thread = threading.Thread(
            target=customer_booking_process,
            args=(booking_system, customer, random.randint(2, 4))
        )
        threads.append(thread)
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()
    
    generate_booking_report(booking_system)

if __name__ == "__main__":
    main()
    
