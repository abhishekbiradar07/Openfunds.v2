import requests
import streamlit as st
import time
from config import API_BASE_URL, API_TIMEOUT, API_RETRY_ATTEMPTS, API_RETRY_DELAY


class APIClient:
    """Base API client with retry logic and error handling"""
    
    def __init__(self, base_url=None):
        self.base_url = base_url or self._get_api_url()
        self.timeout = API_TIMEOUT
        self.session = requests.Session()
    
    @staticmethod
    def _get_api_url():
        """Get API URL from secrets or config"""
        try:
            if hasattr(st, 'secrets') and 'api' in st.secrets:
                return st.secrets['api']['base_url']
        except Exception:
            pass
        return API_BASE_URL
    
    def _get_headers(self, include_auth=False):
        """Get request headers"""
        headers = {
            'Content-Type': 'application/json'
        }
        
        if include_auth and 'access_token' in st.session_state:
            headers['Authorization'] = f"Bearer {st.session_state.access_token}"
        
        return headers
    
    def _make_request(self, method, endpoint, data=None, include_auth=False, retry=True):
        """Make HTTP request with retry logic"""
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers(include_auth)
        
        attempts = API_RETRY_ATTEMPTS if retry else 1
        
        for attempt in range(attempts):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    json=data,
                    headers=headers,
                    timeout=self.timeout
                )
                
                # Return response for all status codes
                return response
                
            except requests.exceptions.Timeout:
                if attempt < attempts - 1:
                    time.sleep(API_RETRY_DELAY)
                    continue
                return None
            except requests.exceptions.ConnectionError:
                if attempt < attempts - 1:
                    time.sleep(API_RETRY_DELAY)
                    continue
                return None
            except Exception as e:
                print(f"Request error: {e}")
                return None
        
        return None
    
    def get(self, endpoint, include_auth=False):
        """GET request"""
        return self._make_request('GET', endpoint, include_auth=include_auth)
    
    def post(self, endpoint, data=None, include_auth=False):
        """POST request"""
        return self._make_request('POST', endpoint, data=data, include_auth=include_auth)
    
    def patch(self, endpoint, data=None, include_auth=False):
        """PATCH request"""
        return self._make_request('PATCH', endpoint, data=data, include_auth=include_auth)
    
    def delete(self, endpoint, include_auth=False):
        """DELETE request"""
        return self._make_request('DELETE', endpoint, include_auth=include_auth)
