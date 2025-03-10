from flask import Blueprint, jsonify, render_template

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template('index.html')

@home_bp.route('/about')
def about():
    return render_template('about.html')

@home_bp.route('/login')
def login():
    return render_template('login.html')

@home_bp.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@home_bp.route('/register', methods=['POST'])
def register():
    return jsonify('djtmem')

@home_bp.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')