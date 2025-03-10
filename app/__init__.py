def create_app_with_blueprint():
    from flask import Flask
    import os
    app = Flask(__name__)

    # ======================
    # |    Configuration   |
    # ======================
    from .models import db
    from .config import Config
    app.secret_key = os.getenv('SECRET_KEY')
    app.config.from_object(Config)
    db.init_app(app)

    # ======================
    # |    Blueprint       |
    # ======================
    from .routes import auth_bp, home_bp, admin_bp, api_bp
    app.register_blueprint(home_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')

    # ======================
    # |    Final stuff     |
    # ======================
    with app.app_context():
        db.create_all()
    
    return app