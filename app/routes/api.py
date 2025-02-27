import os
from flask import Blueprint, jsonify, request, current_app

api_bp = Blueprint('api', __name__)

@api_bp.route('/ping')
def ping():
    return jsonify({'message': 'pong!'})

@api_bp.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'message': 'Missing file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    if file.content_length > current_app.config['MAX_CONTENT_LENGTH']:
        return jsonify({'message': 'File too large'}), 400
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
    return jsonify({'message': 'Ok', 'filename': file.filename}), 200