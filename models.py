"""Models for Flask-Notes App."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
dbx = db.session.execute

bcrypt = Bcrypt()


class User(db.Model):
    """Class for User."""

    __tablename__ = "users"

    username = db.mapped_column(
        db.String(20),
        primary_key=True
    )

    hashed_password = db.mapped_column(
        db.String(100),
        nullable=False
    )

    email = db.mapped_column(
        db.String(50),
        unique=True,
        nullable=False
    )

    first_name = db.mapped_column(
        db.String(30),
        nullable=False
    )

    last_name = db.mapped_column(
        db.String(30),
        nullable=False
    )

    @classmethod
    def register(cls, username, pwd):
        """Register user with hashed password and return user instance."""

        hashed = bcrypt.generate_password_hash(pwd).decode('utf8')

        # password value will be set to hashed password
        return cls(username=username, password=hashed)

    @classmethod
    def authenticate(cls, username, password):
        """
        Authenticate user based on username and password
        Return user instance with username and hashed password
        """

        q = db.select(cls).filter_by(username=username)
        user = dbx(q).scalar_one_or_none()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False
