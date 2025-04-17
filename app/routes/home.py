from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required
from app.models import Personal_Info
from flask_login import current_user
from ..extensions import db


home_bp = Blueprint('home', __name__)



# @app.route('/about')
# def about():
#     return render_template('about.html')

@home_bp.route('/homepage')
def homepage():
    return render_template('home/homepage.html')

@home_bp.route('/set-goal', methods = ["GET", "POST"])
def set_goal():
    if request.method == "POST":
        goal = request.form["goal"]
        print(goal)
        return render_template("home/homepage.html")
    return render_template("home/set_goal.html")


