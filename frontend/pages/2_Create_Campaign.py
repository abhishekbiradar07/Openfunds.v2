import streamlit as st
from components.styles import load_css
from services.campaign_api import CampaignAPI
from services.ml_api import MLAPI
from utils.session import check_authentication

st.set_page_config(page_title="OpenFunds - Create Campaign", page_icon="💰", layout="wide")
load_css()

if not check_authentication():
    st.switch_page("app.py")

campaign_api = CampaignAPI()
ml_api = MLAPI()

st.title("Create a New Fundraising Campaign")
st.write("Fill out the form below to create your campaign. AI will help predict success!")

# Campaign form
with st.form("create_campaign_form"):
    title = st.text_input("Campaign Title *", placeholder="Enter a compelling title")
    description = st.text_area("Campaign Description *", placeholder="Tell your story...", height=150)
    
    col1, col2 = st.columns(2)
    with col1:
        btc_address = st.text_input("Bitcoin Address (Testnet) *", placeholder="2N...")
    with col2:
        target_amount = st.number_input("Target Amount (BTC) *", min_value=0.001, value=1.0, step=0.1)
    
    col1, col2 = st.columns(2)
    with col1:
        check_similar = st.form_submit_button("🔍 Check for Similar Campaigns")
    with col2:
        create = st.form_submit_button("✅ Create Campaign")
    
    if check_similar:
        if title and description:
            with st.spinner("Searching for similar campaigns..."):
                result = ml_api.find_similar(title, description)
                if result.get('success') and result.get('count', 0) > 0:
                    st.warning(f"Found {result['count']} similar campaign(s):")
                    for sim in result['similar_campaigns']:
                        st.info(f"**{sim['title']}** - {sim['match_percentage']:.1f}% match")
                else:
                    st.success("No similar campaigns found!")
        else:
            st.error("Please enter title and description first")
    
    if create:
        if not all([title, description, btc_address, target_amount]):
            st.error("All fields are required")
        else:
            with st.spinner("Creating campaign..."):
                success, campaign, message = campaign_api.create(title, description, btc_address, target_amount)
                
                if success:
                    st.success(message)
                    
                    # Get AI prediction (optional feature)
                    with st.spinner("Getting AI prediction..."):
                        prediction = ml_api.predict_success(title, description, target_amount)
                        if prediction.get('success'):
                            st.success(f"🔮 Success Probability: {prediction['percentage']:.2f}%")
                            st.info(f"💬 {prediction['feedback']}")
                        else:
                            # ML libraries not installed - this is optional
                            pass
                    
                    # Train models (optional)
                    ml_api.train_models()
                    
                    st.success("✅ Campaign created successfully! Click 'View Campaigns' in the sidebar to see it.")
                else:
                    st.error(message)

# Tips section
with st.expander("💡 Tips for Success"):
    st.write("**1. Clear Title:** Make it descriptive and compelling")
    st.write("**2. Detailed Description:** Explain your why and how")
    st.write("**3. Realistic Goal:** Set achievable targets")
    st.write("**4. Share Widely:** Promote through your networks")
