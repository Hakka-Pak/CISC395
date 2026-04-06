import json
import os
from dataclasses import asdict

from src.models import Destination, TripCollection


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "trips.json")


def load_trips() -> TripCollection:
	collection = TripCollection()

	if not os.path.exists(DATA_PATH):
		return collection

	with open(DATA_PATH, encoding="utf-8") as file:
		raw_trips = json.load(file)

	for trip_data in raw_trips:
		collection.add(Destination(**trip_data))

	return collection


def save_trips(collection: TripCollection) -> None:
	os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

	serializable_trips = [asdict(destination) for destination in collection.get_all()]

	with open(DATA_PATH, "w", encoding="utf-8") as file:
		json.dump(serializable_trips, file, indent=2)
