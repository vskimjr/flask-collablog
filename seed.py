from app import app
from models import db, User

db.drop_all()
db.create_all()

def create_user_data():
    """Inserts test user data to collablog users table"""

    users = [
        {"first_name": "Victor", "last_name": "Kim"},
        {"first_name": "David", "last_name": "Jo"},
        {"first_name": "Gilbert", "last_name": "Salas"},
    ]

    for user_data in users:

        # Double asterist unpacks a dictionary into keyword arguemtns in function call
        user = User(**user_data)
        db.session.add(user)

    db.session.commit()

def insert_users():
    """Inserts all users into collablog db users table"""
    create_user_data()


if __name__ == "__main__":
    db.init_app(app)
    with app.app_context():
        insert_users()