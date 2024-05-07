"""Flask Notes App."""

from models import db, User
import os

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from dotenv import load_dotenv
load_dotenv()

# from forms import

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///flask_notes")
app.config["SQLALCHEMY_ECHO"] = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
db.init_app(app)

app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

app.app_context().push()
db.create_all()

toolbar = DebugToolbarExtension(app)

# routes next!
