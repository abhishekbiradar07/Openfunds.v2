from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.api.v1 import api_v1
from app.api.deps import token_required, validate_json
from app.services.campaign_service import CampaignService


@api_v1.route('/campaigns', methods=['GET'])
def get_campaigns():
    """Get all campaigns with optional filters"""
    status = request.args.get('status', None)
    search = request.args.get('search', None)
    sort_by = request.args.get('sort_by', 'newest')
    
    campaigns = CampaignService.get_all_campaigns(status, search, sort_by)
    
    return jsonify({
        'campaigns': campaigns,
        'count': len(campaigns)
    }), 200


@api_v1.route('/campaigns/<int:campaign_id>', methods=['GET'])
def get_campaign(campaign_id):
    """Get a single campaign by ID"""
    campaign = CampaignService.get_campaign_by_id(campaign_id)
    
    if campaign:
        return jsonify({'campaign': campaign}), 200
    else:
        return jsonify({'error': 'Campaign not found'}), 404


@api_v1.route('/campaigns', methods=['POST'])
@token_required
@validate_json('title', 'description', 'btc_address', 'target_amount')
def create_campaign():
    """Create a new campaign"""
    user_id = int(get_jwt_identity())  # Convert back to int
    data = request.get_json()
    
    title = data.get('title')
    description = data.get('description')
    btc_address = data.get('btc_address')
    target_amount = data.get('target_amount')
    
    campaign, message = CampaignService.create_campaign(
        title, description, btc_address, target_amount, user_id
    )
    
    if campaign:
        return jsonify({
            'message': message,
            'campaign': campaign.to_dict()
        }), 201
    else:
        return jsonify({'error': message}), 400


@api_v1.route('/campaigns/<int:campaign_id>/status', methods=['PATCH'])
@token_required
@validate_json('status')
def update_campaign_status(campaign_id):
    """Update campaign status"""
    user_id = int(get_jwt_identity())  # Convert back to int
    data = request.get_json()
    status = data.get('status')
    
    campaign, message = CampaignService.update_campaign_status(campaign_id, status, user_id)
    
    if campaign:
        return jsonify({
            'message': message,
            'campaign': campaign.to_dict()
        }), 200
    else:
        return jsonify({'error': message}), 400


@api_v1.route('/campaigns/<int:campaign_id>/donate', methods=['POST'])
@validate_json('amount')
def donate_to_campaign(campaign_id):
    """Add a donation to a campaign"""
    data = request.get_json()
    amount = data.get('amount')
    
    campaign, message = CampaignService.add_donation(campaign_id, amount)
    
    if campaign:
        return jsonify({
            'message': message,
            'campaign': campaign.to_dict()
        }), 200
    else:
        return jsonify({'error': message}), 400


@api_v1.route('/campaigns/stats', methods=['GET'])
def get_statistics():
    """Get platform statistics"""
    stats = CampaignService.get_statistics()
    
    return jsonify({
        'statistics': stats
    }), 200
