from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()


# ==========================================
# 1. USER MODEL
# ==========================================
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)  # For storing secured passwords

    # 🌟 FIXED: Replaced deprecated datetime.utcnow with modern timezone-aware lambda
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship to link reviews to the user
    reviews = db.relationship('Review', backref='author', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"


# ==========================================
# 2. MOVIE MODEL
# ==========================================
class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    director = db.Column(db.String(100))
    genre = db.Column(db.String(100))
    release_year = db.Column(db.Integer)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))  # Path to movie poster asset
    rating = db.Column(db.Float, default=0.0)

    # Relationship to link reviews to the movie
    reviews = db.relationship('Review', backref='movie', lazy=True)

    def __repr__(self):
        return f"<Movie {self.title}>"


# ==========================================
# 3. REVIEW MODEL
# ==========================================
class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)


    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Foreign Keys connecting to Users and Movies
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)

    def __repr__(self):
        return f"<Review {self.rating}★ for Movie ID {self.movie_id}>"