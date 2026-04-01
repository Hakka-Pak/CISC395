from dataclasses import dataclass, field
from datetime import date

@dataclass
class Destination:
    name: str
    country: str
    budget: float
    notes: list[str] = field(default_factory=list)
    date_added: str = field(default_factory=lambda: date.today().isoformat())

    def add_note(self, note: str) -> None:
        self.notes.append(note)

class TripCollection:
    def __init__(self):
        self._trips: list[Destination] = []

    def add(self, destination: Destination) -> None:
        self._trips.append(destination)

    def get_all(self) -> list[Destination]:
        return self._trips

    def search_by_country(self, country: str) -> list[Destination]:
        return [t for t in self._trips if t.country.lower() == country.lower()]

    def get_by_index(self, index: int) -> Destination:
        return self._trips[index]

    def __len__(self) -> int:
        return len(self._trips)

    def total_budget(self) -> float:
        if not self._trips:
            return 0.0
        return sum(t.budget for t in self._trips)

    def average_budget(self) -> float:
        if len(self._trips) == 0:
            return 0.0
        return self.total_budget() / len(self._trips)

    def top_country(self) -> str:
        counts = self.count_by_country()
        if not counts:
            return "No trips yet"
        return max(counts, key=counts.get)

    def count_by_country(self) -> dict[str, int]:
        counts = {}
        for t in self._trips:
            counts[t.country] = counts.get(t.country, 0) + 1
        return counts
