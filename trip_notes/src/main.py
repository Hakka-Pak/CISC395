import sys
import os

# Fix import path to work from the trip_notes/ root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import Destination, TripCollection
from src.storage import load_trips, save_trips

def main():
    collection = load_trips()

    while True:
        print("\n=== Trip Notes ===")
        print("[1] Add destination")
        print("[2] View all destinations")
        print("[3] Search by country")
        print("[4] Add note to a destination")
        print("[5] Quit")
        print("[6] Show Statistics")
        
        choice = input("Choice: ")

        if choice == '1':
            name = input("Enter name: ")
            country = input("Enter country: ")
            try:
                budget = float(input("Enter budget: "))
            except ValueError:
                print("Invalid budget. Using 0.0")
                budget = 0.0
            
            dest = Destination(name=name, country=country, budget=budget)
            collection.add(dest)
            save_trips(collection)
            print("Destination added!")

        elif choice == '2':
            if len(collection) == 0:
                print("No trips saved yet.")
            else:
                for i, trip in enumerate(collection.get_all(), 1):
                    print(f"{i}. {trip.name} ({trip.country}) - Budget: ${trip.budget:.2f}")
                    if trip.notes:
                        print(f"   Notes: {', '.join(trip.notes)}")

        elif choice == '3':
            country = input("Enter country to search: ")
            results = collection.search_by_country(country)
            if not results:
                print(f"No destinations found in {country}.")
            else:
                for trip in results:
                    print(f"- {trip.name} - Budget: ${trip.budget:.2f}")

        elif choice == '4':
            if len(collection) == 0:
                print("No destinations available to add notes.")
                continue
            
            # Print numbered list
            for i, trip in enumerate(collection.get_all(), 1):
                print(f"{i}. {trip.name} ({trip.country})")
            
            try:
                idx = int(input("Select destination number: "))
                trip = collection.get_by_index(idx - 1)
                note = input("Enter note: ")
                trip.add_note(note)
                save_trips(collection)
                print("Note added!")
            except (ValueError, IndexError):
                print("Invalid selection.")

        elif choice == '5':
            print("Goodbye!")
            break
        
        elif choice == '6':
            if len(collection) == 0:
                print("No trips saved yet.")
            else:
                counts = collection.count_by_country()
                top_country_name = collection.top_country()
                top_country_count = counts.get(top_country_name, 0)
                
                print("\n=== Trip Statistics ===")
                print(f"Total trips: {len(collection)}")
                print(f"Total budget: ${collection.total_budget():,.2f}")
                print(f"Average budget: ${collection.average_budget():,.2f}")
                print(f"Top country: {top_country_name} ({top_country_count} trips)")
                print("Trips by country:")
                for country, count in counts.items():
                    print(f"  {country}: {count}")

        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()
