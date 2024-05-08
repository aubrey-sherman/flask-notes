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

        # catch user trying to make duplicate username
        if db.session.get(User, form.username.data):
            flash(f"Username {form.username.data} already exists.")

        else:
            # TODO: Consider separation of concerns, moving db work to Models
            # Pass all data into register method, rather than partial data
            # Common pattern is adding in models, committing in route
            new_user = User.register(form.username.data, form.password.data)
            new_user.email = form.email.data
            new_user.first_name = form.first_name.data
            new_user.last_name = form.last_name.data

            db.session.add(new_user)
            db.session.commit()
            session['username'] = new_user.username

            flash(f"User {new_user.username} created!")

            return redirect(f"/users/{new_user.username}")

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

    # FIXME: Security hole; first check if the viewer is logged in, then authorized
    # Reorder logic so unauthorized users don't get any information from you
    user = db.get_or_404(User, username)

    current_user = session.get('username')

    if current_user == username:
        form = CSRFProtectForm()

        return render_template("user_info.jinja", user=user, form=form)

    elif current_user:
        flash("You're not authorized to view this page.")
        return redirect(f"/users/{current_user}")

    flash('Not logged in!')
    return redirect('/register')


@app.post("/logout")
def logout_user():
    """Log user out of site and redirect to homepage."""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop("username", None)

    # FIXME: Include a fail case here: What if you can't log out bc of a bad form?
    # Add an UnauthorizedError
    return redirect("/register")
