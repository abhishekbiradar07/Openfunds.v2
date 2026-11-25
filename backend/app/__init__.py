from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config import get_config
from app.database import init_db
import re
import logging


def _build_cors_origins(frontend_url: str) -> list:
    """Build the list of allowed CORS origins.

    Always includes localhost for local development.  If the configured
    FRONTEND_URL contains a wildcard (e.g. ``https://*.streamlit.app``) the
    matching is done via a compiled regex so Flask-CORS can evaluate it at
    request time.
    """
    origins = [
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ]
    if frontend_url and frontend_url not in origins:
        if "*" in frontend_url:
            # Convert glob-style wildcard to a regex pattern
            pattern = re.escape(frontend_url).replace(r"\*", r"[^.]+")
            origins.append(re.compile(pattern))
        else:
            origins.append(frontend_url)
    return origins


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
    allowed_origins = _build_cors_origins(app.config.get("FRONTEND_URL", ""))
    CORS(app, resources={
        r"/api/*": {
            "origins": allowed_origins,
            "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": False,
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
