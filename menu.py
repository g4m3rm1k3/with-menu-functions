#imports
from bs4 import BeautifulSoup
import requests
import re
from movies import populate_movies
from art import tprint

#movie database
movie_db = []



#main menu
menu_prompt = '''
 *************************************
 *    Here are your menu options     *
 *************************************
 * V: View movies                    *
 * A: Add a movie                    *
 * S: Search for a movie             *
 * Q: Quit                           *
 * C: Clear screen                   *
 * M: Menu                           *
 * R: Make a selection               *
 * H: Help                           *
 * P: Pagination toggle              *
 *************************************
 '''

#Movie Class
class Movie:
    def __init__(self, new_title, new_director, new_year):
        self.title = new_title
        self.director = new_director
        self.year = new_year

    #function to display a movie
    def __str__(self):
      return f'{self.title:^20}\n{self.director:^20}\n{self.year:^20}'

    #function to search movies
    @property
    def search_term(self):

        #combine all data 
        data = [self.title, self.director, self.year]
        return [(e.lower()).split(" ") for e in data]
#Add movie function
def add_new_movie():
    name = input("Please enter the name of the movie: ")
    year = input("Please enter the year of the movie: ")
    director = input("Please enter the director of the movie: ")
    return Movie(name, director, year)


#Display movie function
def display_movies(movies, pagination, count = 3):
    pag_count = count
    for movie in movies:
        pag_count -= 1
        print("*" * 20)
        print(str(movie))
        print("*" * 20, "\n")
        if pagination and pag_count == 0:
            retract = input("Press enter or P to break pagination: \n")
            if retract:
                pagination = False
            pag_count = count

#search movie function
def search_movies(search_term, movies, pagination, count=0):
    found_movies = [movie for movie in movies if search_term in [e for e in movie.search_term for e in e]]
    if found_movies:
        display_movies(found_movies, pagination)
    if count < 2 and not found_movies:
        search_term = input("Term not found Please Try again: ")
        search_movies(search_term, movies, pagination, count + 1)


#pagination function
def pagination(pagination = False,count = 3,  *args):
    if not pagination:
        pagination = True
        print("Pagination is on")
        result(pagination, count)
    elif pagination:
        pagination = False
        print("Pagination is off")
        result(pagination)


#Menu function
def menu(clear=False, *args):
    print(menu_prompt)
    if clear:
        print("\n" * 20)
        clear = False

    
#Add movie funciton
def add_movie(*args):
    movie_db.append(add_new_movie())
    input("Movie added successfully press enter to continue... ")

#View movie function
def view_movies(pagination = False, *args):
    display_movies(movie_db, pagination)



#Search movies function
def search(*args):
    search_term = input("Please enter a search term: ")
    search_movies(search_term.lower(), movie_db, pagination)

#Clear screen function
def clear_screen(*args):
    clear = True
    print("\n" * 100)
    menu(clear, *args)

#help menu function
def help_menu(*args):
    print("press M to show menu: ")
    print("Press C to clear screen: ")
    print("Press Q to quit: ")

#quit funciton
def quit(*args):
    question = input("Are you sure you want to quit")
    q = True
    app_start(q)


#choice function
def get_choice(*args):
        selection = input("Please make a choice: ").strip()
        try:
            choice(selection)
        except KeyError:
            print("That isn't a valid option.")


#start of app
def app_start( q = False, *args):
    print("running from here")
    while not q:
      choice('m', *args)
      get_choice(*args)


#choises to function mapping dict
CHOICES = {
    'a': add_movie,
    'r': result,
    'v': view_movies,
    'm': menu,
    's': search,
    'q': quit,
    'h': help_menu,
    'p': pagination,
    'c': clear_screen,
}

#Makeshift switch statement for menu options
def choice(*args):
  if selection[0] = "a":
      CHOICES[selection[0]](*args)
  elif selection[0] = "r":
      CHOICES[selection[0]](*args)
  elif selection[0] = "v":
      CHOICES[selection[0]](*args)
  elif selection[0] = "m":
      CHOICES[selection[0]](*args)
  elif selection[0] = "s":
      CHOICES[selection[0]](*args)
  elif selection[0] = "q":
      CHOICES[selection[0]](*args)
  elif selection[0] = "h":
      CHOICES[selection[0]](*args)
  elif selection[0] = "p":
      CHOICES[selection[0]](*args)
  elif selection[0] = "c":
      CHOICES[selection[0]](*args)
  else:
    get_choice(*args)


# Variables to hold webscraping
url = 'http://www.imdb.com/chart/top'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

#get movies from td table data titleColumn
movies = soup.select('td.titleColumn')

#get title in formation form title= 
directors = [a.attrs.get('title').split("(dir.)")[0] for a in soup.select('td.titleColumn a')]

populate_movies(Movie,movie_db, movies, directors)

#Fancey menu heading
print("\n" * 2, "*" * 39)
tprint("  MOVIES\n by  Mike", font="cybermedium")
print("*" * 39, "\n" * 2)


#Start of app here on the bottom lonely by itself
app_start()
