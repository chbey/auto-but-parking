from datetime import datetime, time

class SmartCard:
    def __init__(self, balance):
        self.balance = balance

    def can_swipe_in(self):
        return self.balance >= 10  # Minimum balance of $10 required to swipe in

    def update_balance(self, fare):
        if self.balance >= fare:
            self.balance -= fare
        else:
            raise ValueError("Insufficient balance to exit the bus!")

class BusSystem:
    def __init__(self):
        self.stops = ["Stop" + str(i) for i in range(1, 16)]  # 15 stops

    def calculate_fare(self, swipe_in_time, swipe_in_day, start_stop, end_stop):
        number_of_stops_travelled = abs(end_stop - start_stop)
        fare_per_stop = self.get_fare_per_stop(swipe_in_time)

        # Basic fare calculation based on the number of stops travelled
        if number_of_stops_travelled > 5:
            discounted_stops = number_of_stops_travelled - 5
            fare = (5 * fare_per_stop) + (discounted_stops * fare_per_stop * 0.8)
        else:
            fare = number_of_stops_travelled * fare_per_stop
        
        # Apply weekend discount if necessary
        if swipe_in_day in ["Saturday", "Sunday"]:
            fare *= 0.9  # 10% weekend discount
        
        # Ensure the fare doesn't exceed the $10 cap
        return min(fare, 10.0)

    def get_fare_per_stop(self, swipe_in_time):
        night_time_start = time(23, 0)
        night_time_end = time(6, 0)

        # Determine if the travel time is during the night or day
        if night_time_start <= swipe_in_time or swipe_in_time <= night_time_end:
            return 0.60  # Night time fare
        else:
            return 0.80  # Day time fare

# Example Usage
def main():
    print("------------------Bus Smart Card System----------------------------")
    print()
    # Keep prompting for the balance until it's at least $10
    while True:
        balance = float(input("Enter the initial balance on the smart card: "))
        if balance >= 10:
            break
        print("Insufficient balance to swipe in! Minimum balance of $10 required. Please enter again.")
    
    card = SmartCard(balance)
    bus_system = BusSystem()

    # User input for swipe-in time
    while True:
        time_input = input("Enter swipe-in time in HH:MM (24-hour format): ")
        try:
            swipe_in_time = datetime.strptime(time_input, "%H:%M").time()
            break  # Exit loop if time input is valid
        except ValueError:
            print("Invalid time format! Please enter time in HH:MM (24-hour format).")

    # Get day of the week dynamically
    while True:
        swipe_in_day = input("Enter the day of the week (e.g., Monday, Saturday): ").strip()
        if swipe_in_day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
            break
        else:
            print("Invalid day! Please enter a valid day of the week.")

    # User input for start and end stops
    while True:
        try:
            start_stop = int(input(f"Enter the starting stop (1 to {len(bus_system.stops)}): "))
            end_stop = int(input(f"Enter the ending stop (1 to {len(bus_system.stops)}): "))
            if 1 <= start_stop <= len(bus_system.stops) and 1 <= end_stop <= len(bus_system.stops):
                break  # Exit loop if stops are valid
            else:
                print(f"Invalid stop numbers! Please enter numbers between 1 and {len(bus_system.stops)}.")
        except ValueError:
            print("Invalid input! Please enter valid integers for the stops.")

    # Ensure card can swipe in
    if card.can_swipe_in():
        print("Swipe in successful!")
        
        # Calculate fare
        fare = bus_system.calculate_fare(swipe_in_time, swipe_in_day, start_stop, end_stop)
        print(f"Calculated Fare: ${fare:.2f}")
        
        # Update card balance and swipe out
        try:
            card.update_balance(fare)
            print(f"Swipe out successful! Remaining Balance: ${card.balance:.2f}")
        except ValueError as e:
            print(e)
    else:
        print("Insufficient balance to swipe in!")

if __name__ == "__main__":
    main()
