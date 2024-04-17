"""Collablog application."""

import os

from flask import Flask, request
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///collablog')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sUp37$EcREtK3Y-c0lL@bLOG'
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
