"""Flask Notes App."""

from forms import RegistrationForm, LoginForm, CSRFProtectForm
from models import db, User
import os

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///flask_notes")
app.config["SQLALCHEMY_ECHO"] = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
db.init_app(app)

app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

app.app_context().push()
db.create_all()

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)


@app.get('/')
def redirect_to_register():
    """Redirect to the register route"""

    return redirect('/register')


@app.route('/register', methods=["GET", "POST"])
def show_registration():
    """Show the registration"""

    form = RegistrationForm()

    if form.validate_on_submit():

        new_user = User.register(form.username.data, form.password.data)
        new_user.email = form.email.data
        new_user.first_name = form.first_name.data
        new_user.last_name = form.last_name.data

        db.session.add(new_user)
        db.session.commit()

        flash(f"User {new_user.username} created!")

        return redirect(f"/users/{new_user.username}")

    else:
        return render_template("register.jinja", form=form)


@app.route('/login', methods=['GET', 'POST'])
def handle_login():
    """Show the login form and process logins"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            return redirect(f"users/{user.username}")

        else:
            form.username.errors = ["Incorrect username or password"]

    return render_template('login.jinja', form=form)


@app.get("/users/<username>")
def show_user_info(username):
    """Show information about user if the user is logged in."""

    user = db.get_or_404(User, username)

    if session.get('username') == username:
        form = CSRFProtectForm()

        return render_template("user_info.jinja", user=user, form=form)

    else:
        flash('Not logged in!')
        return redirect('/')


@app.post("/logout")
def logout_user():
    """Log user out of site and redirect to homepage."""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop("username", None)

    return redirect("/")
