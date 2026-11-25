import streamlit as st


def load_css():
    """Load custom CSS styles"""
    st.markdown("""
    <style>
        /* Main theme colors */
        :root {
            --primary: #7C4DFF;
            --secondary: #00E5FF;
            --background: #111122;
            --text: #FFFFFF;
            --accent: #FF4081;
            --success: #00E676;
            --warning: #FFAB40;
        }
        
        /* Global styling */
        .stApp {
            background: linear-gradient(135deg, #111122, #1A237E);
        }
        
        h1, h2, h3 {
            color: var(--text);
            font-weight: 600;
        }
        
        h1 {
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3em;
            margin-bottom: 0.5em;
        }
        
        .stButton > button {
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            color: white;
            border: none;
            border-radius: 20px;
            padding: 0.5em 2em;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(124, 77, 255, 0.4);
        }
        
        /* Sidebar styling */
        .css-1d391kg, .css-12oz5g7 {
            background: rgba(20, 20, 40, 0.7);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .stMetric {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .stMetric label {
            color: var(--secondary);
        }
        
        /* Card containers */
        .dashboard-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .dashboard-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }
        
        /* Progress bar */
        .stProgress > div > div {
            background-color: var(--primary);
            background-image: linear-gradient(90deg, var(--primary), var(--accent));
        }
        
        /* Auth forms styling */
        .auth-container {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }
        
        /* Footer */
        footer {
            background: rgba(20, 20, 40, 0.5);
            padding: 1rem;
            border-radius: 10px;
            margin-top: 2rem;
        }
        
        /* Loading spinner */
        .stSpinner > div {
            border-top-color: var(--primary) !important;
        }
    </style>
    """, unsafe_allow_html=True)
