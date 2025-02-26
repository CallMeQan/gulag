import os
from flask import Blueprint, jsonify, request, current_app

api_bp = Blueprint('api', __name__)

@api_bp.route('/ping')
def ping():
    return jsonify({'message': 'pong!'})

@api_bp.route('/upload', methods=['GET','POST'])
def upload():
    print(current_app.config['UPLOAD_FOLDER'])
    return jsonify({'message': 'uploading...'})