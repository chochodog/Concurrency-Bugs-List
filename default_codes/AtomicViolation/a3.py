import threading
import time
import random
from tabulate import tabulate
import sys

class Theater:
    def __init__(self, rows=5, seats_per_row=10):
        self.seating = {}
        for row in range(1, rows + 1):
            for seat in range(1, seats_per_row + 1):
                seat_id = f"{chr(64+row)}{seat}"
                self.seating[seat_id] = True
        
        self.bookings = {}
        self.booking_attempts = {}
        
    def is_seat_available(self, seat_id):
        return self.seating.get(seat_id, False)
    
    def reserve_seat_unsafe(self, seat_id, user_id):
        """
        Unsafe reservation function with NO synchronization - vulnerable to atomic violations
        This simulates a real-world scenario where a database record is:
        1. Checked for availability 
        2. Then updated in separate operations
        """
        if seat_id not in self.booking_attempts:
            self.booking_attempts[seat_id] = []
        self.booking_attempts[seat_id].append(user_id)
        
        if self.is_seat_available(seat_id):
            time.sleep(random.uniform(0.01, 0.05))
            self.seating[seat_id] = False
            self.bookings[seat_id] = user_id
            return True
        return False
    
    def display_seating_chart(self):
        """Displays the seating chart and booking information"""
        rows = {}
        for seat_id in self.seating:
            row = seat_id[0]
            if row not in rows:
                rows[row] = []
            status = "BOOKED" if not self.seating[seat_id] else "Available"
            booker = f" by User-{self.bookings.get(seat_id)}" if seat_id in self.bookings else ""
            rows[row].append(f"{seat_id}: {status}{booker}")
        
        for row in sorted(rows.keys()):
            print(f"Row {row}: {', '.join(rows[row])}")
    
    def analyze_booking_attempts(self):
        """Analyze and display booking attempts and conflicts"""
        conflicts = []
        
        for seat_id, attempts in self.booking_attempts.items():
            if len(attempts) > 1:
                booked_by = self.bookings.get(seat_id, "None")
                conflicts.append([
                    seat_id,
                    len(attempts),
                    ", ".join([str(u) for u in attempts]),
                    booked_by
                ])
        
        if conflicts:
            print("\n=== BOOKING CONFLICTS DETECTED ===")
            print(tabulate(
                conflicts,
                headers=["Seat", "# Attempts", "Attempted by Users", "Actually Booked by"],
                tablefmt="grid"
            ))
            
            double_bookings = {}
            for seat_id, booker in self.bookings.items():
                if seat_id not in double_bookings:
                    double_bookings[seat_id] = set()
                double_bookings[seat_id].add(booker)
            
            multi_booked = [seat for seat, bookers in double_bookings.items() if len(bookers) > 1]
            if multi_booked:
                print(f"\n⚠️ CRITICAL ERROR: {len(multi_booked)} seats have multiple bookers!")
                for seat in multi_booked:
                    print(f"  - Seat {seat} was double-booked by users: {double_bookings[seat]}")
        else:
            print("\nNo booking conflicts detected.")


def simulate_user(theater, user_id, target_seats):
    """Simulate a user trying to book one of several preferred seats"""
    for seat_id in target_seats:
        success = theater.reserve_seat_unsafe(seat_id, user_id)
        if success:
            print(f"User-{user_id} successfully booked seat {seat_id}")
            break
        else:
            print(f"User-{user_id} failed to book seat {seat_id}, trying another...")
    else:
        print(f"User-{user_id} couldn't book any of their preferred seats")


def main():
    print("=== DEMONSTRATING ATOMIC VIOLATION IN TICKET BOOKING SYSTEM ===")
    
    theater = Theater(rows=5, seats_per_row=10)
    
    users = [
        (1, ["A1", "A2", "A3"]),
        (2, ["A1", "B1", "C1"]),
        (3, ["A1", "A2", "B2"]),
        (4, ["B1", "B2", "B3"]),
        (5, ["C1", "C2", "C3"]),
        (6, ["A3", "B3", "C3"]),
        (7, ["D1", "D2", "D3"]),
        (8, ["E1", "E2", "E3"]),
    ]
    
    threads = []
    for user_id, preferred_seats in users:
        thread = threading.Thread(
            target=simulate_user,
            args=(theater, user_id, preferred_seats)
        )
        threads.append(thread)
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print("\n=== FINAL SEATING CHART ===")
    theater.display_seating_chart()
    
    # Analyze booking attempts to see if we had race conditions
    theater.analyze_booking_attempts()


if __name__ == "__main__":
    main()
