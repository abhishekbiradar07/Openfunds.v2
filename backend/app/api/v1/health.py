from flask import jsonify
from app.api.v1 import api_v1
from datetime import datetime


@api_v1.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'OpenFunds API',
        'version': '2.0'
    }), 200


@api_v1.route('/ping', methods=['GET'])
def ping():
    """Simple ping endpoint"""
    return jsonify({'message': 'pong'}), 200
