from flask import Blueprint, render_template
from flask import render_template, redirect, url_for, session, request
from flask_login import login_user, logout_user, login_required
import time, hmac, hashlib

import os
from dotenv import load_dotenv

from ..models import User
from ..extensions import db, bcrypt, login_manager

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
    return token, timestamp

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
            return redirect(url_for("home.index"))
    # If method is GET, return to login.html
    return render_template("auth/login.html")

# Page to do something that require registered user session
@auth_bp.route("/forgot_password", methods = ["GET", "POST"])
def forgot_password(): # Endpoint of this route is forgot_password, which is the function's name
    if request.method == "POST":
        email = request.form["email"]

        # Check if email is valid
        if not User.query.filter_by(email = email).first():
            return render_template("auth/register.html")
        
        # Generate reset token and timestamp
        token, ts = generate_reset_token()

        # Tạo link reset password, ví dụ: /email-forgot-password?a=token
        reset_link = url_for('reset_password', a=token, _external=True) # INT 129438200

        # TODO: Save token and timestamp to database or cache for later verification
        new_request = Forgot_Password(email = email, token = token)
        db.session.add(new_request)
        db.session.commit()

        # TODO: Gửi email chứa reset_link tới user
        
        return f"Reset link sent to your email: {reset_link}"
    
    return render_template("auth/forgot_password.html")

@auth_bp.route("/email-forgot-password", methods=["GET", "POST"])
def reset_password():
    token = request.args.get("a")
    # TODO: Xác thực token và kiểm tra thời gian hợp lệ (ví dụ: token hết hạn sau 1 giờ)
    if request.method == "POST":
        new_password = request.form.get("password")
        # TODO: Lưu mật khẩu mới sau khi đã xác nhận token hợp lệ
        return "Password has been reset successfully!"
    return render_template("reset_password.html", token=token)