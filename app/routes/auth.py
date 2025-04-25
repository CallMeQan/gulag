from os import getenv
from flask import Blueprint, jsonify, render_template
from flask import render_template, redirect, url_for, session, request
from flask_login import login_user, login_required, logout_user
import time, hmac, hashlib

import datetime

from ..models import User, User_Login_Check, Forgot_Password, Mobile_Session
from ..extensions import db, bcrypt, login_manager
from ..modules.forgot_module import send_email

auth_bp = Blueprint('auth', __name__)

def generate_timestamp_token() -> str:
    """
    Generate a reset token using HMAC with SHA256.
    The token is created by hashing the current timestamp with a secret key.
    """
    timestamp = str(int(time.time()))
    token = hmac.new(getenv("SECRET_KEY").encode(), timestamp.encode(), hashlib.sha256)
    return token.hexdigest()

def generate_email_hash(email: str) -> str:
    """
    Generate a hash for email using HMAC with SHA256.
    This is reversible so it's good as an alternative to B-Crypt to store email.
    """
    secret = getenv("SECRET_KEY")
    if not secret:
        raise ValueError("SECRET_KEY environment variable not set")
    hashed_email = hmac.new(secret.encode(), str(email).encode(), hashlib.sha256)
    return hashed_email.hexdigest()

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

        # Error handling
        if "" in [username, email, password, password_confirm]:
            return jsonify({"error": "Please input all the essential fields"}), 404
        
        # Hashing password
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        hashed_email = generate_email_hash(email)

        # Check if confirm password is correct
        if password != password_confirm:
            return jsonify({"error": "The password and confirm must be the same"}), 404
        
        # Check if username or email is duplicated
        if User.is_duplicate(username = username, email = hashed_email):
            return jsonify({"error": "The username or email is duplicated"}), 404

        new_user = User(username = username, email = hashed_email, password = hashed_password, name = username, admin = False, goal = 1)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html")

# Log in
@auth_bp.route("/login", methods = ["GET", "POST"])
def login():
    # Get user to homepage if already login
    user = session.get("user")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Error handling
        if "" in [username, password]:
            return jsonify({"error": "Please input all the essential fields"}), 404
        right_password = bcrypt.check_password_hash(user.password, password)
        
        user = User.query.filter_by(username = username).first()

        repeat_below_5 = True
        if not right_password:
            repeat_below_5 = User_Login_Check.record_attempt(username = username)

        if repeat_below_5 and user:
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

        # Error handling
        if email == "":
            return jsonify({"error": "Please input all the essential fields"}), 404
        hashed_email = generate_email_hash(email)

        # Check if email is valid
        print(f"\n\n\n{email}\n\n\n")
        if not User.email_exist(email = hashed_email):
            return render_template("auth/email_not_found.html")
        
        hashed_timestamp = generate_timestamp_token()

        # Tạo link reset password, ví dụ: /recover-password?a=token
        reset_link = url_for('auth.recover_password', token = hashed_timestamp, _external = True)

        created_at = datetime.datetime.now()
        new_request = Forgot_Password(email = hashed_email, created_at = created_at, hashed_timestamp = hashed_timestamp)
        db.session.add(new_request)
        db.session.commit()

        # Send email (not hashed)
        # send_email(restore_link = reset_link, client_email = email)
        return render_template("auth/email_sent.html", email = email)
    return render_template("auth/forgot_password.html")

@auth_bp.route("/recover-password?a=<token>", methods = ["GET", "POST"])
def recover_password(token):
    """
    Recover password function.
    This function is used to recover the user's password.
    The function takes a token as an argument, which is used to verify the user's identity.
    """
    # print(token)
    hashed_email = Forgot_Password.take_email_from_hash(hashed_timestamp = token)

    if hashed_email is None:
        return "The link is not valid! Please come back again later."

    # Login
    if request.method == "POST":
        new_password = request.form["new_password"]
        hashed_password = bcrypt.generate_password_hash(new_password).decode("utf-8")
        
        User.update_password(email = hashed_email, new_password = hashed_password)
        return "Successfully changed password. Please log in!"
    return render_template("auth/recover_password.html", email = hashed_email)

@auth_bp.route("/mobile_check", methods = ["GET", "POST"])
def mobile_check():
    """
    Mobile sign in check.
    This function is used to check if the user can sign in using the mobile app.
    """
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Error handling
        if "" in [email, password]:
            return jsonify({"error": "Please input all the essential fields"}), 404
        hashed_email = generate_email_hash(email)

        user = User.email_exist(email = hashed_email)

        if user and bcrypt.check_password_hash(user.password, password):
            hashed_timestamp = generate_timestamp_token()
            created_at = datetime.datetime.now()

            # Create session or add them
            Mobile_Session.create_session(user_id = user.user_id, created_at = created_at, hashed_timestamp = hashed_timestamp)
            
            # Send the token to mobile app.
            return jsonify({"hashed_timestamp": hashed_timestamp, "user_id": user.user_id}), 200
        return jsonify({"error": "Invalid email or password"}), 401
    return jsonify({"error": "Invalid request method"}), 405

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop('user', None)
    session.clear()
    return redirect(url_for("auth.login"))