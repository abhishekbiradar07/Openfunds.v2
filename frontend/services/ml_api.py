from services.api_client import APIClient


class MLAPI:
    """ML Services API client"""
    
    def __init__(self):
        self.client = APIClient()
    
    def predict_success(self, title, description, target_amount):
        """Predict campaign success probability"""
        data = {
            'title': title,
            'description': description,
            'target_amount': target_amount
        }
        
        response = self.client.post('/ml/predict', data=data)
        
        if response and response.status_code == 200:
            result = response.json()
            if result.get('success'):
                return {
                    'success': True,
                    'probability': result.get('probability', 0),
                    'percentage': result.get('percentage', 0),
                    'feedback': result.get('feedback', '')
                }
            else:
                return {
                    'success': False,
                    'error': result.get('error', 'Prediction unavailable')
                }
        else:
            return {
                'success': False,
                'error': 'Could not connect to ML service'
            }
    
    def find_similar(self, title, description, top_k=3):
        """Find similar campaigns"""
        data = {
            'title': title,
            'description': description,
            'top_k': top_k,
            'threshold': 0.3
        }
        
        response = self.client.post('/ml/similar', data=data)
        
        if response and response.status_code == 200:
            result = response.json()
            if result.get('success'):
                return {
                    'success': True,
                    'similar_campaigns': result.get('similar_campaigns', []),
                    'count': result.get('count', 0)
                }
            else:
                return {
                    'success': False,
                    'error': result.get('error', 'Similarity search unavailable')
                }
        else:
            return {
                'success': False,
                'error': 'Could not connect to ML service'
            }
    
    def train_models(self):
        """Trigger ML model training"""
        response = self.client.post('/ml/train')
        
        if response and response.status_code == 200:
            return True, response.json().get('message', 'Models trained successfully')
        elif response:
            error = response.json().get('error', 'Training failed')
            return False, error
        else:
            return False, 'Could not connect to server'
