# OpenFunds v2.0 - Quick Test Guide

## 🎯 Application is Running!

**URLs:**
- Frontend: http://localhost:8501
- Backend: http://localhost:5000

---

## ✅ Test Data Created

We've automatically created test data for you:

### Users Created:
1. **Demo User**
   - Email: `demo@openfunds.io`
   - Password: `demo123456`

### Campaigns Created:
1. **Save the Ocean - Marine Conservation** (2.5 BTC target)
   - Current: 0.8 BTC raised (32%)
   
2. **Build a School in Rural Africa** (5.0 BTC target)
   - Current: 1.2 BTC raised (24%)
   
3. **Local Food Bank Support** (1.0 BTC target)
   - Current: 0.8 BTC raised (80%)
   
4. **Animal Shelter Emergency Fund** (1.5 BTC target)
   - Current: 0.4 BTC raised (27%)

**Total Platform Stats:**
- 4 campaigns
- 3.2 BTC raised
- 10.0 BTC target
- 32% overall progress

---

## 🧪 Testing Checklist

### ✅ Basic Features

#### 1. View Landing Page
- [ ] Open http://localhost:8501
- [ ] See OpenFunds logo and branding
- [ ] See "Why Choose OpenFunds?" features
- [ ] Gradient design looks good

#### 2. User Registration
- [ ] Click "Sign Up"
- [ ] Enter your details
- [ ] See success message
- [ ] Redirected to login

#### 3. User Login
- [ ] Use credentials:
  - Email: `demo@openfunds.io`
  - Password: `demo123456`
- [ ] Click "Log In"
- [ ] See welcome message with your name
- [ ] Redirected to dashboard

#### 4. Dashboard View
- [ ] See total campaigns count
- [ ] See total BTC raised
- [ ] See "Create New Campaign" button
- [ ] See "Browse Campaigns" button
- [ ] Sidebar shows user name

#### 5. View Campaigns
- [ ] Click "View Campaigns" in sidebar
- [ ] See all 4 campaigns listed
- [ ] See campaign cards with:
  - Title
  - Description
  - Owner name
  - Progress bar
  - Current/target amounts
  - BTC address
- [ ] Check progress bars are correct

#### 6. Filter Campaigns
- [ ] Try status filter: "All", "Active", "Funded"
- [ ] Try sort: "Newest", "Highest Funded", "Closest to Goal"
- [ ] Try search: Type "ocean" or "school"
- [ ] See filtered results update

#### 7. Make a Donation
- [ ] Find "Local Food Bank Support" (80% funded)
- [ ] Enter donation: `0.2` BTC
- [ ] Click "Donate"
- [ ] See success message
- [ ] Progress bar updates to 100%
- [ ] Status might change to "Funded"

#### 8. Create Your Own Campaign
- [ ] Click "Create Campaign" in sidebar
- [ ] Fill in form:
  - Title: "Your Campaign Title"
  - Description: (write at least 50 characters)
  - BTC Address: `2N8hwP1WmJrFF5QWABn38y63uYLhnJYJYTF`
  - Target: `0.5` BTC
- [ ] Click "Create Campaign"
- [ ] See success message
- [ ] Campaign appears in list

#### 9. Update Campaign Status
- [ ] In campaign card, change status dropdown
- [ ] Select different status
- [ ] Click "Update"
- [ ] See success message
- [ ] Status updates

#### 10. Statistics
- [ ] Go to Home
- [ ] See updated campaign count
- [ ] See updated total raised
- [ ] Numbers match your actions

#### 11. Logout
- [ ] Click "Logout" in sidebar
- [ ] Redirected to login page
- [ ] Try accessing dashboard (should redirect to login)

---

### ✅ Advanced Features

#### 12. Test API Directly
```powershell
# Health Check
Invoke-RestMethod http://localhost:5000/api/v1/health

# Get All Campaigns
$campaigns = Invoke-RestMethod http://localhost:5000/api/v1/campaigns
$campaigns.campaigns | Format-Table title, current_amount, target_amount, status

# Get Statistics
$stats = Invoke-RestMethod http://localhost:5000/api/v1/campaigns/stats
$stats.statistics
```

#### 13. Test Authentication
```powershell
# Login
$login = Invoke-RestMethod -Uri "http://localhost:5000/api/v1/auth/login" -Method POST -ContentType "application/json" -Body (@{
    email = "demo@openfunds.io"
    password = "demo123456"
} | ConvertTo-Json)

$token = $login.access_token
Write-Host "Token: $token"

# Get Current User
$headers = @{ "Authorization" = "Bearer $token" }
$user = Invoke-RestMethod -Uri "http://localhost:5000/api/v1/auth/me" -Headers $headers
$user.user
```

#### 14. Test Campaign Creation via API
```powershell
# (Use token from above)
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

$newCampaign = @{
    title = "API Test Campaign"
    description = "This campaign was created via API for testing"
    btc_address = "2N8hwP1WmJrFF5QWABn38y63uYLhnJYJYTF"
    target_amount = 0.75
} | ConvertTo-Json

$result = Invoke-RestMethod -Uri "http://localhost:5000/api/v1/campaigns" -Method POST -Headers $headers -Body $newCampaign
$result.campaign
```

