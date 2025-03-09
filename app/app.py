### IMPORT
from flask import Flask, render_template, redirect, url_for, session, request
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

from sqlalchemy.orm import Mapped, mapped_column

from .env import DATABASE_URI, SECRET_KEY

# ====================================================================== #

### MAIN
# Config
SESSION_TYPE = "filesystem" # Read doc for more info
app = Flask(__name__, static_folder = "static")
app.config.from_object(__name__)
app.secret_key = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
Session(app)

# Create objects
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# User loader to get user object from the session when a request is made
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define User table
class User(db.Model, UserMixin):
    __tablename__ = "users" # Do not use global var for performance
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    nickname: Mapped[str] = mapped_column(nullable=False)
    vip_status: Mapped[bool] = mapped_column()

# Create a database
with app.app_context():
    db.create_all()

# Homepage
@app.route("/")
def index():
    return render_template("index.html")

# Register account
@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        password_confirm = request.form["password_confirm"]

        if password != password_confirm:
            return render_template("register-not-confirmed.html")

        # Hashing password
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(username = username, email = email, password = hashed_password, nickname = username, vip_status = False)
        db.session.add(new_user)
        db.session.commit()
        print(username)
        print(password)
        return redirect(url_for("login"))
    return render_template("register.html")

# Log in
@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username = username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            session["username"] = username
            return redirect(url_for("index"))
    return render_template("login.html")

# # Log out
# @app.route("/logout")
# @login_required # Should not used in place of "username" in session
# def logout():
#     logout_user()
#     session.pop('username', None)
#     session.clear()
#     return redirect(url_for("login"))

# Page to do something that require registered user session
@app.route("/forgot_password", methods = ["GET", "POST"])
def forgot_password(): # Endpoint of this route is forgot_password, which is the function's name
    if request.method == "POST":
        email = request.form["email"]
        return render_template("result.html")
    return render_template("forgot_password.html")

# Run cmd: "flask --app app run"
if __name__ == "__main__":
    port_number = 5000
    print(app.url_map)
    app.run(debug = True, port = port_number)