from flask import Blueprint

# Create API v1 blueprint
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# Import routes to register them
from app.api.v1 import auth, campaigns, ml, health

__all__ = ['api_v1']
