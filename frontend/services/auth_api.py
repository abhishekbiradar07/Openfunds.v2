import streamlit as st
from services.api_client import APIClient


class AuthAPI:
    """Authentication API client"""
    
    def __init__(self):
        self.client = APIClient()
    
    def register(self, name, email, password):
        """Register a new user"""
        data = {
            'name': name,
            'email': email,
            'password': password
        }
        
        response = self.client.post('/auth/register', data=data)
        
        if response and response.status_code == 201:
            return True, response.json().get('message', 'Registration successful')
        elif response:
            error = response.json().get('error', 'Registration failed')
            return False, error
        else:
            return False, 'Could not connect to server. Please try again.'
    
    def login(self, email, password):
        """Login user and store token"""
        data = {
            'email': email,
            'password': password
        }
        
        response = self.client.post('/auth/login', data=data)
        
        if response and response.status_code == 200:
            data = response.json()
            st.session_state.access_token = data.get('access_token')
            st.session_state.user_info = data.get('user')
            st.session_state.logged_in = True
            return True, data.get('message', 'Login successful')
        elif response:
            error = response.json().get('error', 'Login failed')
            return False, error
        else:
            return False, 'Could not connect to server. Please try again.'
    
    def get_current_user(self):
        """Get current user info"""
        response = self.client.get('/auth/me', include_auth=True)
        
        if response and response.status_code == 200:
            return response.json().get('user')
        return None
    
    def verify_token(self):
        """Verify if current token is valid"""
        response = self.client.get('/auth/verify', include_auth=True)
        
        if response and response.status_code == 200:
            return True
        return False
    
    def logout(self):
        """Logout user"""
        if 'access_token' in st.session_state:
            del st.session_state.access_token
        if 'user_info' in st.session_state:
            del st.session_state.user_info
        st.session_state.logged_in = False
