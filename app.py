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