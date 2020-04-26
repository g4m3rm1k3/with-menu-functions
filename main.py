#imports
from bs4 import BeautifulSoup
import requests
import re
from movies import populate_movies
from art import tprint
from collections import namedtuple

#movie database
movie_db = []

#main menu
MENU_PROMPT = '''
 *************************************
 *    Here are your menu options     *
 *************************************
 * V: View movies                    *
 * A: Add a movie                    *
 * S: Search for a movie             *
 * Q: Quit                           *
 * C: Clear screen                   *
 * M: Menu                           *
 * H: Help                           *
 *************************************
 '''

Movie = namedtuple('Movie', ['title', 'director', 'year'])


#Add movie function
def add_new_movie():
    name = input("Please enter the name of the movie: ")
    year = input("Please enter the year of the movie: ")
    director = input("Please enter the director of the movie: ")
    return Movie(name, director, year)


#Display movie function
def display_movies(movies, pagination = True, pag_count = 3):
    space = long_mov_str()
    for i,movie in enumerate(movies):
          display_format(space, *movie)
          if pagination:
            if i % pag_count == 0:
              retract = input("Press enter or P to break pagination: \n")
              if retract == 'p':
                  pagination = False

#Create a format for movies to be diplayed as a column                  
def display_format(space, title, director, year):
        print("*" * space)
        print(f'{title:^{space}}\n{director:^{space}}'
        f'\n{year:^{space}}')
        print("*" * space, "\n")

#search movie function
def search_movies(search_term, movies, pagination = True, count=0):
    found_movies = []
    for movie in movies:
        search_results = [
            attribute for attribute in movie
            if search_term in attribute.lower()
        ]
        if search_results:
            found_movies.append(movie)
    if found_movies:
        display_movies(found_movies, pagination)
    elif count < 2 and not found_movies:
        search_term = input("Term not found Please Try again: ")
        search_movies(search_term, movies, pagination, count + 1)


#Menu function
def menu(clear=False):
    print(MENU_PROMPT)
    if clear:
        print("\n" * 20)
        clear = False

    
#Add movie funciton
def add_movie():
    movie_db.append(add_new_movie())
    input("Movie added successfully press enter to continue... ")


#View movie function
def view_movies():
    display_movies(movie_db)


#Search movies function
def search():
    search_term = input("Please enter a search term: ")
    search_movies(search_term.lower(), movie_db)


#Clear screen function
def clear_screen():
    clear = True
    print("\n" * 100)
    menu(clear)


#help menu function
def help_menu():
    print("press M to show menu: ")
    print("Press C to clear screen: ")
    print("Press Q to quit: ")


#start of app
def app_start():
    selection = 'm'
    CHOICES[selection]()
    while selection != 'q':
      selection = input("Please make a choice: ").strip().lower()
      if selection == 'q':
        print("Thanks for playing")
      else:
        if selection in CHOICES:
          CHOICES[selection]()
        else:
          print("That isn't a valid option. ")


#choises to function mapping dict
CHOICES = {
    'a': add_movie,
    'v': view_movies,
    'm': menu,
    's': search,
    'h': help_menu,
    'c': clear_screen,
}

# Variables to hold webscraping
url = 'http://www.imdb.com/chart/top'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

#get movies from td table data titleColumn
movies = soup.select('td.titleColumn')

#get title in formation form title= 
directors = [a.attrs.get('title').split("(dir.)")[0] for a in soup.select('td.titleColumn a')]

#Populate movie db
populate_movies(Movie, movie_db, movies, directors)

#Fancey menu heading
print("\n" * 2, "*" * 39)
tprint("  MOVIES\n by  Mike", font="cybermedium")
print("*" * 39, "\n" * 2)

#Find longest length of movie string
def long_mov_str():
  longest = []  
#make a list of string lengths and return the hightest
  for movie in movie_db:
    longest.append(max(len(attribute) for attribute in movie))
  return max(longest)

#Start of app here on the bottom lonely by itself
app_start()
