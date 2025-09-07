from flask import Flask, render_template, request, redirect, url_for, abort
from data_manager import DataManager
from models import db, Movie
import os

app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))
db_dir = os.path.join(basedir, 'movie_data')
os.makedirs(db_dir, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(db_dir, 'movies3.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
data_manager = DataManager(db_session=db.session)


@app.route('/')
def home():
    users = data_manager.get_all_users()
    return render_template('index.html', users=users)

@app.route('/users', methods=['POST'])
def add_user():
    username = request.form['username']
    try:
        data_manager.add_user(username)
    except Exception as e:
        return render_template('error.html', error=f"Fehler beim Hinzufügen des Users: {e}")
    return redirect(url_for('home'))

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = data_manager.get_user_by_id(user_id)
    if not user:
        abort(404, description="User not found")
    try:
        data_manager.delete_user(user_id)
    except Exception as e:
        return render_template('error.html', error=f"Fehler beim Löschen des Users: {e}")
    return redirect(url_for('home'))

@app.route('/users/<int:user_id>/movies', methods=['GET'])
def user_movies(user_id):
    user = data_manager.get_user_by_id(user_id)
    if not user:
        abort(404, description="User not found")
    movies = data_manager.get_movies_by_user(user_id)
    return render_template('movies.html', user=user, movies=movies)

@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    user = data_manager.get_user_by_id(user_id)
    if not user:
        abort(404, description="User not found")
    title = request.form['title']
    try:
        data_manager.add_movie(title, user_id)
    except Exception as e:
        return render_template('error.html', error=f"Fehler beim Hinzufügen des Films: {e}")
    return redirect(url_for('user_movies', user_id=user_id))

@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    try:
        new_rating = float(request.form['new_rating'])
        movie = data_manager.update_movie_rating(movie_id, new_rating)
        if not movie:
            return "Movie not found", 404
    except Exception as e:
        return f"Error updating movie: {str(e)}", 500

    return redirect(url_for('user_movies', user_id=user_id))

@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    movie = data_manager.get_movie_by_id(movie_id)
    if not movie:
        abort(404, description="Movie not found")
    try:
        data_manager.delete_movie(movie_id)
    except Exception as e:
        return render_template('error.html', error=f"Fehler beim Löschen des Films: {e}")
    return redirect(url_for('user_movies', user_id=user_id))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error=e), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('error.html', error=e), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
