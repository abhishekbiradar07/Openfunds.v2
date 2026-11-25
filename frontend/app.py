import streamlit as st
from components.styles import load_css
from components.auth_forms import show_auth_page
from utils.session import init_session_state, check_authentication
from services.auth_api import AuthAPI
from services.campaign_api import CampaignAPI

# Page configuration
st.set_page_config(
    page_title="OpenFunds - Decentralized Fundraising App",
    page_icon="💰",
    layout="wide",
)

# Initialize session state
init_session_state()

# Load custom CSS
load_css()

# Hide sidebar when not logged in
if not check_authentication():
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Main application
def show_main_app():
    """Display main app after login"""
    st.title("OpenFunds – Decentralized Fundraising App")
    
    # Logo section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, rgba(124, 77, 255, 0.2), rgba(0, 229, 255, 0.2)); border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);">
            <div style="font-size: 4em; margin-bottom: 10px;">💰</div>
            <h2 style="background: linear-gradient(90deg, #7C4DFF, #00E5FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.2em; font-weight: 700; margin-bottom: 10px;">OpenFunds</h2>
            <p style="color: #FFFFFF; font-size: 1.2em; opacity: 0.8;">Decentralized Fundraising Platform</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Welcome section
    st.write("## Welcome to OpenFunds!")
    st.write("OpenFunds is a modern decentralized fundraising platform that empowers creators and supporters to connect directly through blockchain technology.")
    
    st.write("### How It Works")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background: rgba(124, 77, 255, 0.1); padding: 20px; border-radius: 15px; text-align: center;">
            <div style="font-size: 2em; margin-bottom: 10px;">📝</div>
            <h4>Create</h4>
            <p>Set up your campaign with a compelling story and funding goal</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(0, 229, 255, 0.1); padding: 20px; border-radius: 15px; text-align: center;">
            <div style="font-size: 2em; margin-bottom: 10px;">📢</div>
            <h4>Share</h4>
            <p>Share your campaign with friends, family, and supporters</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: rgba(255, 64, 129, 0.1); padding: 20px; border-radius: 15px; text-align: center;">
            <div style="font-size: 2em; margin-bottom: 10px;">💸</div>
            <h4>Fund</h4>
            <p>Accept Bitcoin donations directly to your wallet</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Features
    st.write("### Features")
    st.write("- **Decentralized** - No middlemen, donations go directly to creators")
    st.write("- **Transparent** - All campaigns and funding are publicly visible")
    st.write("- **Secure** - Built on blockchain technology for maximum security")
    st.write("- **AI-Powered** - Smart predictions and duplicate detection")
    
    # Get statistics
    campaign_api = CampaignAPI()
    stats = campaign_api.get_statistics()
    
    # Dashboard stats
    st.write("## Dashboard Overview")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(124, 77, 255, 0.2), rgba(0, 229, 255, 0.2)); padding: 20px; border-radius: 15px; text-align: center;">
            <h3 style="margin-bottom: 10px;">Total Campaigns</h3>
            <div style="font-size: 3em; font-weight: bold;">{stats.get('total_campaigns', 0)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(0, 229, 255, 0.2), rgba(255, 64, 129, 0.2)); padding: 20px; border-radius: 15px; text-align: center;">
            <h3 style="margin-bottom: 10px;">Total Fundraising</h3>
            <div style="font-size: 3em; font-weight: bold;">{stats.get('total_raised', 0):.4f} BTC</div>
        </div>
        """, unsafe_allow_html=True)
    
    # CTA buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Create New Campaign", key="create_btn"):
            st.switch_page("pages/2_Create_Campaign.py")
    
    with col2:
        if st.button("Browse Campaigns", key="browse_btn"):
            st.switch_page("pages/3_View_Campaigns.py")
    
    # Footer
    st.markdown("""
    <footer>
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


# Main layout
if not check_authentication():
    show_auth_page()
else:
    # Sidebar when logged in
    auth_api = AuthAPI()
    
    st.sidebar.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <div style="font-size: 3em;">💰</div>
        <h3>OpenFunds</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Display user info
    if 'user_info' in st.session_state and st.session_state.user_info:
        st.sidebar.markdown(f"### Welcome, {st.session_state.user_info.get('name')}!")
    
    # Navigation
    st.sidebar.markdown("### Navigation")
    
    if st.sidebar.button("🏠 Home", key="home_nav", use_container_width=True):
        st.switch_page("pages/1_Home.py")
    
    if st.sidebar.button("➕ Create Campaign", key="create_nav", use_container_width=True):
        st.switch_page("pages/2_Create_Campaign.py")
    
    if st.sidebar.button("👁️ View Campaigns", key="view_nav", use_container_width=True):
        st.switch_page("pages/3_View_Campaigns.py")
    
    # Logout button
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout", key="logout_btn", use_container_width=True):
        auth_api.logout()
        st.rerun()
    
    # Sidebar stats
    campaign_api = CampaignAPI()
    stats = campaign_api.get_statistics()
    
    st.sidebar.markdown("### Dashboard Stats")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Campaigns", f"{stats.get('total_campaigns', 0)}")
    with col2:
        st.metric("Total BTC", f"{stats.get('total_raised', 0):.4f}")
    
    # Show main app
    show_main_app()
