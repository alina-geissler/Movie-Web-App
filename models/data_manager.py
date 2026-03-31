from sqlalchemy.exc import SQLAlchemyError

from .data_models import db, User, Movie


class DataManager:
    @staticmethod
    def create_user(name):
        new_user = User(name=name)
        try:
            db.session.add(new_user)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise


    @staticmethod
    def get_users():
        users = User.query.all()
        return users

    @staticmethod
    def get_movies(user_id):
        movies = Movie.query.filter_by(user_id=user_id)
        return movies

    @staticmethod
    def add_movie(movie):
        try:
            db.session.add(movie)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise

    @staticmethod
    def update_movie(movie_id, new_title):
        try:
            movie_to_update = db.session.get(Movie, movie_id)
            if movie_to_update:
                movie_to_update.title = new_title
                db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise

    @staticmethod
    def delete_movie(movie_id):
        try:
            movie_to_delete = db.session.get(Movie, movie_id)
            if movie_to_delete:
                db.session.delete(movie_to_delete)
                db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
