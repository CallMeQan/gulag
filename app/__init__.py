# app.py
from flask import Flask #, session
from flask_session import Session
from .config import Config
from .extensions import db, bcrypt, login_manager, session
from .models import User
from .routes import home_bp, auth_bp, admin_bp, data_bp, dashboard_bp, mobile_bp

def create_app_with_blueprint():

    # ======================
    # |    Configuration   |
    # ======================
    app = Flask(__name__, static_folder="static")
    app.config.from_object(__name__)
    app.config.from_object(Config)
    Session(app)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    session.init_app(app)

    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ======================
    # |    Blueprint       |
    # ======================
    app.register_blueprint(home_bp, url_prefix = "/")
    app.register_blueprint(auth_bp, url_prefix = "/auth")
    app.register_blueprint(admin_bp, url_prefix = "/admin")
    app.register_blueprint(data_bp, url_prefix = "/data")
    app.register_blueprint(dashboard_bp, url_prefix = "/dashboard")
    app.register_blueprint(mobile_bp, url_prefix = "/mobile")

    # ======================
    # |    Final stuff     |
    # ======================
    with app.app_context():
        db.create_all()
    return app

if __name__ == "__main__":
    app = create_app_with_blueprint()
    app.run(debug=False, port=5000)
