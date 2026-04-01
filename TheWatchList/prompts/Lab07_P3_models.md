I am building a Movie Watchlist CLI app.

src/models.py already exists with the Movie dataclass and Watchlist collection.

Read src/models.py first, then create src/main.py with:

- The necessary imports from src/models.py.
- An instance of the Watchlist collection.
- A continuous command-line interface loop displaying these 4 menu options:
  1. Add a new movie (Prompts for title and genre, then adds to watchlist)
  2. View unwatched movies (Displays the list of unwatched movies)
  3. Mark movie as watched (Prompts for title and updates status)
  4. Quit (Exits the loop and closes the app)

Ensure the script handles user input correctly and calls the corresponding methods from the Watchlist instance for each menu option. 

Write the file directly to src/main.py.