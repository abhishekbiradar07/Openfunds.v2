# OpenFunds v2.0 - Complete Deployment Guide

This guide walks you through deploying OpenFunds on **100% free hosting platforms**.

## 📋 Prerequisites

- GitHub account
- Render.com account (free)
- Streamlit Community Cloud account (free)
- Git installed locally

---

## 🚀 Part 1: Deploy Backend to Render.com

### Step 1: Prepare Your Repository

```bash
cd OpenFunds-v2
git add .
git commit -m "Initial OpenFunds v2.0"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/openfunds-v2.git
git push -u origin main
```

### Step 2: Create Render Web Service

1. Go to [render.com](https://render.com) and sign up
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select the **openfunds-v2** repository
5. Configure the service:

**Settings:**
- **Name:** `openfunds-api`
- **Region:** Oregon (or closest to you)
- **Branch:** `main`
- **Root Directory:** `backend`
- **Runtime:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app.main:app --bind 0.0.0.0:$PORT --timeout 120`

**Environment Variables:**
Click "Advanced" → Add Environment Variables:

```
FLASK_ENV=production
SECRET_KEY=<generate-strong-random-key>
JWT_SECRET_KEY=<generate-another-strong-random-key>
DATABASE_URL=sqlite:///data/openfunds.db
FRONTEND_URL=https://openfunds.streamlit.app
```

To generate secure keys:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

6. Click **"Create Web Service"**
7. Wait 5-10 minutes for deployment
8. **Copy your backend URL:** `https://openfunds-api.onrender.com`

### Step 3: Test Your Backend

Visit: `https://openfunds-api.onrender.com/api/v1/health`

You should see:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-XX...",
  "service": "OpenFunds API",
  "version": "2.0"
}
```

✅ **Backend is live!**

---

## 🎨 Part 2: Deploy Frontend to Streamlit Cloud

### Step 1: Update Frontend Configuration

Create `.streamlit/secrets.toml` locally (don't commit this):

```toml
[api]
base_url = "https://openfunds-api.onrender.com/api/v1"
```

### Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"New app"**
4. Configure:
   - **Repository:** `YOUR_USERNAME/openfunds-v2`
   - **Branch:** `main`
   - **Main file path:** `frontend/app.py`
   
5. Click **"Advanced settings..."**
6. Add **Secrets** (paste your secrets.toml content):

```toml
[api]
base_url = "https://openfunds-api.onrender.com/api/v1"
```

7. Click **"Deploy!"**
8. Wait 2-5 minutes for deployment
9. **Your app URL:** `https://openfunds.streamlit.app` (or similar)

### Step 3: Update Backend CORS

Go back to Render dashboard:
1. Open your web service
2. Go to **Environment**
3. Update `FRONTEND_URL` to your Streamlit URL:

```
FRONTEND_URL=https://your-app-name.streamlit.app
```

4. Click **"Save Changes"** (this will redeploy)

### Step 4: Test Your Frontend

Visit your Streamlit URL and:
1. ✅ Sign up for an account
2. ✅ Log in
3. ✅ Create a campaign
4. ✅ View campaigns
5. ✅ Make a donation
6. ✅ Check AI predictions

✅ **Frontend is live and connected!**

---

## 🔧 Part 3: Optional Enhancements

### A) PostgreSQL Database (Recommended for Production)

**Why:** SQLite on Render's free tier may lose data on restart.

**How to add free PostgreSQL:**

1. In Render dashboard, click **"New +"** → **"PostgreSQL"**
2. Name: `openfunds-db`
3. Database: `openfunds`
4. User: `openfunds_user`
5. Plan: **Free**
6. Click **"Create Database"**
7. Copy the **Internal Database URL**
8. Update your web service's `DATABASE_URL` environment variable
9. Redeploy

### B) Keep Backend Awake (Prevent Cold Starts)

Render free tier sleeps after 15 minutes of inactivity. Use **UptimeRobot** (free) to ping your backend every 5 minutes:

