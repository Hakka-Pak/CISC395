import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ai_assistant import ask, TRAVEL_SYSTEM_PROMPT
from src.models import Destination
from src.storage import load_trips, save_trips


def show_all_trips(collection) -> None:
	if len(collection) == 0:
		print("No trips saved yet.")
		return

	for index, trip in enumerate(collection.get_all(), start=1):
		print(f"{index}. {trip.name} ({trip.country}) - ${trip.budget}")
		print(f"   Notes: {trip.notes}")


def show_search_results(collection) -> None:
	country = input("Country: ")
	results = collection.search_by_country(country)

	if not results:
		print("No trips found.")
		return

	for index, trip in enumerate(results, start=1):
		print(f"{index}. {trip.name} ({trip.country}) - ${trip.budget}")
		print(f"   Notes: {trip.notes}")


def add_destination(collection) -> None:
	name = input("Name: ")
	country = input("Country: ")

	try:
		budget = float(input("Budget: "))
	except ValueError:
		print("Invalid budget.")
		return

	collection.add(Destination(name, country, budget))
	save_trips(collection)
	print("Destination added.")


def add_note_to_destination(collection) -> None:
	if len(collection) == 0:
		print("No trips saved yet.")
		return

	show_all_trips(collection)

	try:
		choice = int(input("Choose a trip number: "))
		trip = collection.get_by_index(choice - 1)
	except (ValueError, IndexError):
		print("Invalid option, try again.")
		return

	note = input("Note: ")
	trip.add_note(note)
	save_trips(collection)
	print("Note added.")


def ask_ai(collection) -> None:
	question = input("Your question: ")
	response = ask(question, system_prompt=TRAVEL_SYSTEM_PROMPT)

	if response is None:
		print("Error: Could not get a response from AI.")
		return

	print("\nAI Response:")
	print(response)

	save_choice = input("\nSave this as a note on a trip? (y/n): ")
	if save_choice.lower() == "y":
		if len(collection) == 0:
			print("No trips saved yet.")
			return

		show_all_trips(collection)
		try:
			trip_index = int(input("Trip number: ")) - 1
			if trip_index < 0 or trip_index >= len(collection):
				raise IndexError
			trip = collection.get_by_index(trip_index)
		except (ValueError, IndexError):
			print("Invalid option, saving cancelled.")
			return

		trip.add_note(response)
		save_trips(collection)
		print(f"Saved as a note on {trip.name}.")


def main() -> None:
	collection = load_trips()

	while True:
		print("\n=== Trip Notes ===")
		print("\n-- Data --")
		print("[1] Add destination")
		print("[2] View all destinations")
		print("[3] Search by country")
		print("[4] Add note to a destination")
		print("\n-- AI --")
		print("[6] Ask AI a travel question\n")
		print("[Q] Quit")

		choice = input("Choose an option: ")

		if choice == "1":
			add_destination(collection)
		elif choice == "2":
			show_all_trips(collection)
		elif choice == "3":
			show_search_results(collection)
		elif choice == "4":
			add_note_to_destination(collection)
		elif choice == "6":
			ask_ai(collection)
		elif choice.lower() == "q":
			print("Goodbye!")
			break
		else:
			print("Invalid option, try again.")


if __name__ == "__main__":
	main()
