from app import app
from models import db, User

db.drop_all()
db.create_all()

def create_user_data():
    """Inserts test user data to collablog users table"""

    users = [
        {
            "first_name": "Victor",
            "last_name": "Kim",
            "about": "I went to WTS"
        },
        {
            "first_name": "David",
            "last_name": "Jo",
            "about": "I went to CUNY"
        },
        {
            "first_name": "Gilbert",
            "last_name": "Salas",
            "about": "I went to CUNY"
        },
    ]

    for user_data in users:

        # Double asterisks unpacks a dictionary
        # into keyword arguments in function call

        user = User(**user_data)
        db.session.add(user)

    db.session.commit()

create_user_data()