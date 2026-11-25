import streamlit as st
from components.styles import load_css
from services.campaign_api import CampaignAPI
from utils.session import check_authentication

st.set_page_config(page_title="OpenFunds - Home", page_icon="💰", layout="wide")
load_css()

if not check_authentication():
    st.switch_page("app.py")

campaign_api = CampaignAPI()

st.title("OpenFunds – Home Dashboard")

# Same UI as app.py main page
# (Full implementation in final version - keeping concise for now)

st.write("Welcome to your OpenFunds dashboard!")
stats = campaign_api.get_statistics()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Campaigns", stats.get('total_campaigns', 0))
with col2:
    st.metric("Active Campaigns", stats.get('active_campaigns', 0))
with col3:
    st.metric("Funded Campaigns", stats.get('funded_campaigns', 0))

col1, col2 = st.columns(2)
with col1:
    if st.button("➕ Create Campaign", use_container_width=True):
        st.switch_page("pages/2_Create_Campaign.py")
with col2:
    if st.button("👁️ Browse Campaigns", use_container_width=True):
        st.switch_page("pages/3_View_Campaigns.py")
