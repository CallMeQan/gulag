from flask import Blueprint, render_template, jsonify, request

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return jsonify(request.form)
    return render_template('register.html')

@auth_bp.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')