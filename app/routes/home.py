from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required
from app.models import Personal_Stat
from flask_login import current_user

from ..extensions import db
from ..models import User

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def intro():
    return render_template('home/intro.html')

@home_bp.route('/homepage')
def homepage():
    return render_template('home/homepage.html')

@home_bp.route('/about')
def about():
    return render_template('home/about_us.html')

@home_bp.route('/set-goal', methods = ["GET", "POST"])
def set_goal():
    if request.method == "POST":
        new_goal = request.form.get("goal")
        User.update_goal(user_id = current_user.user_id, new_goal = new_goal)
        return render_template("home/homepage.html")
    return render_template("home/set_goal.html")

@home_bp.route('/profile', methods = ["GET", "POST"])
@login_required
def profile():
    stat = Personal_Stat.query.filter_by(user_id=current_user.user_id).first()

    if request.method == "POST":
        weight = request.form.get("weight", type=float)
        height = request.form.get("height", type=float)
        age = request.form.get("age", type=int)

        if stat:
            stat.weight = weight
            stat.height = height
            stat.age = age
        else:
            stat = Personal_Stat(user_id=current_user.user_id, weight=weight, height=height, age=age)
            db.session.add(stat)

        db.session.commit()
        return redirect(url_for("home.profile"))

    return render_template("home/profile.html", username=current_user.username, personal_stat=stat)

@home_bp.route('/statistics')
def statistics():
    return render_template('home/statistics.html')