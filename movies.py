
#Loop to populate database
def populate_movies(Movie, movie_db, movies, directors):
  for movie, director in zip(movies, directors):
      movie_string = movie.get_text()

      #get line of movie from imdb

      _, title, year = movie.get_text().strip().split("\n")
      title = title.strip()
      year = year.strip("( )")
      #add movie to database

      movie_db.append(Movie(title,director, year))