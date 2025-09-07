from flask import Flask
from data_manager import DataManager
from models import db, Movie
import os
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies2.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

data_manager = DataManager(db_session=db.session)

@app.route('/')
def home():
    return "Welcome to the Movie Web App!"



"""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    
CREATE TABLE user_favorites (
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, movie_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
);
"""



if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)