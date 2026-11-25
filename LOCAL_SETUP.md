# OpenFunds v2.0 - Local Setup Guide

## ✅ Project is Running Locally!

Your OpenFunds application is now running on your local machine.

---

## 🌐 Access URLs

### Backend (Flask API)
- **URL:** http://localhost:5000
- **Health Check:** http://localhost:5000/api/v1/health
- **Status:** ✅ RUNNING

### Frontend (Streamlit)
- **URL:** http://localhost:8501
- **Status:** ✅ RUNNING

---

## 📚 Available API Endpoints

### Authentication
```
POST   http://localhost:5000/api/v1/auth/register
POST   http://localhost:5000/api/v1/auth/login
GET    http://localhost:5000/api/v1/auth/me
GET    http://localhost:5000/api/v1/auth/verify
```

### Campaigns
```
GET    http://localhost:5000/api/v1/campaigns
POST   http://localhost:5000/api/v1/campaigns
GET    http://localhost:5000/api/v1/campaigns/{id}
PATCH  http://localhost:5000/api/v1/campaigns/{id}/status
POST   http://localhost:5000/api/v1/campaigns/{id}/donate
GET    http://localhost:5000/api/v1/campaigns/stats
```

### ML Services (Optional - requires dependencies)
```
POST   http://localhost:5000/api/v1/ml/predict
POST   http://localhost:5000/api/v1/ml/similar
POST   http://localhost:5000/api/v1/ml/train
```

### Monitoring
```
GET    http://localhost:5000/api/v1/health
GET    http://localhost:5000/api/v1/ping
```

---

## 🧪 Test the Application

### 1. Open Frontend
Open your browser and go to: **http://localhost:8501**

### 2. Register a New Account
- Click "Sign Up"
- Fill in:
  - Name: Your Name
  - Email: test@example.com
  - Password: password123
- Click "Sign Up"

### 3. Login
- Use the credentials you just created
- Click "Log In"

### 4. Create a Campaign
- Click "Create Campaign" in the sidebar
- Fill in:
  - Title: "My First Campaign"
  - Description: "This is a test campaign for the OpenFunds platform"
  - BTC Address: "2N8hwP1WmJrFF5QWABn38y63uYLhnJYJYTF" (testnet)
  - Target Amount: 1.0 BTC
- Click "Create Campaign"

### 5. View Campaigns
- Click "View Campaigns" in the sidebar
- You should see your campaign listed
- Try making a donation (0.1 BTC)
- Watch the progress bar update!

### 6. Check Statistics
- Go to Home
- See total campaigns and BTC raised

---

## 🔧 Testing API Directly

### Test with cURL:

**Health Check:**
```bash
curl http://localhost:5000/api/v1/health
```

**Register User:**
```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "password123"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

**Get Campaigns:**
```bash
curl http://localhost:5000/api/v1/campaigns
```

---

## 🛠️ Development Commands

### Backend Commands

**Stop Backend:**
```powershell
# Find the Python process
Get-Process python | Where-Object {$_.Path -like "*OpenFunds-v2*"}
# Stop it
Stop-Process -Name python -Force
```

**Restart Backend:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python run.py
```

