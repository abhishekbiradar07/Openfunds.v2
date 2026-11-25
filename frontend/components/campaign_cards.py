import streamlit as st
from utils.formatters import format_btc, format_percentage


def display_campaign_card(campaign, campaign_api, ml_api):
    """Display a single campaign card"""
    st.markdown(f"### {campaign['title']}")
    
    # Status indicator
    status = campaign.get('status', 'Active')
    status_colors = {
        'Active': 'green',
        'Funded': 'blue',
        'Closed': 'gray'
    }
    color = status_colors.get(status, 'gray')
    st.markdown(f"**Status:** :{color}[{status}]")
    
    # Campaign details
    st.markdown(f"**Owner:** {campaign.get('owner_name', 'Unknown')}")
    st.markdown(f"**Description:** {campaign['description']}")
    
    # ML Prediction (optional feature)
    if ml_api:
        prediction = ml_api.predict_success(
            campaign['title'],
            campaign['description'],
            campaign['target_amount']
        )
        
        if prediction.get('success'):
            st.markdown(f"🔮 **Predicted Success:** {prediction.get('percentage', 0):.2f}%")
            st.markdown(f"💬 **AI Feedback:** {prediction.get('feedback', '')}")
        # If ML libraries not installed, just skip this section silently
    
    st.markdown(f"**Bitcoin Address:** `{campaign['btc_address']}`")
    
    # Progress bar
    progress = campaign.get('progress', 0)
    st.progress(min(progress / 100, 1.0))
    
    # Amount display
    current = campaign.get('current_amount', 0)
    target = campaign.get('target_amount', 0)
    st.markdown(f"**{format_btc(current)}** of **{format_btc(target)}** ({format_percentage(progress)})")
    
    # Donation and status controls
    col_a, col_b = st.columns(2)
    
    with col_a:
        if status == 'Active':
            donation_amount = st.number_input(
                "Donation Amount (BTC)",
                min_value=0.0001,
                max_value=float(target),
                value=0.01,
                step=0.01,
                key=f"donation_{campaign['id']}"
            )
            
            if st.button("Donate", key=f"donate_btn_{campaign['id']}"):
                with st.spinner("Processing donation..."):
                    success, message = campaign_api.donate(campaign['id'], donation_amount)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        else:
            st.info("This campaign is not accepting donations")
    
    with col_b:
        status_options = ["Active", "Funded", "Closed"]
        new_status = st.selectbox(
            "Update Status",
            options=status_options,
            index=status_options.index(status),
            key=f"status_{campaign['id']}"
        )
        
        if new_status != status:
            if st.button("Update", key=f"update_btn_{campaign['id']}"):
                with st.spinner("Updating status..."):
                    success, message = campaign_api.update_status(campaign['id'], new_status)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
    
    st.markdown("---")
