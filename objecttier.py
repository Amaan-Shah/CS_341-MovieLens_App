#
# objecttier
#
# Builds Movie-related objects from data retrieved through 
# the data tier.
#
# Original author:
#   Prof. Joe Hummel
#   U. of Illinois, Chicago
#   CS 341, Spring 2022
#   Project #02
#
import datatier


##################################################################
#
# Movie:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#
class Movie:
  def __init__(self, id, title, year):
    self._Movie_ID = id
    self._Title = title
    self._Release_Year = year

  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Year(self):
    return self._Release_Year 

##################################################################
#
# MovieRating:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#   Num_Reviews: int
#   Avg_Rating: float
#
class MovieRating:
  def __init__(self, id, title, year, numRevs, avg):
    self._Movie_ID = id
    self._Title = title
    self._Release_Year = year
    self._Num_Reviews = numRevs
    self._Avg_Rating = avg

  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title
  
  @property
  def Release_Year(self):
    return self._Release_Year
  
  @property
  def Num_Reviews(self):
    return self._Num_Reviews
  
  @property
  def Avg_Rating(self):
    return self._Avg_Rating
  
##################################################################
#
# MovieDetails:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Date: string, date only (no time)
#   Runtime: int (minutes)
#   Original_Language: string
#   Budget: int (USD)
#   Revenue: int (USD)
#   Num_Reviews: int
#   Avg_Rating: float
#   Tagline: string
#   Genres: list of string
#   Production_Companies: list of string
#
class MovieDetails:
  def __init__(self, id, title, relDate, runtime, lang, bud, rev, numRevs, avg, tag, genres, prod_cos):
    self._Movie_ID = id
    self._Title = title
    self._Release_Date = relDate
    self._Runtime = runtime
    self._Original_Language = lang
    self._Budget = bud
    self._Revenue = rev
    self._Num_Reviews = numRevs
    self._Avg_Rating = avg
    self._Tagline = tag
    self._Genres = genres
    self._Production_Companies = prod_cos
  
  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title
  
  @property
  def Release_Date(self):
    return self._Release_Date
  
  @property
  def Runtime(self):
    return self._Runtime

  @property
  def Original_Language(self):
    return self._Original_Language

  @property
  def Budget(self):
    return self._Budget

  @property
  def Revenue(self):
    return self._Revenue

  @property
  def Num_Reviews(self):
    return self._Num_Reviews

  @property
  def Avg_Rating(self):
    return self._Avg_Rating
  
  @property
  def Tagline(self):
    return self._Tagline
  
  @property
  def Genres(self):
    return self._Genres
  
  @property
  def Production_Companies(self):
    return self._Production_Companies

##################################################################
# 
# num_movies:
#
# Returns: # of movies in the database; if an error returns -1
#
def num_movies(dbConn):
  try:
    sql = "select count(*) from Movies"
    movies = datatier.select_one_row(dbConn, sql)
    num = movies[0]
    return num

  except Exception as err:
    print("num_movies failed:", err)
    return -1;


##################################################################
# 
# num_reviews:
#
# Returns: # of reviews in the database; if an error returns -1
#
def num_reviews(dbConn):
  try:
    sql = "select count(*) from Ratings"
    reviews = datatier.select_one_row(dbConn, sql)
    num = reviews[0]
    return num

  except Exception as err:
    print("num_reviews failed:", err)
    return -1;


##################################################################
#
# get_movies:
#
# gets and returns all movies whose name are "like"
# the pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all stations.
#
# Returns: list of movies in ascending order by name; 
#          an empty list means the query did not retrieve
#          any data (or an internal error occurred, in
#          which case an error msg is already output).
#
def get_movies(dbConn, pattern):
  try:
    movies = []

    sql = """ select  movie_id, title, strftime('%Y', release_date) as year
              from movies
              where title like ?
              order by title asc;"""

    parameters = []
    parameters.append(pattern)

    rows = datatier.select_n_rows(dbConn, sql, parameters)

    for row in rows:
      newMovie = Movie(row[0], row[1], row[2])
      movies.append(newMovie)
    
    return movies
    
  except Exception as err:
    print("get_movies failed:", err)
    return None

