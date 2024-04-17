"""Collablog application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///collablog')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sUp37$EcREtK3Y-c0lL@bLOG'
app.config['SQLALCHEMY_ECHO'] = True


toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.get('/')
def root():
    """Homepage redirects to list of users"""

    return redirect("/users")


################################################################################
# User Route
################################################################################

@app.get('/users')
def users_index():
    """Displays page with information on all Collablog users"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)

@app.get('/users/new')
def users_new():
    """Displays page with form to create a new Collablog user"""


@app.post('/users/new')
def users_new_submit():
    """Handles form submission for creating a new Collablog user"""

@app.get('/users/<int:user_id>')
def users_display_user():
    """Displays page for specific user information"""

@app.get('/users/<int:user_id>/edit')
def users_edit_user():
    """Displays edit page for specific user"""


@app.post('/users/<int:user_id>/edit')
def users_edit_user_submit():
    """Handles user edit form submission, returns user to /users page"""

@app.post('/users/<int:user_id>/delete')
def users_delete_user():
    """Handles user edit form delete submission, returns user to /users page"""