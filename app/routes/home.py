from flask import Blueprint, jsonify, render_template, request
import requests

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    return render_template('home/index.html')

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

@home_bp.route('/running')
def running():
    return render_template('home/running.html')

@home_bp.route('/pause-running')
def resume():
    return render_template('home/resume.html')

@home_bp.route('/congrats')
def congrats():
    return render_template('home/congrats.html')

@home_bp.route('/bad-news')
def bad_news():
    return render_template('home/bad_news.html')