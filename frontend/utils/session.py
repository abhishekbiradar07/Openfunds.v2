import streamlit as st


def init_session_state():
    """Initialize session state variables"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = 'login'
    
    if 'access_token' not in st.session_state:
        st.session_state.access_token = None
    
    if 'user_info' not in st.session_state:
        st.session_state.user_info = None


def check_authentication():
    """Check if user is authenticated"""
    return st.session_state.get('logged_in', False) and st.session_state.get('access_token') is not None
