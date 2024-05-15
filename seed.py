from app import app
from models import db, User, Post, DEFAULT_IMAGE_URL

db.drop_all()
db.create_all()


def create_user_data():
    """Inserts test user data to collablog users table"""

    users = [
        {
            "first_name": "Victor",
            "last_name": "Kim",
            "about": "I went to WTS",
            "posts": [
                {"title": "Victor Kim's first post",
                 "blurb": "This is Victor Kim's first post",
                 "content": "This is the content for the first post"
                 },
                {"title": "Victor Kim's second post",
                 "blurb": "This is Victor Kim's second post",
                 "content": "This is the content for the second post"
                 },
                {"title": "Victor Kim's third post",
                 "blurb": "This is Victor Kim's third post",
                 "content": "This is the content for the third post"
                 }
            ]
        },
        {
            "first_name": "David",
            "last_name": "Jo",
            "about": "I went to CUNY",
            "posts": [
                {"title": "David Jo's first post",
                 "blurb": "This is David Jo's first post",
                 "content": "This is the content for the first post"
                 },
                {"title": "David Jo's second post",
                 "blurb": "This is David Jo's second post",
                 "content": "This is the content for the second post"
                 },
                {"title": "David Jo's third post",
                 "blurb": "This is David Jo's third post",
                 "content": "This is the content for the third post"
                 }
            ]
        },
        {
            "first_name": "Gilbert",
            "last_name": "Salas",
            "about": "I went to CUNY",
            "posts": [
                {"title": "Gilbert Salas's first post",
                 "blurb": "This is Gilbert Salas's first post",
                 "content": "This is the content for the first post"
                 },
                {"title": "Gilbert Salas's second post",
                 "blurb": "This is Gilbert Salas's second post",
                 "content": "This is the content for the second post"
                 },
                {"title": "Gilbert Salas's third post",
                 "blurb": "This is Gilbert Salas's third post",
                 "content": "This is the content for the third post"
                 }
            ]
        },
    ]

    for user_data in users:
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            about=user_data['about'],
            image_url=user_data.get('image_url', DEFAULT_IMAGE_URL)
        )
        db.session.add(user)
        db.session.commit() 

        for post_data in user_data.get('posts', []):
            post = Post(
                title=post_data['title'],
                blurb=post_data['blurb'],
                content=post_data['content'],
                user=user
            )
            db.session.add(post)
            db.session.commit()


create_user_data()
