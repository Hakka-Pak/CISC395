from models import Movie, Watchlist

def main():
    watchlist = Watchlist()
    
    while True:
        print("\n--- Movie Watchlist CLI ---")
        print("1. Add a new movie")
        print("2. View unwatched movies")
        print("3. Mark movie as watched")
        print("4. Quit")
        
        choice = input("\nSelect an option (1-4): ")
        
        if choice == '1':
            title = input("Enter movie title: ")
            genre = input("Enter movie genre: ")
            movie = Movie(title=title, genre=genre)
            watchlist.addMovie(movie)
            print(f"Added '{title}' to the watchlist.")
            
        elif choice == '2':
            unwatched = watchlist.getUnwatchedMovies()
            if not unwatched:
                print("\nNo unwatched movies in your list.")
            else:
                print("\nUnwatched Movies:")
                for movie in unwatched:
                    print(f"- {movie.title} ({movie.genre})")
                    
        elif choice == '3':
            title = input("Enter the title of the movie to mark as watched: ")
            if watchlist.markAsWatched(title):
                print(f"Marked '{title}' as watched.")
            else:
                print(f"Movie '{title}' not found in the watchlist.")
                
        elif choice == '4':
            print("Exiting the Movie Watchlist app. Goodbye!")
            break
        else:
            print("Invalid selection. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
