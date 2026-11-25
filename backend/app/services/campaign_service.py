from app.database import db
from app.models.campaign import Campaign
from app.utils.validators import validate_btc_address
import os

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("⚠️ pandas not available - CSV export disabled")


class CampaignService:
    """Service for campaign operations"""
    
    @staticmethod
    def create_campaign(title, description, btc_address, target_amount, owner_id):
        """Create a new campaign"""
        # Validate inputs
        if not title or len(title.strip()) < 4:
            return None, "Title must be at least 4 characters"
        
        if not description or len(description.strip()) < 10:
            return None, "Description must be at least 10 characters"
        
        if not validate_btc_address(btc_address):
            return None, "Invalid Bitcoin address format"
        
        if target_amount <= 0:
            return None, "Target amount must be greater than 0"
        
        try:
            campaign = Campaign(
                title=title.strip(),
                description=description.strip(),
                btc_address=btc_address.strip(),
                target_amount=float(target_amount),
                owner_id=owner_id
            )
            db.session.add(campaign)
            db.session.commit()
            
            # Export to CSV for ML training
            CampaignService.export_to_csv()
            
            return campaign, "Campaign created successfully"
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to create campaign: {str(e)}"
    
    @staticmethod
    def get_all_campaigns(status=None, search=None, sort_by='newest'):
        """Get all campaigns with optional filters"""
        query = Campaign.query
        
        # Filter by status
        if status and status != 'All':
            query = query.filter_by(status=status)
        
        # Search filter
        if search:
            search_term = f"%{search}%"
            query = query.join(Campaign.owner).filter(
                db.or_(
                    Campaign.title.ilike(search_term),
                    Campaign.description.ilike(search_term),
                    db.text(f"users.name ILIKE '{search_term}'")
                )
            )
        
        # Sorting
        if sort_by == 'newest':
            query = query.order_by(Campaign.created_at.desc())
        elif sort_by == 'highest_funded':
            query = query.order_by(Campaign.current_amount.desc())
        elif sort_by == 'closest_to_goal':
            # Sort by progress percentage (current/target)
            query = query.order_by((Campaign.current_amount / Campaign.target_amount).desc())
        
        campaigns = query.all()
        return [campaign.to_dict() for campaign in campaigns]
    
    @staticmethod
    def get_campaign_by_id(campaign_id):
        """Get a single campaign by ID"""
        campaign = Campaign.query.get(campaign_id)
        return campaign.to_dict() if campaign else None
    
    @staticmethod
    def update_campaign_status(campaign_id, status, user_id):
        """Update campaign status"""
        campaign = Campaign.query.get(campaign_id)
        
        if not campaign:
            return None, "Campaign not found"
        
        # Check ownership (optional - can be enforced based on requirements)
        # if campaign.owner_id != user_id:
        #     return None, "You don't have permission to update this campaign"
        
        if status not in ['Active', 'Funded', 'Closed']:
            return None, "Invalid status"
        
        try:
            campaign.status = status
            db.session.commit()
            
            CampaignService.export_to_csv()
            
            return campaign, "Status updated successfully"
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to update status: {str(e)}"
    
    @staticmethod
    def add_donation(campaign_id, amount):
        """Add donation to campaign"""
        campaign = Campaign.query.get(campaign_id)
        
        if not campaign:
            return None, "Campaign not found"
        
        if campaign.status != 'Active':
            return None, "Campaign is not accepting donations"
        
        if amount <= 0:
            return None, "Donation amount must be greater than 0"
        
        try:
            campaign.current_amount += float(amount)
            
            # Auto-update status if goal reached
            if campaign.current_amount >= campaign.target_amount:
                campaign.status = 'Funded'
            
            db.session.commit()
            
            CampaignService.export_to_csv()
            
            return campaign, "Donation added successfully"
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to add donation: {str(e)}"
    
    @staticmethod
    def get_statistics():
        """Get platform statistics"""
        total_campaigns = Campaign.query.count()
        active_campaigns = Campaign.query.filter_by(status='Active').count()
        funded_campaigns = Campaign.query.filter_by(status='Funded').count()
        
        total_raised = db.session.query(
            db.func.sum(Campaign.current_amount)
        ).scalar() or 0.0
        
        total_target = db.session.query(
            db.func.sum(Campaign.target_amount)
        ).scalar() or 0.0
        
        return {
            'total_campaigns': total_campaigns,
            'active_campaigns': active_campaigns,
            'funded_campaigns': funded_campaigns,
            'total_raised': round(total_raised, 8),
            'total_target': round(total_target, 8),
            'platform_progress': round((total_raised / total_target * 100) if total_target > 0 else 0, 2)
        }
    
    @staticmethod
    def export_to_csv():
        """Export all campaigns to CSV for ML training"""
        if not PANDAS_AVAILABLE:
            return False
            
        try:
            campaigns = Campaign.query.all()
            
            if not campaigns:
                return False
            
            data = []
            for campaign in campaigns:
                data.append({
                    'id': campaign.id,
                    'title': campaign.title,
                    'description': campaign.description,
                    'btc_address': campaign.btc_address,
                    'target_amount': campaign.target_amount,
                    'current_amount': campaign.current_amount,
                    'status': campaign.status,
                    'owner_id': campaign.owner_id,
                    'created_at': campaign.created_at
                })
            
            df = pd.DataFrame(data)
            
            # Create directory if not exists
            os.makedirs('data_exports', exist_ok=True)
            
            # Save to CSV
            df.to_csv('data_exports/campaigns.csv', index=False)
            
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
    
    @staticmethod
    def get_campaigns_for_ml():
        """Get campaign data for ML operations"""
        campaigns = Campaign.query.all()
        return [campaign.to_dict() for campaign in campaigns]
