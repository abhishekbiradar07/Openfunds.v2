from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

db = SQLAlchemy()


def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)

    with app.app_context():
        # Ensure the data directory exists for SQLite
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        if db_uri.startswith('sqlite:///'):
            db_file = db_uri.replace('sqlite:///', '')
            db_dir = os.path.dirname(db_file)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)

        # Import models to ensure they're registered
        from app.models import user, campaign

        # Create all tables
        db.create_all()

        print("Database initialized successfully!")


def get_db():
    """Get database instance"""
    return db
