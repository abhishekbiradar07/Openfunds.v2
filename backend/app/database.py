from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    
    with app.app_context():
        # Import models to ensure they're registered
        from app.models import user, campaign
        
        # Create all tables
        db.create_all()
        
        print("Database initialized successfully!")


def get_db():
    """Get database instance"""
    return db
