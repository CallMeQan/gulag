from os import getenv
from flask import Blueprint, jsonify, render_template
from flask import render_template, redirect, url_for, session, request
from flask_login import login_user
import time, hmac, hashlib

import datetime

from ..models import User, Forgot_Password, Mobile_Session
from ..extensions import db, bcrypt, login_manager
from ..modules.forgot_module import send_email

auth_bp = Blueprint('auth', __name__)

def generate_token() -> str:
    """
    Generate a reset token using HMAC with SHA256.
    The token is created by hashing the current timestamp with a secret key.
    """
    timestamp = str(int(time.time()))
    token = hmac.new(getenv("SECRET_KEY"), timestamp.encode(), hashlib.sha256)
    return token.hexdigest()

@login_manager.user_loader
def load_user(user_id):
    """
    Load a user from the database using the user_id stored in the session.
    This function is used by Flask-Login to retrieve the user object for the current session.
    """
    return User.query.get(int(user_id))

# Register account
@auth_bp.route("/register", methods = ["GET", "POST"])
def register():
    """
    Register a new user account.
    """
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        password_confirm = request.form["password_confirm"]

        # Check if confirm password is correct
        if password != password_confirm:
            return render_template("auth/register-not-confirmed.html")
        
        # Check if username or email is duplicated
        if User.is_duplicate(username = username, email = email):
            return render_template("auth/register-duplicated.html")

        # Hashing password
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(username = username, email = email, password = hashed_password, name = username, admin = False)
        db.session.add(new_user)
        db.session.commit()
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
            # Save user data to session
            session["user"] = {
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email
            }
            login_user(user)
            return redirect(url_for("home.homepage"))
    return render_template("auth/login.html")

@auth_bp.route("/forgot-password", methods = ["GET", "POST"])
def forgot_password():
    """
    Forgot password function.
    This function is used to send a reset password link to the user's email.
    The link contains a token that is used to verify the user's identity.
    The token is generated using HMAC with SHA256 based on the current timestamp and a secret key.
    """
    if request.method == "POST":
        email = request.form["email"]

        # Check if email is valid
        if not User.query.filter_by(email = email).first():
            return render_template("auth/register.html")
        
        hashed_timestamp = generate_token()

        # Tạo link reset password, ví dụ: /recover-password?a=token
        reset_link = url_for('auth.recover_password', token = hashed_timestamp, _external = True)

        created_at = datetime.datetime.now()
        new_request = Forgot_Password(email = email, created_at = created_at, hashed_timestamp = hashed_timestamp)
        db.session.add(new_request)
        db.session.commit()

        send_email(restore_link = reset_link, client_email = email)
        return f"Reset link sent to your email: {email}"
    
    return render_template("auth/forgot_password.html")

@auth_bp.route("/recover-password?a=<token>", methods = ["GET", "POST"])
def recover_password(token):
    """
    Recover password function.
    This function is used to recover the user's password.
    The function takes a token as an argument, which is used to verify the user's identity.
    """
    # print(token)
    email = Forgot_Password.take_email_from_hash(hashed_timestamp = token)

    if email is None:
        return "The link is not valid! Please come back again later."

    # Login
    if request.method == "POST":
        new_password = request.form["new_password"]
        hashed_password = bcrypt.generate_password_hash(new_password).decode("utf-8")
        
        User.update_password(email = email, new_password = hashed_password)
        return "Successfully changed password. Please log in!"
    return render_template("auth/recover_password.html", email = email)

@auth_bp.route("/mobile_check", methods = ["GET", "POST"])
def mobile_check():
    """
    Mobile sign in check.
    This function is used to check if the user can sign in using the mobile app.
    """
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email = email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            hashed_timestamp = generate_token()
            created_at = datetime.datetime.now()

            # Create session or add them
            Mobile_Session.create_session(user_id = user.user_id, created_at = created_at, hashed_timestamp = hashed_timestamp)
            
            # TODO: Send the token to mobile app.
            return jsonify({"token": hashed_timestamp, "user_id": user.user_id}), 200
        return jsonify({"error": "Invalid email or password"}), 401
    return jsonify({"error": "Invalid request method"}), 405