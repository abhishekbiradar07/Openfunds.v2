from flask import request, jsonify
from app.api.v1 import api_v1
from app.api.deps import validate_json
from app.ml.predictor import MLPredictor
from app.ml.similarity import SimilarityEngine
from app.services.campaign_service import CampaignService


@api_v1.route('/ml/predict', methods=['POST'])
@validate_json('title', 'description', 'target_amount')
def predict_success():
    """Predict campaign success probability"""
    data = request.get_json()
    
    title = data.get('title')
    description = data.get('description')
    target_amount = data.get('target_amount')
    
    result = MLPredictor.predict_success(title, description, target_amount)
    
    if result.get('success'):
        return jsonify(result), 200
    else:
        return jsonify(result), 200  # Still return 200 but with error message


@api_v1.route('/ml/similar', methods=['POST'])
@validate_json('title', 'description')
def find_similar():
    """Find similar campaigns"""
    data = request.get_json()
    
    title = data.get('title')
    description = data.get('description')
    top_k = data.get('top_k', 3)
    threshold = data.get('threshold', 0.3)
    
    # Get all campaigns for similarity comparison
    campaigns_data = CampaignService.get_campaigns_for_ml()
    
    result = SimilarityEngine.find_similar(
        title, description, campaigns_data, top_k, threshold
    )
    
    if result.get('success'):
        return jsonify(result), 200
    else:
        return jsonify(result), 200


@api_v1.route('/ml/train', methods=['POST'])
def train_models():
    """Train ML models on current campaign data"""
    # Get all campaigns
    campaigns_data = CampaignService.get_campaigns_for_ml()
    
    if len(campaigns_data) < 3:
        return jsonify({
            'success': False,
            'error': 'Need at least 3 campaigns to train models'
        }), 400
    
    success, message = MLPredictor.train_models(campaigns_data)
    
    if success:
        return jsonify({
            'success': True,
            'message': message
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': message
        }), 400
