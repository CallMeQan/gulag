from flask import Blueprint, render_template
from flask import render_template, redirect, url_for, session, request
from flask_login import login_user, logout_user, login_required
import time, hmac, hashlib

import datetime
import os
from dotenv import load_dotenv

from ..models import User, Forgot_Password
from ..extensions import db, bcrypt, login_manager
from ..modules.forgot_module import send_email

# env get
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

# Create instance
auth_bp = Blueprint('auth', __name__)

def generate_reset_token():
    # Lấy timestamp hiện tại
    timestamp = str(int(time.time()))
    # Tạo token hash bằng cách dùng HMAC kết hợp SECRET_KEY và timestamp
    token = hmac.new(SECRET_KEY.encode(), timestamp.encode(), hashlib.sha256).hexdigest()
    return token

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
        # Receive information
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username = username).first()

        # If the username is valid, and the password match, login user
        if user and bcrypt.check_password_hash(user.password, password):
            # Save user data to session
            session["user"] = {
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email
            }
            # Login and save session data
            login_user(user)
            return redirect(url_for("home.homepage"))
    # If method is GET, return to login.html
    return render_template("auth/login.html")

# Page to do something that require registered user session
@auth_bp.route("/forgot-password", methods = ["GET", "POST"])
def forgot_password(): # Endpoint of this route is forgot_password, which is the function's name
    if request.method == "POST":
        email = request.form["email"]

        # Check if email is valid
        if not User.query.filter_by(email = email).first():
            return render_template("auth/register.html")
        
        # Generate reset token and timestamp
        hashed_timestamp = generate_reset_token()

        # Tạo link reset password, ví dụ: /email-forgot-password?a=token
        reset_link = url_for('auth.recover_password', token = hashed_timestamp, _external = True) # INT 129438200

        # TODO: Save token and timestamp to database or cache for later verification
        created_at = datetime.datetime.now()
        new_request = Forgot_Password(email = email, created_at = created_at, hashed_timestamp = hashed_timestamp)
        db.session.add(new_request)
        db.session.commit()

        # TODO: Gửi email chứa reset_link tới user
        send_email(restore_link = reset_link, client_email = email)
        return f"Reset link sent to your email: {email}"
    
    return render_template("auth/forgot_password.html")

@auth_bp.route("/recover-password?a=<token>", methods = ["GET", "POST"])
def recover_password(token):
    # Get the email and check for validity (less than 1 hour)
    print(token)
    email = Forgot_Password.take_email_from_hash(hashed_timestamp = token)

    if email is None:
        return "The link is not valid! Please come back again later."

    # Changing password
    if request.method == "POST":
        # Get hashed timestamp token and updated password
        new_password = request.form["new_password"]
        hashed_password = bcrypt.generate_password_hash(new_password).decode("utf-8")
        
        # Save the password
        User.update_password(email = email, new_password = hashed_password)
        return "Successfully changed password. Please log in!"
    return render_template("auth/recover_password.html", email = email)