#### 15. View Database
```powershell
cd backend
sqlite3 data/openfunds.db

# SQL commands:
.mode column
.headers on
.width 20 30 20 10

SELECT id, name, email FROM users;
SELECT id, title, current_amount, target_amount, status FROM campaigns;

.exit
```

---

### ✅ UI/UX Testing

#### 16. Design Elements
- [ ] Gradient background (purple/cyan)
- [ ] Campaign cards have hover effects
- [ ] Buttons have gradient and hover animations
- [ ] Progress bars are smooth
- [ ] Text is readable
- [ ] Logo displays correctly

#### 17. Responsive Design
- [ ] Resize browser window
- [ ] Check mobile view (narrow window)
- [ ] Sidebar collapses properly
- [ ] Cards stack vertically on small screens

#### 18. Loading States
- [ ] See spinner when creating campaign
- [ ] See spinner when making donation
- [ ] See "Loading campaigns..." message

#### 19. Error Handling
- [ ] Try creating campaign without login (should require login)
- [ ] Try invalid BTC address (should show error)
- [ ] Try negative donation amount (should show error)
- [ ] Try donating to closed campaign (should show message)

#### 20. Session Persistence
- [ ] Login
- [ ] Refresh page (should stay logged in)
- [ ] Close browser
- [ ] Open again (might need to login again)

---

### ✅ Performance Testing

#### 21. Load Testing
- [ ] Create 10 campaigns quickly
- [ ] Check if list loads fast
- [ ] Check if filters work with many campaigns
- [ ] Check search performance

#### 22. Concurrent Users
- [ ] Open in multiple browser tabs
- [ ] Login as different users
- [ ] Create campaigns simultaneously
- [ ] Check data consistency

---

### ✅ Security Testing

#### 23. Authentication
- [ ] Try accessing /api/v1/auth/me without token (should fail)
- [ ] Try creating campaign without login (should fail)
- [ ] Try wrong password (should fail)
- [ ] Check password is not visible in network tab

#### 24. Input Validation
- [ ] Try empty campaign title (should fail)
- [ ] Try invalid email format (should fail)
- [ ] Try short password (< 6 chars) (should fail)
- [ ] Try invalid BTC address (should fail)

---

## 📊 Expected Results

### Campaign List Should Show:
```
ID  Campaign                              Owner      Target  Current  Status
==  ==================================    =========  ======  =======  ======
1   Save the Ocean                        Demo User  2.5     0.8      Active
2   Build a School in Rural Africa        Demo User  5.0     1.2      Active
3   Local Food Bank Support               Demo User  1.0     1.0      Funded*
4   Animal Shelter Emergency Fund         Demo User  1.5     0.4      Active
5   Your Campaign                         Your Name  0.5     0.0      Active

*After you donate 0.2 BTC to reach the goal
```

### Statistics Should Show:
```
Total Campaigns:  5
Active Campaigns: 4
Funded Campaigns: 1
Total Raised:     3.4 BTC
Total Target:     10.5 BTC
Platform Progress: 32.4%
```

---

## 🐛 Common Issues & Solutions

### Issue: "Connection refused"
**Solution:** Backend is starting, wait 10 seconds

### Issue: "Cannot find module"
**Solution:** 
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Issue: Blank frontend page
**Solution:** Streamlit is loading, wait 15 seconds and refresh

### Issue: Campaigns not showing
**Solution:** Check backend terminal for errors, restart if needed

### Issue: Can't create campaign
**Solution:** Make sure you're logged in first

### Issue: Database locked
**Solution:**
```powershell
cd backend
Remove-Item data/openfunds.db
# Restart backend to create fresh database
```

---

## 📸 Screenshots to Take

Document your testing:
1. Landing page
2. Login screen
3. Dashboard with stats
4. Campaign list view
5. Campaign detail card
6. Create campaign form
7. Donation process
8. Progress bar at 100%
9. Statistics page
10. User profile (sidebar)

---

## ✅ Sign-off Checklist

After completing all tests:

- [ ] All basic features work
- [ ] Authentication works properly
- [ ] Campaigns can be created
- [ ] Donations update correctly
- [ ] Progress bars are accurate
- [ ] Statistics are correct
- [ ] UI looks beautiful
- [ ] No console errors
- [ ] API responses are fast
- [ ] Database persists data

---

## 🎉 Testing Complete!

If all tests pass, you have successfully:
✅ Set up OpenFunds v2.0 locally
✅ Tested all major features
✅ Verified API functionality
✅ Confirmed UI/UX quality
✅ Validated security measures

**Next Step:** Deploy to production!
See DEPLOYMENT.md for instructions.

---

## 📝 Notes

- Test data is stored in `backend/data/openfunds.db`
- All passwords are hashed with bcrypt
- JWT tokens expire after 24 hours
- Donations are tracked in real-time
- Progress bars update automatically

---

## 🆘 Need Help?

1. Check terminal output for errors
2. Review LOCAL_SETUP.md
3. Test API endpoints directly
4. Check database contents
5. Restart both services

---

**Happy Testing! 🚀**
