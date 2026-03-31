"""
Data Models for CineStash movie collection app.
Relationship: User 1:n Movie
Foreign Keys: movie.user_id → user.user_id
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)


class Movie(db.Model):
    __tablename__ = 'movies'
    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(100), nullable=True)
    release_year = db.Column(db.Integer, nullable=True)
    poster_url = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    user = db.relationship('User', backref='movies')


