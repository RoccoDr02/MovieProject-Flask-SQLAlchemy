from models import db, User, Movie


class DataManager:
    def __init__(self, db_sesion):
        self.session = db_sesion

    def add_user(self, name):
        user = User(name=name)
        self.session.add(user)
        self.session.commit()
        return user

    def get_user_by_id(self, id):
        return User.query.get(id)

    def get_all_users(self):
        return User.query.all()

    def update_user(self, id, new_name):
        user = User.query.get(id)
        if user:
            user.username = new_username
            self.session.commit()
        return user

    def delete_user(self, id):
        user = User.query.get(id)
        if user:
            self.session.delete(user)
            self.session.commit()
        return user

    def add_movie(self, title, year, director, user_id):
        movie = Movie(title=title, year=year, director=director, user_id=user_id)
        self.session.add(movie)
