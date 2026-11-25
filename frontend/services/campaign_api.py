from services.api_client import APIClient


class CampaignAPI:
    """Campaign API client"""
    
    def __init__(self):
        self.client = APIClient()
    
    def get_all(self, status=None, search=None, sort_by='newest'):
        """Get all campaigns"""
        endpoint = '/campaigns?'
        
        if status:
            endpoint += f'status={status}&'
        if search:
            endpoint += f'search={search}&'
        endpoint += f'sort_by={sort_by}'
        
        response = self.client.get(endpoint)
        
        if response and response.status_code == 200:
            return response.json().get('campaigns', [])
        return []
    
    def get_by_id(self, campaign_id):
        """Get campaign by ID"""
        response = self.client.get(f'/campaigns/{campaign_id}')
        
        if response and response.status_code == 200:
            return response.json().get('campaign')
        return None
    
    def create(self, title, description, btc_address, target_amount):
        """Create a new campaign"""
        data = {
            'title': title,
            'description': description,
            'btc_address': btc_address,
            'target_amount': target_amount
        }
        
        response = self.client.post('/campaigns', data=data, include_auth=True)
        
        if response and response.status_code == 201:
            return True, response.json().get('campaign'), response.json().get('message')
        elif response:
            error = response.json().get('error', 'Failed to create campaign')
            return False, None, error
        else:
            return False, None, 'Could not connect to server'
    
    def update_status(self, campaign_id, status):
        """Update campaign status"""
        data = {'status': status}
        
        response = self.client.patch(
            f'/campaigns/{campaign_id}/status', 
            data=data, 
            include_auth=True
        )
        
        if response and response.status_code == 200:
            return True, response.json().get('message')
        elif response:
            error = response.json().get('error', 'Failed to update status')
            return False, error
        else:
            return False, 'Could not connect to server'
    
    def donate(self, campaign_id, amount):
        """Add donation to campaign"""
        data = {'amount': amount}
        
        response = self.client.post(f'/campaigns/{campaign_id}/donate', data=data)
        
        if response and response.status_code == 200:
            return True, response.json().get('message')
        elif response:
            error = response.json().get('error', 'Failed to process donation')
            return False, error
        else:
            return False, 'Could not connect to server'
    
    def get_statistics(self):
        """Get platform statistics"""
        response = self.client.get('/campaigns/stats')
        
        if response and response.status_code == 200:
            return response.json().get('statistics', {})
        return {
            'total_campaigns': 0,
            'active_campaigns': 0,
            'funded_campaigns': 0,
            'total_raised': 0.0,
            'total_target': 0.0,
            'platform_progress': 0.0
        }
