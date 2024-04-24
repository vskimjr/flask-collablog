"""Models for Collablog."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcSOmKqc9qEhdH_KLPbjhX7LeGkcHMFOjQBGFRSgW72y7NUmCSHP2leqi-1X6cHMn1yXMBuDwaqKugjuBnI"

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
        nullable=False
    )

    image_url = db.Column(
        db.Text,
        nullable=False,
        default=DEFAULT_IMAGE_URL
    )

    @property
    def full_name(self):
        """ Returns user's full name"""

        return f"{self.first_name} {self.last_name}"


def connect_db(app):
    """Connects this database to Collablog flask app"""

    app.app_context().push()
    db.app = app
    db.init_app(app)