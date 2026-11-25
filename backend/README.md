# OpenFunds Backend API

Flask-based REST API for the OpenFunds decentralized crowdfunding platform.

## Features

- 🔐 JWT Authentication
- 💰 Campaign Management (CRUD)
- 🤖 ML-Powered Success Prediction
- 🔍 Semantic Similarity Detection
- 📊 Platform Statistics
- 🗄️ SQLite/PostgreSQL Support

## Tech Stack

- **Framework:** Flask 3.0
- **Database:** SQLAlchemy (SQLite/PostgreSQL)
- **Auth:** Flask-JWT-Extended
- **ML:** scikit-learn, sentence-transformers
- **Deployment:** Gunicorn

## Setup

### Local Development

1. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your settings
```

4. **Run the server:**
```bash
python run.py
```

Server will start at `http://localhost:5000`

### API Documentation

**Health Check:**
```
GET /api/v1/health
```

**Authentication:**
```
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/auth/me
```

**Campaigns:**
```
GET    /api/v1/campaigns
POST   /api/v1/campaigns
GET    /api/v1/campaigns/{id}
PATCH  /api/v1/campaigns/{id}/status
POST   /api/v1/campaigns/{id}/donate
GET    /api/v1/campaigns/stats
```

**ML Services:**
```
POST /api/v1/ml/predict
POST /api/v1/ml/similar
POST /api/v1/ml/train
```

## Deployment

### Render.com (Free Tier)

1. Push code to GitHub
2. Connect Render to your repository
3. Use `render.yaml` for automatic configuration
4. Set environment variables in Render dashboard

### Railway/Heroku

```bash
# Uses Procfile for deployment
git push railway main
# or
git push heroku main
```

## Environment Variables

```
FLASK_ENV=production
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=postgresql://...
FRONTEND_URL=https://your-frontend.streamlit.app
```

## Project Structure

```
backend/
├── app/
│   ├── api/v1/          # API routes
│   ├── models/          # SQLAlchemy models
│   ├── services/        # Business logic
│   ├── ml/              # ML services
│   ├── utils/           # Utilities
│   ├── config.py        # Configuration
│   ├── database.py      # Database setup
│   └── main.py          # App factory
├── data/                # SQLite database
├── tests/               # Tests
├── requirements.txt     # Dependencies
└── run.py              # Dev server
```

## License

MIT License - see LICENSE file
