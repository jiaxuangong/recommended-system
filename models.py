from exts import db
from datetime import datetime
from sqlalchemy import Text
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import JSON

class MovieModel(db.Model):
    __tablename__ = "movie_infor"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255))
    time = db.Column(db.String(255))
    genre = db.Column(db.String(255))
    release_time = db.Column(db.String(255))
    intro = db.Column(db.Text)
    directors = db.Column(db.String(255))
    writers = db.Column(db.String(255))
    starts = db.Column(db.String(255))


class UserModel(db.Model):
    __tablename__ = "movie_users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now)
    viewed_movies = db.Column(db.String(255), nullable=True)