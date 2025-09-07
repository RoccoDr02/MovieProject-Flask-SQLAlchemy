from flask import Flask, render_template, request, redirect, url_for, render_template
from data_manager import DataManager
from models import db, Movie
import os
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_dir = os.path.join(basedir, 'movie_data')
os.makedirs(db_dir, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'movie_data/movies3.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
data_manager = DataManager(db_session=db.session)

@app.route('/')
def home():
    users = data_manager.get_all_users()
    return render_template('index.html', users=users)

@app.route('/users', methods=['GET'])
def list_users():
    users = data_manager.get_all_users()
    return render_template('index.html', users=users)

@app.route('/users', methods=['POST'])
def add_user():
    username = request.form['username']
    data_manager.add_user(username)
    return redirect(url_for('home'))

@app.route('/users/<int:user_id>/movies', methods=['GET'])
def user_movies(user_id):
    user = data_manager.get_user_by_id(user_id)
    movies = data_manager.get_movies_by_user(user_id)
    return render_template('movies.html', user=user, movies=movies)

@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    title = request.form['title']
    data_manager.add_movie(title, user_id)
    return redirect(url_for('user_movies', user_id=user_id))



if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)