import json
from pathlib import Path
import requests

class MovieAgent:

    def __init__(self,data_path):
        self.data_path = Path(data_path)
        self.movies = self.load_movies()

    def load_movies(self):
        if not self.data_path.exists():
            return []

        with open(self.data_path,'r') as file:
            return json.load(file)

    def save_movies(self):
        with open(self.data_path,'w') as file:
            json.dump(self.movies,file, incent=2)

    def add_movie(self,title,genre,rating,year,matched=False):
        movie = {
            "title":title,
            "genre":genre,
            "rating":rating,
            "year":year,
            "matched":matched
        }
        self.movies.append(movie)
        self.save_movies()

    def list_movies(self):
        return self.movies

    def search_by_genre(self,genre):
        return[
            movie for movie in self.movies
            if movie["genre"].lower() == genre.lower()
        ]

    def recommend(self, min_rating=8):
        return[
            movie for movie in self.movies
            if movie["rating"] >= min_rating
        ]

    def fetch_movie_details(self, title):
        url = "http://www.omdbapi.com/"
        params = {
            "t": title,
            "apikey": "f013a7e"
        }

        response = requests.get(url, params=params, timeout=5)

        if response.status_code != 200:
            return None

        data = response.json()

        if data.get("Response") != "True":
            return None

        return {
            "title": data["Title"],
            "genre": data["Genre"],
            "rating": float(data.get("imdbRating", 0)),
            "year": int(data.get("Year", 0)),
            "matched": True
        }


if __name__ == "__main__":
      agent = MovieAgent("data/movies.json")

      movie_name = input("Enter movie name: ")

      movie = agent.fetch_movie_details(movie_name)

      if movie:
          print("\n Movie found from API:")
          print(movie)
      else:
          print("\n Movie not found from API:")


