import os
import json
from dataclasses import asdict
from models import Movie, Watchlist

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "movies.json")

def load_movies() -> Watchlist:
    watchlist = Watchlist()
    if not os.path.exists(DATA_PATH):
        return watchlist

    try:
        with open(DATA_PATH, "r") as f:
            data = json.load(f)
            for d in data:
                watchlist.addMovie(Movie(**d))
    except (json.JSONDecodeError, FileNotFoundError):
        pass

    return watchlist

def save_movies(watchlist: Watchlist) -> None:
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    
    list_of_dicts = [asdict(m) for m in watchlist.get_all()]
    
    with open(DATA_PATH, "w") as f:
        json.dump(list_of_dicts, f, indent=2)