**Run Tests:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python test_api.py
```

**Check Database:**
```powershell
cd backend
sqlite3 data/openfunds.db
# SQL commands:
# .tables
# SELECT * FROM users;
# SELECT * FROM campaigns;
# .exit
```

### Frontend Commands

**Stop Frontend:**
```powershell
# Find Streamlit process
Get-Process | Where-Object {$_.ProcessName -like "*streamlit*"}
# Or just close the terminal/command window
```

**Restart Frontend:**
```powershell
cd frontend
streamlit run app.py
```

**Clear Cache:**
```powershell
cd frontend
streamlit cache clear
```

---

## 📂 Project Files

### Backend Files
```
backend/
├── app/
│   ├── api/v1/           # API routes
│   ├── models/           # Database models
│   ├── services/         # Business logic
│   ├── ml/               # ML services
│   └── utils/            # Utilities
├── data/
│   └── openfunds.db      # SQLite database
└── run.py                # Start server
```

### Frontend Files
```
frontend/
├── pages/                # Streamlit pages
├── components/           # UI components
├── services/             # API clients
├── utils/                # Utilities
├── .streamlit/
│   └── secrets.toml      # API configuration
└── app.py                # Main entry
```

---

## 🐛 Troubleshooting

### Backend Not Starting
**Problem:** Port 5000 already in use
**Solution:**
```powershell
# Check what's using port 5000
netstat -ano | findstr :5000
# Kill the process
taskkill /PID <PID> /F
# Restart backend
```

### Frontend Not Connecting to Backend
**Problem:** Connection refused
**Solution:**
1. Check backend is running: http://localhost:5000/api/v1/health
2. Check `.streamlit/secrets.toml` has correct URL:
   ```toml
   [api]
   base_url = "http://localhost:5000/api/v1"
   ```
3. Restart frontend

### Database Errors
**Problem:** Database locked or corrupted
**Solution:**
```powershell
cd backend
# Delete database
Remove-Item data/openfunds.db
# Restart backend (creates new database)
python run.py
```

### Import Errors
**Problem:** Module not found
**Solution:**
```powershell
# Backend
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Frontend
cd frontend
pip install -r requirements.txt
```

---

## 🔒 Default Credentials

For testing, you can use:
- **Email:** test@example.com
- **Password:** password123

Or register a new account through the UI.

---

## 📊 Database Location

**SQLite Database:** `backend/data/openfunds.db`

**Tables:**
- `users` - User accounts
- `campaigns` - Fundraising campaigns

**View Data:**
```powershell
cd backend
sqlite3 data/openfunds.db
.mode column
.headers on
SELECT * FROM users;
SELECT * FROM campaigns;
```

---

## 🎨 UI/UX Features

✅ **Same beautiful design as v1**
- Purple/cyan gradient theme
- Smooth animations
- Responsive layout
- Progress bars
- Campaign cards
- Real-time updates

✅ **User Flow:**
1. Landing page with login/signup
2. Dashboard after login
3. Create campaign with validation
4. Browse campaigns with filters
5. Make donations
6. View statistics

---

## 🚀 Next Steps

### 1. Test All Features
- [ ] Register account
- [ ] Login
- [ ] Create campaign
- [ ] View campaigns
- [ ] Make donation
- [ ] Update campaign status
- [ ] Check statistics
- [ ] Logout

### 2. Customize
- [ ] Change colors in `frontend/components/styles.py`
- [ ] Modify campaign fields
- [ ] Add new features
- [ ] Update logo/branding

### 3. Deploy to Production
- [ ] Follow DEPLOYMENT.md guide
- [ ] Deploy backend to Render.com
- [ ] Deploy frontend to Streamlit Cloud
- [ ] Go live!

---

## 📝 Notes

- **Backend runs on:** http://localhost:5000
- **Frontend runs on:** http://localhost:8501
- **Database:** SQLite (backend/data/openfunds.db)
- **ML Features:** Optional (requires additional dependencies)
- **API Docs:** See backend/README.md

---

## 🆘 Need Help?

1. **Check logs:** Terminal output shows errors
2. **Review documentation:** README.md, DEPLOYMENT.md
3. **Test API:** Use curl or Postman
4. **Check database:** Use SQLite browser
5. **Restart services:** Stop and start both backend and frontend

---

## ✅ Quick Reference

| Service | URL | Status |
|---------|-----|--------|
| Backend API | http://localhost:5000 | ✅ Running |
| Frontend UI | http://localhost:8501 | ✅ Running |
| Health Check | http://localhost:5000/api/v1/health | ✅ Healthy |
| Database | backend/data/openfunds.db | ✅ Ready |

---

**🎉 Enjoy using OpenFunds v2.0 locally!**

**Ready to deploy? See DEPLOYMENT.md for production setup.**
