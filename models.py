"""Models for Collablog."""

import datetime
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
        nullable=False,
        default=""
    )

    image_url = db.Column(
        db.Text,
        nullable=False,
        default=DEFAULT_IMAGE_URL
    )

    posts = db.relationship("Post", backref="user")

    @property
    def full_name(self):
        """Returns user's full name"""

        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """Collablog post"""

    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(50),
        nullable=False
    )

    blurb = db.Column(
        db.Text,
        nullable=False)

    content = db.Column(
        db.Text,
        nullable=False)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)

    @property
    def formatted_date(self):
        """Returns formatted date"""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")


class Tag(db.Model):
    """Tag for posts"""

    __tablename__ = "tags"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        backref="tags"
    )


class PostTag(db.Model):
    """Tag on a post"""

    __tablename__ = "posts_tags"

    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id'),
        primary_key=True
    )

    tag_id = db.Column(
        db.Integer,
        db.ForeignKey('tags.id'),
        primary_key=True
    )


def connect_db(app):
    """Connects this database to Collablog flask app"""

    app.app_context().push()
    db.app = app
    db.init_app(app)
