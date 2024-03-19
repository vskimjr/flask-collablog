"""SQLAlchemy models for CollaBlog."""

from flask_sqlalchemy import SQLAlchemy

DEFAULT_IMAGE_URL = "https://tinyurl.com/y3rfozh8"

db = SQLAlchemy()

class User(db.Model):
    """CollaBlog user"""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    first_name = db.Column(
        db.String(30),
        nullable=False
    )

    last_name = db.Column(
        db.String(30),
        nullable=False
    )

    image_url = db.Column(
        db.Text,
        nullable=False,
        default=DEFAULT_IMAGE_URL
    )
