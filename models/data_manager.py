from .data_models import db, User, Movie


class DataManager:
    @staticmethod
    def create_user(name):
        new_user = User(user_name=name)
        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def get_users():
        users = User.query.all()
        return users

    @staticmethod
    def get_movies(user_id):
        user = User.query.get(user_id)
        movies = user.movies.all()
        return movies

    @staticmethod
    def add_movie(movie):
        db.session.add(movie)
        db.session.commit()

    @staticmethod
    def update_movie(movie_id, new_title):
        movie_to_update = Movie.query.get(movie_id)
        if movie_to_update:
            movie_to_update.movie_title = new_title
            db.session.commit()

    @staticmethod
    def delete_movie(movie_id):
        movie_to_delete = Movie.query.get(movie_id)
        if movie_to_delete:
            db.session.delete(movie_to_delete)
            db.session.commit()
