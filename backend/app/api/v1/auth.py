from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
from app.api.v1 import api_v1
from app.api.deps import validate_json, token_required
from app.services.auth_service import AuthService


@api_v1.route('/auth/register', methods=['POST'])
@validate_json('name', 'email', 'password')
def register():
    """Register a new user"""
    data = request.get_json()
    
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    
    user, message = AuthService.register_user(name, email, password)
    
    if user:
        return jsonify({
            'message': message,
            'user': user.to_dict()
        }), 201
    else:
        return jsonify({'error': message}), 400


@api_v1.route('/auth/login', methods=['POST'])
@validate_json('email', 'password')
def login():
    """Login user and return JWT token"""
    data = request.get_json()
    
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    user, message = AuthService.login_user(email, password)
    
    if user:
        # Create JWT token (convert user_id to string for JWT)
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': message,
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
    else:
        return jsonify({'error': message}), 401


@api_v1.route('/auth/me', methods=['GET'])
@token_required
def get_current_user():
    """Get current user information"""
    user_id = int(get_jwt_identity())  # Convert back to int
    user = AuthService.get_user_by_id(user_id)
    
    if user:
        return jsonify({
            'user': user.to_dict()
        }), 200
    else:
        return jsonify({'error': 'User not found'}), 404


@api_v1.route('/auth/verify', methods=['GET'])
@token_required
def verify_token():
    """Verify if token is valid"""
    return jsonify({
        'valid': True,
        'message': 'Token is valid'
    }), 200
