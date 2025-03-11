from flask import Blueprint, render_template
from flask import render_template, redirect, url_for, session, request
from flask_login import login_user, logout_user, login_required

from ..models import User
from ..extensions import db, bcrypt, login_manager

# Create instance
auth_bp = Blueprint('auth', __name__)

# User loader to get user object from the session when a request is made
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register account
@auth_bp.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        password_confirm = request.form["password_confirm"]

        if password != password_confirm:
            return render_template("auth/register-not-confirmed.html")

        # Hashing password
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(username = username, email = email, password = hashed_password, name = username, admin = False)
        db.session.add(new_user)
        db.session.commit()
        print(username)
        print(password)
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html")

# Log in
@auth_bp.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username = username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            session["username"] = username
            return redirect(url_for("home.index"))
    return render_template("auth/login.html")

# Page to do something that require registered user session
@auth_bp.route("/forgot_password", methods = ["GET", "POST"])
def forgot_password(): # Endpoint of this route is forgot_password, which is the function's name
    if request.method == "POST":
        email = request.form["email"]
        return render_template("result.html")
    return render_template("auth/forgot_password.html")