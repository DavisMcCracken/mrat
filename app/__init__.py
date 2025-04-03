from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    csrf.init_app(app)

    from app import models  # Import models so SQLAlchemy knows about them

    # ⬇ Register route blueprint here (from app/routes.py)
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app