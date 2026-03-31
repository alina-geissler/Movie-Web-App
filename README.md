# :clapper: Movie-Web-App - CineStash

**Web Movie Collection Manager with OMDb API Integration**

A Flask web application to manage personal movie collections.  
This project is the **conceptual successor** to my earlier **CLI Movie-Project** extending 
its core idea into a **full web app** with OMDb API integration, multi-user support, 
full CRUD operations, and a responsive Bootstrap UI.

## :rocket: Live Demo

**This project is deployed on PythonAnywhere and can be accessed here:**    

https://ombe.pythonanywhere.com/  



## :sparkles: Features

- **Multi-User Support**: Each user has their own movie collection
- **OMDb API Integration**: Automatic movie data lookup (title, director, year, poster)
- **CRUD Operations**: Create/read/update/delete movies per user
- **Flash Messages**: Success/error feedback with Bootstrap styling
- **Movie Posters**: Automatic OMDb poster URLs with fallback image
- **Responsive Design**: Bootstrap 5 mobile-first frontend
- **Error Handling**: Comprehensive SQLAlchemy + requests exception handling
- **PRG Pattern**: POST/Redirect/GET for robust form handling

## :file_folder: Project Structure

```
Movie-Web-App/
├── data/
│   └── movies.db   # SQLite database
├── static/
│   ├── images/
│   │   └── fallback_poster.png # default movie poster
│   └── style.css
├── templates/
│   ├── base.html   # Bootstrap base template
│   ├── index.html   # users overview
│   ├── movies.html   # user movie collection
│   ├── 404.html
│   ├── 405.html
│   └── 500.html
├── models/
│   ├── data_models.py   # SQLAlchemy User/Movie models
│   └── data_manager.py   # CRUD data access layer
├── app.py   # main Flask application with all routes
├── .env   # store SECRET_KEY + OMDb API key
├── README.md
└── requirements.txt
```

## :wrench: Setup & Usage

1. **Clone the repository**   
`git clone ...`  
2. **Install virtual env**    
Windows: `python -m venv .venv`    
Linux / macOS: `python3 -m venv .venv`  
3. **Create data folder & database**  
Create folder:   
`mkdir data`  
Create database file:   
Windows PowerShell: `ni data\movies.db -fo`  
Windows CMD: `type nul > data\movies.db`   
Linux / macOS: `touch data/movies.db`
4. **Get free API key from https://www.omdbapi.com/**
5. **Generate a strong secret key, for example:**  
Windows: `python -c "import secrets; print(secrets.token_hex(32))"`  
Linux / macOS: `python3 -c "import secrets; print(secrets.token_hex(32))"`
6. **Create .env file in project root to store keys**   
SECRET_KEY='your_secret_key_here'  
OMDB_API_KEY='your_omdb_api_key_here'  
7. **Install dependencies**    
Windows: `pip install -r requirements.txt`    
Linux / macOS: `pip3 install -r requirements.txt`  
8. **Start the application**    
Windows: `python app.py`    
Linux / macOS: `python3 app.py`  
9. **Open in browser**    
`http://127.0.0.1:5000`  

## :clipboard: Routes & Features

| Route                                       | Method | Description                       |
|---------------------------------------------|--------|-----------------------------------|
| `/`                                         | GET    | Home: List all users              |
| `/users`                                    | POST   | Create new user                   |
| `/users/<user_id>/movies`                   | GET    | Show movies for specific user     |
| `/users/<user_id>/movies`                   | POST   | Add new movie via OMDb API lookup |
| `/users/<user_id>/movies/<movie_id>/update` | POST   | Update movie title                |
| `/users/<user_id>/movies/<movie_id>/delete` | POST   | Delete movie from collection      |

## :package: Dependencies
 
`flask` - Core web framework + routing    
`flask-sqlalchemy` - Database ORM integration   
`python-dotenv` - loads SECRET_KEY + OMDb key from .env   
`requests` - OMDb API HTTP client  
`sqlalchemy` - Core database toolkit  