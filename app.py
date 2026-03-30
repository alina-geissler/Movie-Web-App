import os

from dotenv import load_dotenv
from flask import Flask
import requests

from models.data_manager import DataManager
from models.data_models import db, Movie, User

load_dotenv()

API_KEY = os.getenv('API_KEY')

REQUEST_DATA_URL = f'https://www.omdbapi.com/?apikey={API_KEY}&t='

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, '../data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app. This is the reason you need to import db from models

data_manager = DataManager()  # Create an object of your DataManager class


@app.route('/')
def index():
    pass


@app.route('/users', methods=['POST'])
def create_user():
    pass


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def list_movies():
    pass


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie():
    pass


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie():
    pass


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie():
    pass


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=5000, debug=True)
