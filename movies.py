from random import randint

import matplotlib.pyplot as plt

from bin.constants import *
from bin.modules import *

from os import listdir
from os.path import isfile
from json import load, dumps, JSONDecodeError

class Movie:
    def __init__(self,movie_data: dict):
        self.movie_data = movie_data


    def asdict(self) -> dict:
        """
        Used to default some values e.g. on save
        """
        return {
            'title': self.title,
            'rating': self.rating,
            'release_year': self.release_year
        }
    @property
    def title(self) -> str:
        return self.movie_data.get('title','n.a.')
    @title.setter
    def title(self, value: str):
        self.movie_data['title'] = value
    @property
    def rating(self) -> int:
        return self.movie_data.get('rating',0)
    @rating.setter
    def rating(self, value: int):
        self.movie_data['rating'] = value
    @property
    def release_year(self) -> int:
        return self.movie_data.get('release_year',0)
    @release_year.setter
    def release_year(self, value: int):
        self.movie_data['release_year'] = value
    

class MovieRank:
    def __init__(self):
        self.isrunning = True
        self.load_movies()

    @property
    def titles(self) -> list[str]:
        return [i.title for i in self.movies]

    def save_movies(self):
        with open(f'movies.json', 'w') as file_write:
            file_write.write(dumps([movie.asdict() for movie in self.movies],indent=4))
    
    def load_movies(self):
        self.movies: list[Movie] = []
        file_name = f'movies.json'
        if isfile(file_name):
            try:
                with open(file_name) as file_read:
                    movies_json = load(file_read)
                    if not isinstance(movies_json,list):
                        raise TypeError()
                    self.movies = [Movie(movie) for movie in movies_json]
                    
            except JSONDecodeError:
                print(f'Cant load from file: {file_name} ERROR: JSONDE')
            except TypeError:
                print(f'Cant load from file: {file_name} ERROR: TE')
        
    
    def list_movies(self):

        print(f"Movies in total: {len(self.movies)}")
        print(f"{'Movie':<45} {'Rating':<7} {'Release':<7}")
        for movie in self.movies:
            print(f"{movie.title:<45} {movie.rating:<7} {movie.release_year}")
            
    def add_movie(self):

        title =  get_user_input_colorized("Movie title: ")
        rating = convert_to_float(get_user_input_colorized("Movie rating: "))
        release_year = convert_to_float(get_user_input_colorized("Movie release year: "))
        
        if release_year < 1891:
            error(MSG_KINETOSSCOPE_NOT_INVENTED_YET)
            return
        if not rating: 
            error(MSG_RATING_IS_NOT_NUMERIC)
            return
        if rating > 10:
            error(MSG_WRONG_RATING)
            return
        
        if title not in [i.title for i in self.movies]:
            
            temp_movie = Movie(
                {
                    "title": title,
                    'rating': rating,
                    "release_year": int(release_year)
                }
            )
            self.movies.append(temp_movie)
            
    def remove_movie(self):

        title =  get_user_input_colorized("Movie title: ")
        if title in self.titles:
            
            self.movies.pop(self.titles.index(title))
        else:
            error(MSG_MOVIE_DOESNT_EXIST)
            
    def edit_movie(self):

        title =  get_user_input_colorized("Movie title: ")
        
        if title not in self.movies:
            error(MSG_MOVIE_DOESNT_EXIST)
            return
        
        rating = get_user_input_colorized("Movie rating: ")
        
        if not rating: 
            error(MSG_RATING_IS_NOT_NUMERIC)
            return
        if rating > 10:
            error(MSG_WRONG_RATING)
            return
        if title in self.titles:
            self.movies[self.titles.index(title)].rating = rating
        else:
            error(MSG_MOVIE_DOESNT_EXIST)
            
    def print_stats(self):
        """
        Calculates and prints various statistics about the movie ratings.

        This method computes the average, median, worst, and best ratings 
        from the 'movies' attribute of the instance. It then prints these statistics
        in a user-friendly format.
        """
        ratings = [self.movies[i] for i in self.movies]
        median = ratings.copy()
        median.sort()
        median_hlen = len(median)//2
        if len(median) % 2:
            median = median[median_hlen]
        else:
            
            _median_1 = median[median_hlen]
            median.sort(reverse=True)
            median = round((median[median_hlen] +_median_1) / 2,2)
            print(median)
        average = sum(ratings) / len(ratings)
        worst, ratingW = [],11
        best, ratingB = [],-1
        
        for key in self.movies:
            if self.movies[key] > ratingB:
                best.append(key)
                ratingB = self.movies[key]
            if self.movies[key] < ratingW:
                worst.append(key)
                ratingW = self.movies[key]
        
        print(f"Average rating: {round(average,2)}. Median rating: {median}.\n{"-"*15}")
        print(f'Best Rating{"s" if len(best) > 1 else ""}\n{"-"*15}')
        for b in best:
            print(f"Rating: {b} with {ratingB}/10")
        print(f'Worst Rating{"s" if len(worst) > 1 else ""}\n{"-"*15}')
        for w in worst:
            print(f"Rating: {w} with {ratingW}/10. ")
        
    def print_random_movie(self):
        """ 
        Selects and prints a random movie and its rating from the instance's collection.

        This method randomly picks one movie from the 'movies' attribute and
        displays its title along with its corresponding rating to the console.
        """
        rndMovie = [i for i in self.movies][randint(0,len(self.movies)-1)]
        print(f"{rndMovie}: {self.movies[rndMovie]}")
    
    def print_movies_by_rank(self):
        """
        Prints all movies stored in the instance, sorted by their rating in descending order.

        Each movie's name and its rating (out of 10) are printed to the console.
        The movie name is left-aligned and padded to a width of 35 characters.
        """
        listed = [[i,self.movies[i]] for i in self.movies]
        listed = sorted(listed,key=lambda x: x[1],reverse=True)
        for n, r in listed:
            print(f"{n:<35} {r}/10")
    def print_search(self):
        """
        Prompts the user for a search query and prints matching movie titles.

        This method first asks the user for a search string using `get_user_input_colorized`.
        It then attempts to find an exact, case-insensitive match within the movie titles.
        If an exact match is found, it's printed.

        If no exact match is found, the method iterates through all movie titles
        and prints any movie whose title has a significant similarity to the search query,
        as determined by the `compare_two_strings` function.
        """
        value = get_user_input_colorized("Search: ").lower()
        normal_movies = list(self.movies)
        low_movies = [m.lower() for m in normal_movies]
        results = 0
        if value in low_movies:
            #normal_movies[low_movies.index(value)]
            results += 1
            print(normal_movies[low_movies.index(value)])
        if not results:
            for movie in self.movies:
                if compare_two_strings(value, movie):
                    print(movie)
    def plot_movies(self):
        """ Generates and displays a histogram of movie ratings. """
        plt.hist([self.movies[i] for i in self.movies])
        plt.show()
    def byebye(self):
        """ The last thing the app will do before close """
        self.save_movies()
        print('bye!')
    def update(self,inp):
        """
        Acts as a dispatcher for various movie management operations based on user input.

        This method takes a string input, typically representing a user's menu choice,
        and calls the corresponding movie-related method within the class.
        """
        match inp:
            case '0': 
                self.isrunning = False
                self.byebye()
            case "1": self.list_movies()
            case "2": self.add_movie()
            case "3": self.remove_movie()
            case "4": self.edit_movie()
            case "5": self.print_stats()
            case "6": self.print_random_movie()
            case "7": self.print_search()
            case "8": self.print_movies_by_rank()
            case "9": self.plot_movies()
            case _: error(MSG_INVALID_INPUT)         

def main():
    while MR.isrunning:
        print("""\033[J
********** My Movies Database **********

Menu:
1. List movies
2. Add movie
3. Delete movie
4. Update movie
5. Stats
6. Random movie
7. Search movie
8. Movies sorted by rating
9. Create Rating Histogram 
        """)

        MR.update(get_user_input_colorized("Enter choice 1-9: "))
    
        get_user_input_colorized("Press Enter to continue")


if __name__ == "__main__":
    MR = MovieRank()
    main()
