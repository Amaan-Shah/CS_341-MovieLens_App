import sqlite3
import objecttier

################################################################
################       Command Functions      ##################
################################################################
#
# cmd 1: Inputs a movie name and outputs the movie’s ID, title, and year of release
#
def cmd1(dbConn):
  print()
  name = input("Enter movie name (wildcards _ and % supported): ")
  movies = objecttier.get_movies(dbConn, name)

  print()
  print("# of movies found:", len(movies))

  if len(movies) == 0:
    return
  elif len(movies) > 100:
    print()
    print("There are too many movies to display, please narrow your search and try again...")
    return
  else:
    print()
    for movie in movies:
      print(movie.Movie_ID, ":", movie.Title, "(" + movie.Release_Year + ")")


#
# cmd 2: Inputs a movie id and outputs detailed movie information about this movie
#
def cmd2(dbConn):
  print()
  id = input("Enter movie id: ")
  print()

  movie = objecttier.get_movie_details(dbConn, id)

  if movie == None:
    print("No such movie...")
    return
  else:
    print(movie.Movie_ID, ":", movie.Title)
    print("  Release date:", movie.Release_Date)
    print("  Runtime:", movie.Runtime, "(mins)")
    print("  Orig language:", movie.Original_Language)
    print("  Budget: $" + f"{movie.Budget:,}" , "(USD)")
    print("  Revenue: $" + f"{movie.Revenue:,}", "(USD)")
    print("  Num reviews: ", movie.Num_Reviews)
    print("  Avg rating:", f"{movie.Avg_Rating:.2f}", "(0..10)")
    genres = ""
    companies = ""
    for genre in movie.Genres:
      genres += genre
      genres += ", "
    print("  Genres:", genres)
    for company in movie.Production_Companies:
      companies += company
      companies += ", "
    print("  Production companies:", companies)
    print("  Tagline:", movie.Tagline)
  return

  
#
# cmd 3: Output the top N movies based on their average rating *and* with a minimum number of reviews
#
def cmd3(dbConn):
  print()
  N = int(input("N? "))
  if N <= 0:
    print("Please enter a positive value for N...")
    return
  numRevs = int(input("min number of reviews? "))
  if numRevs <= 0:
    print("Please enter a positive value for min number of reviews...")
    return

  ratings = objecttier.get_top_N_movies(dbConn, N, numRevs)
  print()

  for rate in ratings:
    print(rate.Movie_ID, ":", rate.Title, "(" + rate.Release_Year + "), avg rating =", f"{rate.Avg_Rating:.2f}", "(" + str(rate.Num_Reviews) + " reviews)")


#
# cmd 4: Inserts a new review into the database
#
def cmd4(dbConn):
  print()
      
  rating = int(input("Enter rating (0..10): "))    
  if  rating < 0 or rating > 10:
    print("Invalid rating...")
    return
        
  id = int(input("Enter movie id: "))

  updated = objecttier.add_review(dbConn, id, rating)
  print()
  if updated == 1:
    print("Review successfully inserted")
  else:
    print("No such movie...")
    
  return


#
# cmd 5: Sets the tagline for a given movie, either by inserting (if not already there) or updating (if already there).
#
def cmd5(dbConn):
  print()

  tag = input("tagline? ")
  id = int(input("movie id? "))

  newTag = objecttier.set_tagline(dbConn, id, tag)

  if newTag == 0:
    print()
    print("No such movie...")
  else:
    print()
    print("Tagline successfully set")

  return
  
##################################################################  
#
# main
#
print('** Welcome to the MovieLens app **')

dbConn = sqlite3.connect('MovieLens.db')

print()

print("General stats:")

movies = objecttier.num_movies(dbConn)
print("  # of movies:", f"{movies:,}")

reviews = objecttier.num_reviews(dbConn)
print("  # of reviews:", f"{reviews:,}")

print()
cmd = input("Please enter a command (1-5, x to exit): ")

while cmd != "x":
    if cmd == "1":
      cmd1(dbConn)
      
    elif cmd == "2":
      cmd2(dbConn)
      
    elif cmd == "3":
      cmd3(dbConn)
      
    elif cmd == "4":
        cmd4(dbConn)
      
    elif cmd == "5":
      cmd5(dbConn)
  
    else:
      print("**Error, unknown command, try again...")

    print()
    cmd = input("Please enter a command (1-5, x to exit): ")

#
# done
#