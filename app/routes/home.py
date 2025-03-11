from flask import Blueprint, jsonify, render_template

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    return render_template('home/index.html')

# @app.route('/about')
# def about():
#     return render_template('about.html')
