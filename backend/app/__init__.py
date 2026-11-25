from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config import get_config
from app.database import init_db
import logging


def create_app():
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(get_config())
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize extensions
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['FRONTEND_URL'],
            "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    JWTManager(app)
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    from app.api.v1 import api_v1
    app.register_blueprint(api_v1)
    
    # Root endpoint
    @app.route('/')
    def index():
        return {
            'service': 'OpenFunds API',
            'version': '2.0',
            'status': 'running',
            'docs': '/api/v1/health'
        }
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500
    
    return app