##################################################################
#
# get_movie_details:
#
# gets and returns details about the given movie; you pass
# the movie id, function returns a MovieDetails object. Returns
# None if no movie was found with this id.
#
# Returns: if the search was successful, a MovieDetails obj
#          is returned. If the search did not find a matching
#          movie, None is returned; note that None is also 
#          returned if an internal error occurred (in which
#          case an error msg is already output).
#
def get_movie_details(dbConn, movie_id):
  
  params = []
  params.append(movie_id)

  sql = """ select movie_id, title, date(release_date), runtime, original_language, budget, revenue
            from movies
            where movie_id = ?"""
  row = datatier.select_one_row(dbConn, sql, params)

  if len(row) == 0:
    return None
    
  id = row[0]
  title = row[1]
  relDate = row[2]
  runtime = row[3]
  lang = row[4]
  budget = row[5]
  revenue = row[6]

  sql = """ select count(rating), avg(rating)
            from ratings
            where movie_id = ?"""
  row = datatier.select_one_row(dbConn, sql, params)

  if row[0] == 0:
    numRevs = 0
    avg = 0.0
  else:
    numRevs = row[0]
    avg = row[1]
    
  genres = []
  sql = """ select distinct genre_name
            from genres
            join movie_genres on (movie_genres.genre_id = genres.genre_id)
            join movies on (movie_genres.movie_id = movies.movie_id)
            where movies.movie_id = ?
            order by genre_name asc"""
  rows = datatier.select_n_rows(dbConn, sql, params)
  for row in rows:
    genres.append(row[0])
    
  companies = []
  sql = """ select company_name
            from companies
            join movie_production_companies on (movie_production_companies.company_id = companies.company_id)
            join movies on (movie_production_companies.movie_id = movies.movie_id)
            where movies.movie_id = ?
            order by company_name asc"""
  rows = datatier.select_n_rows(dbConn, sql, params)
  for row in rows:
    companies.append(row[0])

  sql = """ select tagline
            from movie_taglines
            join movies on (movie_taglines.movie_id = movies.movie_id)
            where movies.movie_id = ?"""
  row = datatier.select_one_row(dbConn, sql, params)
    
  if len(row) == 0:
    tag = ""
  else:
    tag = row[0]

  data = MovieDetails(id, title, relDate, runtime, lang, budget, revenue, numRevs, avg, tag, genres, companies)

  return data
         

##################################################################
#
# get_top_N_movies:
#
# gets and returns the top N movies based on their average 
# rating, where each movie has at least the specified # of
# reviews. Example: pass (10, 100) to get the top 10 movies
# with at least 100 reviews.
#
# Returns: returns a list of 0 or more MovieRating objects;
#          the list could be empty if the min # of reviews
#          is too high. An empty list is also returned if
#          an internal error occurs (in which case an error 
#          msg is already output).
#
def get_top_N_movies(dbConn, N, min_num_reviews):
  try:
    movieRatings = []

    params = []
    params.append(int(min_num_reviews))
    params.append(int(N))

    sql = """ select movies.movie_id, title, strftime('%Y', release_date) as year, count(rating) as numRatings, avg(rating) as average
              from ratings
              join movies on (ratings.movie_id = movies.movie_id)
              group by movies.movie_id
              having numRatings >= ?
              order by average desc
              limit ?"""
    rows = datatier.select_n_rows(dbConn, sql, params)
    
    for row in rows:
      rate = MovieRating(row[0], row[1], row[2], row[3], row[4])
      movieRatings.append(rate)

    return movieRatings
  except Exception as err:
    list = []
    print("get_top_N_movies failed:", err)
    return list


##################################################################
#
# add_review:
#
# Inserts the given review --- a rating value 0..10 --- into
# the database for the given movie. It is considered an error
# if the movie does not exist (see below), and the review is
# not inserted.
#
# Returns: 1 if the review was successfully added, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def add_review(dbConn, movie_id, rating):
  try:
    #check if movie exists
    sql = """ select title
              from movies
              where movie_id = ?"""
    params = []
    params.append(movie_id)

    movies = datatier.select_one_row(dbConn, sql, params)
    
    if len(movies) < 1: #movie does not exist
      return 0

    params.append(rating)
    sql = """ insert into ratings(movie_id, rating)
              values(?, ?)"""

    rowsChanged = datatier.perform_action(dbConn, sql, params)
    if rowsChanged == 1:
      return 1
    else:
      return 0
      
  except Exception as err:
    print("add_review error:", err)
    return 0


##################################################################
#
# set_tagline:
#
# Sets the tagline --- summary --- for the given movie. If
# the movie already has a tagline, it will be replaced by
# this new value. Passing a tagline of "" effectively 
# deletes the existing tagline. It is considered an error
# if the movie does not exist (see below), and the tagline
# is not set.
#
# Returns: 1 if the tagline was successfully set, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def set_tagline(dbConn, movie_id, tagline):
  try:
    #check if movie exists
    sql = """ select title
              from movies
              where movie_id = ?"""
    params = []
    params.append(movie_id)

    movies = datatier.select_one_row(dbConn, sql, params)
    
    if len(movies) < 1: #movie does not exist
      return 0

    #Check current tagline
    sql = """ select tagline
              from movie_taglines
              where movie_id = ?"""
    tags = datatier.select_one_row(dbConn, sql, params)

    params.append(tagline)
    
    if len(tags) == 0: # Insert tag
      sql = """ insert into movie_taglines(movie_id, tagline)
                values(?, ?)"""
      
      rowsChanged = datatier.perform_action(dbConn, sql, params)
      if rowsChanged == 1:
        return 1
      else:
        return 0 
      
    else: # Update tag
      parameters = []
      parameters.append(tagline)
      parameters.append(movie_id)
  
      sql = """ update movie_taglines
                set tagline = ?
                where movie_id = ?"""

      rowsChanged = datatier.perform_action(dbConn, sql, parameters)
      if rowsChanged == 1:
        return 1
      else:
        return 0 
    
  except Exception as err:
    print("set_tagline failed:", err)
    return 0
