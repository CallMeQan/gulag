from flask import Blueprint, render_template, request

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    return render_template('home/index.html')

@home_bp.route('/homepage')
def homepage():
    return render_template('home/homepage.html')

@home_bp.route('/about')
def about():
    return render_template('home/about_us.html')

@home_bp.route('/set-goal', methods = ["GET", "POST"])
def set_goal():
    if request.method == "POST":
        goal = request.form["goal"]
        print(goal)
        return render_template("home/homepage.html")
    return render_template("home/set_goal.html")