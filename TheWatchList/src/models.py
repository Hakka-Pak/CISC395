from dataclasses import dataclass
from typing import List

@dataclass
class Movie:
    title: str
    genre: str
    isWatched: bool = False

class Watchlist:
    def __init__(self):
        self.movies: List[Movie] = []

    def addMovie(self, movie: Movie):
        """Adds a movie to the watchlist."""
        self.movies.append(movie)

    def markAsWatched(self, title: str):
        """Marks a movie with the given title as watched."""
        for movie in self.movies:
            if movie.title.lower() == title.lower():
                movie.isWatched = True
                return True
        return False

    def getUnwatchedMovies(self) -> List[Movie]:
        """Returns a list of movies that have not been watched."""
        return [movie for movie in self.movies if not movie.isWatched]

    def get_all(self) -> List[Movie]:
        """Returns all movies in the watchlist."""
        return self.movies
