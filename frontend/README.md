# OpenFunds Frontend

Streamlit-based frontend for OpenFunds decentralized crowdfunding platform.

## Features

- 🔐 User Authentication (JWT)
- 💰 Campaign Browsing & Creation
- 🤖 AI Success Predictions
- 🔍 Duplicate Campaign Detection
- 📊 Real-time Statistics
- 💸 Bitcoin Donations

## Setup

### Local Development

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure API URL:**
```bash
cp .env.example .env
# Edit .env with your backend API URL
```

3. **Configure Streamlit secrets:**
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml with your API URL
```

4. **Run the app:**
```bash
streamlit run app.py
```

App will start at `http://localhost:8501`

## Project Structure

```
frontend/
├── app.py                 # Main entry point
├── pages/                 # Streamlit pages
│   ├── 1_Home.py
│   ├── 2_Create_Campaign.py
│   └── 3_View_Campaigns.py
├── components/            # Reusable UI components
│   ├── styles.py
│   ├── auth_forms.py
│   └── campaign_cards.py
├── services/              # API client services
│   ├── api_client.py
│   ├── auth_api.py
│   ├── campaign_api.py
│   └── ml_api.py
├── utils/                 # Utility functions
│   ├── formatters.py
│   └── session.py
└── config.py              # Configuration
```

## Deployment

### Streamlit Community Cloud (Free)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set main file path: `frontend/app.py`
5. Add secrets in Streamlit Cloud dashboard:
   ```toml
   [api]
   base_url = "https://your-backend.onrender.com/api/v1"
   ```
6. Deploy!

## Environment Variables

```
API_BASE_URL=http://localhost:5000/api/v1
```

Or use Streamlit secrets (`.streamlit/secrets.toml`):
```toml
[api]
base_url = "http://localhost:5000/api/v1"
```

## License

MIT License
