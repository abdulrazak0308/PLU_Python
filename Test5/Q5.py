import sqlite3

class Movie:
    def __init__(self, movie_id, title, genre, rating, watch_count):
        self.movie_id = movie_id
        self.title = title
        self.genre = genre
        self.rating = rating
        self.watch_count = watch_count

    def __repr__(self):
        return f"ID: {self.movie_id:<3} | Title: {self.title:<22} | Genre: {self.genre:<10} | Rating: {self.rating} | Watch Count: {self.watch_count}"

def setup_database():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE movies (
            movie_id INTEGER PRIMARY KEY,
            title TEXT,
            genre TEXT,
            rating REAL,
            watch_count INTEGER
        )
    ''')

    sample_movies = [
        (1, "COOLIE", "Action", 9.0, 1500000),
        (2, "PEDDI", "Action", 8.8, 1200000),
        (3, "GUNTUR KARAM", "Drama", 8.9, 900000),
        (4, "SPIRIT", "Crime", 8.7, 1300000),
        (5, "RRR", "Action", 8.1, 800000),
        (6, "SALAAR", "Crime", 9.2, 1100000),
        (7, "DC", "Action", 7.6, 650000),
        (8, "VIKRAM:HITLIST", "Thriller", 7.7, 950000),
        (9, "LEO", "Thriller", 8.6, 500000),
        (10, "MASTER", "Action", 8.4, 600000),
        (11, "KGF", "Action", 8.5, 980000),
        (12, "PARADISE", "Thriller", 8.5, 880000)
    ]

    cursor.executemany("INSERT INTO movies VALUES (?, ?, ?, ?, ?)", sample_movies)
    conn.commit()
    return conn


def sort_by_rating(movie_list):
    """Sorts movies by rating from highest to lowest using simple python sorting."""
    def get_rating(movie):
        return movie.rating

    return sorted(movie_list, key=get_rating, reverse=True)


def binary_search_by_id(movie_list, target_id):
    """Searches for a movie by ID (list must be sorted by movie_id)."""
    low = 0
    high = len(movie_list) - 1

    while low <= high:
        mid = (low + high) // 2
        if movie_list[mid].movie_id == target_id:
            return movie_list[mid]
        elif movie_list[mid].movie_id < target_id:
            low = mid + 1
        else:
            high = mid - 1

    return None

def main():
    conn = setup_database()
    cursor = conn.cursor()

    cursor.execute("SELECT movie_id, title, genre, rating, watch_count FROM movies")
    rows = cursor.fetchall()

    movie_list = []
    for row in rows:
        m = Movie(row[0], row[1], row[2], row[3], row[4])
        movie_list.append(m)

    print("=== All Movies (Fetched from DB) ===")
    for m in movie_list:
        print(m)
    print("\n" + "-"*60 + "\n")


    sorted_movies = sort_by_rating(movie_list)

    print("=== Movies Sorted by Rating (Highest to Lowest) ===")
    for m in sorted_movies:
        print(m)
    print("\n" + "-"*60 + "\n")



    movies_sorted_by_id = sorted(movie_list, key=lambda m: m.movie_id)
    search_id = 4

    print(f"=== Searching for Movie ID: {search_id} ===")
    found_movie = binary_search_by_id(movies_sorted_by_id, search_id)
    if found_movie:
        print("Found:", found_movie)
    else:
        print("Movie not found.")
    print("\n" + "-"*60 + "\n")


    print("=== Top 10 Highest-Rated Movies ===")
    top_10 = sorted_movies[:10]
    for i, m in enumerate(top_10, 1):
        print(f"{i:<2}. {m}")
    print("\n" + "-"*60 + "\n")

    
    print("=== Most Watched Movie in Every Genre (Using Python Dictionary) ===")
    most_watched_by_genre = {}

    for m in movie_list:
        if m.genre not in most_watched_by_genre or m.watch_count > most_watched_by_genre[m.genre].watch_count:
            most_watched_by_genre[m.genre] = m

    for genre, movie in most_watched_by_genre.items():
        print(f"Genre: {genre:<10} | Most Watched: {movie.title} ({movie.watch_count:,} views)")

    print("\n--- Alternative: Most Watched by Genre (Using SQL GROUP BY & MAX) ---")
    query = '''
        SELECT genre, title, MAX(watch_count) 
        FROM movies 
        GROUP BY genre
    '''
    cursor.execute(query)
    for row in cursor.fetchall():
        print(f"Genre: {row[0]:<10} | Most Watched: {row[1]} ({row[2]:,} views)")

    conn.close()


if __name__ == "__main__":
    main()