"""Models for Collablog."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/img/1672"

class User(db.Model):
    """Collablog user"""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    first_name = db.Column(
        db.String(25),
        nullable=False
    )

    last_name = db.Column(
        db.String(35),
        nullable=False
    )

    about = db.Column(
        db.Text,
        nullable=False,
    )

    image_url = db.Column(
        db.Text,
        nullable=False,
        default=DEFAULT_IMAGE_URL
    )


def connect_db(app):
    """Connects this database to Collablog flask app"""

    app.app_context().push()
    db.app = app
    db.init_app(app)