1. Go to [uptimerobot.com](https://uptimerobot.com)
2. Sign up (free)
3. Add New Monitor:
   - **Monitor Type:** HTTP(s)
   - **URL:** `https://openfunds-api.onrender.com/api/v1/ping`
   - **Monitoring Interval:** 5 minutes
4. Save

Your backend will stay warm!

### C) Custom Domain (Optional)

**Render Custom Domain:**
1. Go to your web service → Settings
2. Scroll to **Custom Domain**
3. Add your domain (e.g., `api.openfunds.com`)
4. Update DNS records as instructed

**Streamlit Custom Domain:**
1. Requires **Streamlit Teams plan** (paid)
2. For free hosting, use the provided `.streamlit.app` subdomain

---

## 📊 Part 4: Monitoring & Logs

### Backend Logs (Render)
1. Open your web service on Render
2. Click **"Logs"** tab
3. View real-time logs

### Frontend Logs (Streamlit)
1. Open your app on Streamlit Cloud
2. Click **"Manage app"**
3. View logs and resource usage

### Health Check
Monitor your API health:
```
GET https://openfunds-api.onrender.com/api/v1/health
```

---

## 🐛 Troubleshooting

### Backend Issues

**Problem:** 503 Service Unavailable
- **Solution:** Backend is cold-starting (wait 30 seconds and retry)
- **Prevention:** Use UptimeRobot to keep it warm

**Problem:** Database connection errors
- **Solution:** Check `DATABASE_URL` environment variable
- **For SQLite:** Ensure path is correct (`sqlite:///data/openfunds.db`)
- **For PostgreSQL:** Check connection string format

**Problem:** CORS errors in browser
- **Solution:** Verify `FRONTEND_URL` matches your Streamlit URL exactly

### Frontend Issues

**Problem:** "Could not connect to server"
- **Solution:** Backend is sleeping or down
- **Check:** Visit health endpoint directly
- **Fix:** Wait for backend to wake up (30s)

**Problem:** Authentication not working
- **Solution:** Check API base URL in secrets
- **Verify:** Secrets are properly set in Streamlit Cloud dashboard

**Problem:** ML predictions not showing
- **Solution:** Models need training data (create 3+ campaigns first)
- **Check:** Backend logs for ML errors

---

## 🔄 Updating Your Deployment

### Update Backend
```bash
git add backend/
git commit -m "Update backend"
git push origin main
```
Render auto-deploys on git push!

### Update Frontend
```bash
git add frontend/
git commit -m "Update frontend"
git push origin main
```
Streamlit Cloud auto-deploys on git push!

---

## 💰 Cost Breakdown

| Service | Plan | Cost | Limits |
|---------|------|------|--------|
| **Render (Backend)** | Free | $0/month | 750 hours/month, 512MB RAM |
| **Streamlit Cloud** | Free | $0/month | Unlimited public apps |
| **PostgreSQL (Render)** | Free | $0/month | 1GB storage |
| **UptimeRobot** | Free | $0/month | 50 monitors |
| **GitHub** | Free | $0/month | Unlimited public repos |
| **Total** | | **$0/month** | ✅ |

---

## 🎉 Success Checklist

- [ ] Backend deployed to Render
- [ ] Backend health check works
- [ ] Frontend deployed to Streamlit Cloud
- [ ] Can register/login
- [ ] Can create campaigns
- [ ] Can view campaigns
- [ ] Can make donations
- [ ] AI predictions work
- [ ] Similarity detection works
- [ ] UptimeRobot monitoring setup (optional)
- [ ] PostgreSQL database setup (optional)

---

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Flask Documentation](https://flask.palletsprojects.com)
- [OpenFunds Backend API Docs](backend/README.md)
- [OpenFunds Frontend Docs](frontend/README.md)

---

## 🆘 Need Help?

1. Check logs (Render/Streamlit dashboards)
2. Review this guide
3. Open a GitHub issue
4. Check API endpoint directly with curl/Postman

---

**🚀 Happy Deploying!**
