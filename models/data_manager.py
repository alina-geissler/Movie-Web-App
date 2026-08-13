"""
Data access layer for CineStash movie app CRUD operations.
Centralizes database logic for User and Movie models.
"""

from sqlalchemy.exc import SQLAlchemyError

from .data_models import db, User, Movie


class DataManager:

    @staticmethod
    def create_user(name):
        """
        Create a new user in the database.
        Raise SQLAlchemyError if database operation fails.
        :param name: User's display name (max 100 chars)
        """
        new_user = User(name=name)
        try:
            db.session.add(new_user)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise

    @staticmethod
    def get_users():
        """
        Fetch all users from the database.
        :return: complete list of all users
        """
        users = User.query.all()
        return users

    @staticmethod
    def delete_user(user_id):
        """
        Delete a user from the database.
        Raise SQLAlchemyError if database operation fails.
        :param user_id: ID of the user to delete
        """
        try:
            user_to_delete = db.session.get(User, user_id)
            if user_to_delete:
                db.session.delete(user_to_delete)
                db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise

    @staticmethod
    def get_movies(user_id):
        """
        Fetch all movies for a specific user.
        :param user_id: ID of the user whose movies to retrieve
        :return: complete list of movies owned by the specific user
        """
        movies = Movie.query.filter_by(user_id=user_id)
        return movies

    @staticmethod
    def add_movie(movie):
        """
        Add a new movie to the database.
        Raise SQLAlchemyError if database operation fails.
        :param movie: movie instance to persist
        """
        try:
            db.session.add(movie)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise

    @staticmethod
    def update_movie_title(movie_id, new_title):
        """
        Update the title of an existing movie.
        Raise SQLAlchemyError if database operation fails.
        :param movie_id: ID of the movie to update
        :param new_title: new title for the movie
        """
        try:
            movie_to_update = db.session.get(Movie, movie_id)
            if movie_to_update:
                movie_to_update.title = new_title
                db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise

    @staticmethod
    def update_movie_rating(movie_id, new_rating):
        """
        Update the rating of an existing movie.
        Raise SQLAlchemyError if database operation fails.
        :param movie_id: ID of the movie to update
        :param new_rating: new rating for the movie
        """
        try:
            movie_to_update = db.session.get(Movie, movie_id)
            if movie_to_update:
                movie_to_update.rating = new_rating
                db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise

    @staticmethod
    def delete_movie(movie_id):
        """
        Delete a movie from the database.
        Raise SQLAlchemyError if database operation fails.
        :param movie_id: ID of the movie to delete
        """
        try:
            movie_to_delete = db.session.get(Movie, movie_id)
            if movie_to_delete:
                db.session.delete(movie_to_delete)
                db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
