def create_app_with_blueprint():
    from flask import Flask
    app = Flask(__name__)

    # ======================
    # |    Configuration   |
    # ======================
    from .models import db
    from .config import Config
    app.config.from_object(Config)
    db.init_app(app)

    # ======================
    # |    Blueprint       |
    # ======================
    from .routes.auth import auth_bp
    from .routes.api import api_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    # ======================
    # |    Final stuff     |
    # ======================
    with app.app_context():
        db.create_all()
    return app