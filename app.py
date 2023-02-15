from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from models import connect_db, db, User
from forms import RegisterForm, LoginForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask-feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "shhhhh"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.route("/")
def homepage():
    """Show homepage of feedback site."""

    return redirect('/register')


@app.route("/register", methods=["GET", "POST"])
def register():
    """Show page where user can register."""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(username, password, first_name, last_name, email)

        db.session.commit()
        session['username'] = user.username

        return render_template("register.html")

    else:
        return render_template("/register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login form and handle login"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()
