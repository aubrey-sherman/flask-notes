"""Forms for flask notes"""

from wtforms import SelectField, PasswordField, EmailField
from flask_wtf import FlaskForm
from wtforms.validators import Length, InputRequired


class RegistrationForm(FlaskForm):
    """Form to register a new user"""

    username = SelectField(
        "Username",
        validators=[
            Length(min=1, max=20),
            InputRequired()
        ]
    )

    password = PasswordField("Password", validators=[InputRequired()])

    # TODO: does EmailField automatically validate the input was an email
    email = EmailField(
        "Email",
        validators=[Length(min=1, max=50)])

    first_name = SelectField(
        "First Name",
        validators=[Length(min=1, max=30)]
    )

    last_name = SelectField(
        "Last Name",
        validators=[Length(min=1, max=30)]
    )
