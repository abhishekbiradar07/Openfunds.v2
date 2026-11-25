import streamlit as st
from services.auth_api import AuthAPI


def show_auth_page():
    """Show authentication page (login/signup)"""
    auth_api = AuthAPI()
    
    # Logo and title
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, rgba(124, 77, 255, 0.2), rgba(0, 229, 255, 0.2)); border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);">
            <div style="font-size: 4em; margin-bottom: 10px;">💰</div>
            <h2 style="background: linear-gradient(90deg, #7C4DFF, #00E5FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.2em; font-weight: 700; margin-bottom: 10px;">OpenFunds</h2>
            <p style="color: #FFFFFF; font-size: 1.2em; opacity: 0.8;">Decentralized Fundraising Platform</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Auth form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        
        if st.session_state.auth_mode == 'login':
            st.markdown('<h2 style="text-align: center;">Log Into Your Account</h2>', unsafe_allow_html=True)
            st.markdown('<p style="text-align: center; color: rgba(255,255,255,0.7);">Welcome back to OpenFunds</p>', unsafe_allow_html=True)
            
            with st.form("login_form"):
                email = st.text_input("Email Address")
                password = st.text_input("Password", type="password")
                
                submit_button = st.form_submit_button("Log In", use_container_width=True)
                
                if submit_button:
                    if not email or not password:
                        st.error("Email and password are required")
                    else:
                        with st.spinner("Logging in..."):
                            success, message = auth_api.login(email, password)
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
            
            st.markdown('<div style="text-align: center; margin-top: 1rem;">', unsafe_allow_html=True)
            st.markdown('Need an account?')
            if st.button("Sign Up", key="toggle_signup"):
                st.session_state.auth_mode = 'signup'
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        else:  # Signup mode
            st.markdown('<h2 style="text-align: center;">Create an Account</h2>', unsafe_allow_html=True)
            st.markdown('<p style="text-align: center; color: rgba(255,255,255,0.7);">Join the OpenFunds community</p>', unsafe_allow_html=True)
            
            with st.form("signup_form"):
                name = st.text_input("Full Name")
                email = st.text_input("Email Address")
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                
                submit_button = st.form_submit_button("Sign Up", use_container_width=True)
                
                if submit_button:
                    if not name or not email or not password or not confirm_password:
                        st.error("All fields are required")
                    elif password != confirm_password:
                        st.error("Passwords do not match")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters long")
                    else:
                        with st.spinner("Creating account..."):
                            success, message = auth_api.register(name, email, password)
                            if success:
                                st.success(message)
                                st.session_state.auth_mode = 'login'
                                st.rerun()
                            else:
                                st.error(message)
            
            st.markdown('<div style="text-align: center; margin-top: 1rem;">', unsafe_allow_html=True)
            st.markdown('Already have an account?')
            if st.button("Log In", key="toggle_login"):
                st.session_state.auth_mode = 'login'
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Features section
    st.markdown("<h2 style='text-align: center; margin-top: 40px;'>Why Choose OpenFunds?</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(124, 77, 255, 0.1); padding: 20px; border-radius: 15px; text-align: center;">
            <div style="font-size: 2em; margin-bottom: 10px;">🔒</div>
            <h4>Decentralized</h4>
            <p style="color: rgba(255,255,255,0.7);">No middlemen, all donations go directly to creators</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(0, 229, 255, 0.1); padding: 20px; border-radius: 15px; text-align: center;">
            <div style="font-size: 2em; margin-bottom: 10px;">👁️</div>
            <h4>Transparent</h4>
            <p style="color: rgba(255,255,255,0.7);">All campaigns and funding are publicly visible</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: rgba(255, 64, 129, 0.1); padding: 20px; border-radius: 15px; text-align: center;">
            <div style="font-size: 2em; margin-bottom: 10px;">🧠</div>
            <h4>AI-Powered</h4>
            <p style="color: rgba(255,255,255,0.7);">Smart suggestions and success predictions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: rgba(0, 230, 118, 0.1); padding: 20px; border-radius: 15px; text-align: center;">
            <div style="font-size: 2em; margin-bottom: 10px;">💸</div>
            <h4>No Fees</h4>
            <p style="color: rgba(255,255,255,0.7);">Keep 100% of what you raise</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <footer style="margin-top: 60px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
                <p>© 2025 OpenFunds - A Decentralized Fundraising Platform</p>
            </div>
            <div style="display: flex; gap: 15px;">
                <span style="opacity: 0.7;">Follow us:</span>
                <a href="#" style="color: #00acee; text-decoration: none;">Twitter</a>
                <a href="#" style="color: #00acee; text-decoration: none;">Facebook</a>
                <a href="#" style="color: #00acee; text-decoration: none;">Instagram</a>
            </div>
        </div>
    </footer>
    """, unsafe_allow_html=True)
