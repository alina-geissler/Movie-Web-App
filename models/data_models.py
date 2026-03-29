from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    user_name = db.Column(db.String(100), nullable=False)


class Movie(db.Model):
    __tablename__ = 'movies'
    movie_id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    movie_title = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(100))  # TODO: nullable?
    release_year = db.Column(db.Integer)  # TODO: nullable?
    poster_url = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    user = db.relationship('User', backref='movies')


