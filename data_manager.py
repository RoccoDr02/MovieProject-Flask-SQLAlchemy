from models import db, User, Movie
import requests

API_KEY = "a8e97f74"
BASE_URL = "http://www.omdbapi.com/"
POSTER_URL = "http://img.omdbapi.com/"


def fetch_movie_from_omdb(title):
    """Fetch a movie from OMDB API."""
    params = {"apikey": API_KEY, "t": title}
    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        raise Exception("OMDb API error")

    data = response.json()
    if data.get("Response") == "False":
        raise Exception(f"Movie not found: {title}")

    imdb_id = data.get("imdbID")

    year_str = data.get("Year", "0")
    if "–" in year_str:
        year_str = year_str.split("–")[0]
    try:
        year = int(year_str)
    except ValueError:
        year = 0

    return {
        "title": data["Title"],
        "year": year,
        "rating": float(data["imdbRating"]) if data["imdbRating"] != "N/A" else 0.0,
        "poster_url": f"{POSTER_URL}?apikey={API_KEY}&i={imdb_id}" if imdb_id else ""
    }


class DataManager:
    def __init__(self, db_session):
        self.session = db_session

    def add_user(self, username):
        user = User(username=username)
        self.session.add(user)
        self.session.commit()
        return user

    def get_user_by_id(self, user_id):
        return User.query.get(user_id)

    def get_all_users(self):
        return User.query.all()

    def update_user(self, user_id, new_username):
        user = User.query.get(user_id)
        if user:
            user.username = new_username
            self.session.commit()
        return user

    def delete_user(self, user_id):
        user = User.query.get(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
        return user


    def add_movie(self, title, user_id):
        movie_data = fetch_movie_from_omdb(title)

        movie = Movie(
            title=movie_data["title"],
            user_id=user_id,
            # year=movie_data["year"],
            # rating=movie_data["rating"],
            poster_url=movie_data["poster_url"]
        )
        self.session.add(movie)
        self.session.commit()
        return movie

    def get_movie_by_id(self, movie_id):
        return Movie.query.get(movie_id)

    def get_movies_by_user(self, user_id):
        return Movie.query.filter_by(user_id=user_id).all()

    def update_movie(self, movie_id, new_title=None, new_user_id=None):
        movie = Movie.query.get(movie_id)
        if movie:
            if new_title:
                movie.title = new_title
            if new_user_id:
                movie.user_id = new_user_id
            self.session.commit()
        return movie

    def delete_movie(self, movie_id):
        movie = Movie.query.get(movie_id)
        if movie:
            self.session.delete(movie)
            self.session.commit()
        return movie

