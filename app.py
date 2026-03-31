"""
CineStash: Flask movie collection manager.

Fetches movie data from OMDb API, stores in SQLite via SQLAlchemy.
CRUD operations for users and personal movie collections.
Responsive Bootstrap frontend.

See README.md for setup and features.
"""

import os

from dotenv import load_dotenv
from flask import flash, Flask, render_template, request, redirect, url_for
import requests
from sqlalchemy.exc import SQLAlchemyError

from models.data_manager import DataManager
from models.data_models import db, Movie, User

load_dotenv()

OMDB_API_KEY = os.getenv('OMDB_API_KEY')

REQUEST_DATA_URL = f'https://www.omdbapi.com/?apikey={OMDB_API_KEY}&type=movie&t='

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

data_manager = DataManager()


@app.route('/')
def index():
    """
    Display the users overview page.
    Load all users and render the index template.
    :return: rendered template with users list or with flash message if db query fails
    """
    try:
        users = data_manager.get_users()
    except SQLAlchemyError:
        flash('Could not load users. Please try again.', 'danger')
        users = []
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user from POST form data.
    :return: redirect to index page after success/failure with appropriate flash message
    """
    new_user = request.form['new_user']
    try:
        data_manager.create_user(new_user)
        flash(f'User {new_user} created successfully!', 'success')
        return redirect(url_for('index'))
    except SQLAlchemyError:
        flash('Could not create new user. Please try again.', 'danger')
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def list_movies(user_id):
    """
    Display all movies for a specific user.
    :param user_id: ID of user whose movies to display
    :return: rendered 'movies.html' with user and their movies if success
    or redirect to index page if db query fails (+ appropriate flash message)
    """
    try:
        user = db.session.get(User, user_id)
        if not user:
            flash('User not found! Please use a valid user ID or select a user from the list below.')
            return redirect(url_for('index'))
        user_movies = data_manager.get_movies(user_id)
        if user_movies.count() == 0:
            flash('No movies in the database yet. Start collecting!', 'warning')
        else:
            flash(f'{user_movies.count()} movie(s) in the collection.', 'success')
    except SQLAlchemyError:
        flash('Could not load movies. Please try again.', 'danger')
        return redirect(url_for('index'))
    return render_template('movies.html', movies=user_movies, user=user)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """
    Add a new movie to user's collection via OMDb API lookup.
    Get movie title to add and optional release year from POST form.
    :param user_id: ID of user to add movie for
    :return: redirect to movies page with success/error flash message
    """
    movie_to_add = request.form.get('new_movie')
    year = request.form.get('release_year')
    if not OMDB_API_KEY:
        flash('OMDb API key is missing!', 'danger')
        return redirect(url_for('list_movies', user_id=user_id))
    request_url = REQUEST_DATA_URL + movie_to_add + (f'&y={year}' if year else '')

    try:
        res = requests.get(request_url, timeout=(3.0, 5.0))  # timeout: 3s connect, 5s read
        movie_info = res.json()
        if movie_info.get("Error") == "Movie not found!":
            flash('No matching movie found to add.', 'danger')
            return redirect(url_for('list_movies', user_id=user_id))
        elif movie_info.get("Error") == "Invalid API key!":
            flash('OMDb API key is invalid! ', 'danger')
            return redirect(url_for('list_movies', user_id=user_id))
        res.raise_for_status()
    except requests.exceptions.Timeout:
        flash('OMDb timeout: Server too slow.', 'danger')
        return redirect(url_for('list_movies', user_id=user_id))
    except requests.exceptions.ConnectionError:
        flash('OMDb not reachable.', 'danger')
        return redirect(url_for('list_movies', user_id=user_id))
    except requests.exceptions.HTTPError:
        flash('OMDb HTTP error.', 'danger')
        return redirect(url_for('list_movies', user_id=user_id))
    except requests.exceptions.JSONDecodeError:
        flash('Invalid response from OMDb.', 'danger')
        return redirect(url_for('list_movies', user_id=user_id))
    except requests.exceptions.RequestException:
        flash(f'OMDb error occured.', 'danger')
        return redirect(url_for('list_movies', user_id=user_id))

    title = movie_info.get('Title', movie_to_add)
    director = movie_info.get('Director') if movie_info.get('Director') != 'N/A' else None
    # parse release year: must be exactly 4 digits (e.g. "2019"); reject "2017-2019" or "N/A"
    year_str = movie_info.get('Year', 'N/A')
    if year_str != 'N/A' and len(year_str) == 4 and year_str.isdigit():
        release_year = int(year_str)
    else:
        release_year = None
    if not release_year and year:
        try:
            release_year = int(year)  # HTML input type="number" expected; validate in any case
        except ValueError:
            pass
    # extract poster URL; validity checked via HTML <img> onerror fallback
    poster_url = movie_info.get('Poster') if movie_info.get('Poster') != 'N/A' else None

    movie = Movie(
        title=title,
        director=director,
        release_year=release_year,
        poster_url=poster_url,
        user_id=user_id
    )
    try:
        data_manager.add_movie(movie)
        flash(f'Movie "{title}" added successfully!', 'success')
    except SQLAlchemyError:
        flash('Could not save movie. Please try again.', 'danger')
    return redirect(url_for('list_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """
    Update movie title via POST form.
    :param user_id: ID of user to update movie for
    :param movie_id: ID of movie to update
    :return: redirect to movie page with success/error flash message
    """
    try:
        new_title = request.form['update_movie']
        data_manager.update_movie(movie_id, new_title)
        flash(f'Movie "{new_title}" updated successfully!', 'success')
    except SQLAlchemyError:
        flash('Could not update movie. Please try again.')
    return redirect(url_for('list_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """
    Delete movie by ID via POST request.
    :param user_id: ID of user to delete movie for
    :param movie_id: ID of movie to delete
    :return: redirect to movie page with success/error flash message
    """
    try:
        movie_to_delete = Movie.query.get_or_404(movie_id)
        data_manager.delete_movie(movie_id)
        flash(f'Movie "{movie_to_delete.title}" deleted successfully!', 'success')
    except SQLAlchemyError:
        flash('Could not delete movie. Please try again.', 'danger')
    return redirect(url_for('list_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(error):
    """
    Custom 404 error handler.
    :return: rendered 404.html with 404 status
    """
    return render_template('404.html'), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """
    Custom 405 error handler.
    :return: rendered 405.html with 405 status
    """
    return render_template('405.html'), 405


@app.errorhandler(500)
def internal_server_error(error):
    """
    Custom 500 error handler.
    :return: rendered 500.html with 500 status
    """
    return render_template('500.html'), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # only creates the tables if they do not already exist

    app.run(host="0.0.0.0", port=5000, debug=False)
