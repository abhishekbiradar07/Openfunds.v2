import streamlit as st
import pandas as pd
from components.styles import load_css
from components.campaign_cards import display_campaign_card
from services.campaign_api import CampaignAPI
from services.ml_api import MLAPI
from utils.session import check_authentication

st.set_page_config(page_title="OpenFunds - View Campaigns", page_icon="💰", layout="wide")
load_css()

if not check_authentication():
    st.switch_page("app.py")

campaign_api = CampaignAPI()
ml_api = MLAPI()

st.title("View Fundraising Campaigns")
st.write("Browse all active fundraising campaigns and support the ones you like.")

# Refresh button
if st.button("🔄 Refresh Campaigns"):
    st.rerun()

# Filters
st.subheader("Filter Campaigns")
col1, col2, col3 = st.columns(3)

with col1:
    status_filter = st.selectbox("Status", options=["All", "Active", "Funded", "Closed"], index=0)

with col2:
    sort_by = st.selectbox("Sort By", options=["Newest", "Highest Funded", "Closest to Goal"], index=0)

with col3:
    search_term = st.text_input("Search", placeholder="Title or owner...")

# Map sort options to API parameters
sort_mapping = {
    "Newest": "newest",
    "Highest Funded": "highest_funded",
    "Closest to Goal": "closest_to_goal"
}

# Fetch campaigns
with st.spinner("Loading campaigns..."):
    campaigns = campaign_api.get_all(
        status=None if status_filter == "All" else status_filter,
        search=search_term if search_term else None,
        sort_by=sort_mapping[sort_by]
    )

if not campaigns:
    st.info("No campaigns found. Create a new campaign to get started!")
    if st.button("Create New Campaign"):
        st.switch_page("pages/2_Create_Campaign.py")
else:
    # Display count
    st.write(f"Displaying {len(campaigns)} campaign(s)")
    
    # Display as table first
    df = pd.DataFrame(campaigns)
    df_display = df[['id', 'title', 'owner_name', 'target_amount', 'current_amount', 'status']].copy()
    df_display.columns = ['ID', 'Campaign', 'Owner', 'Target (BTC)', 'Current (BTC)', 'Status']
    st.dataframe(df_display, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Campaign Details")
    
    # Display campaign cards
    col1, col2 = st.columns(2)
    
    for i, campaign in enumerate(campaigns):
        with (col1 if i % 2 == 0 else col2):
            with st.container():
                display_campaign_card(campaign, campaign_api, ml_api)

# Footer
st.markdown("---")
st.write("© 2025 OpenFunds - A Decentralized Fundraising Platform")
