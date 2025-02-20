from flask import Flask
from .routes.auth import auth_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)

@app.route('/')
def index():
    return 'Hello, World!'

def run():
    app.run(debug=True)