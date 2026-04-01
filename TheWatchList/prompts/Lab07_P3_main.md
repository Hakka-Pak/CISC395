I am building a Movie Watchlist CLI app.

Create src/models.py with:

- 
Movie (@dataclass): title, genre, isWatched

- 
Watchlist: addMovie(), markAsWatched(), getUnwatchedMovies()

Read src/models.py first, then create src/main.py with:

A command-line interface loop displaying these 4 menu options:
1. Add a new movie
2. View unwatched movies
3. Mark movie as watched
4. Quit

Do not add an if __name__ == "__main__" block in src/models.py.

Write the files directly to src/models.py and src/main.py.