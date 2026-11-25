# OpenFunds v2.0 - Test Campaigns Guide

## 🎉 Test Data Successfully Created!

Your OpenFunds platform now has **17 diverse campaigns** to test with!

---

## 📊 Current Statistics

- **Total Campaigns:** 17
- **Active Campaigns:** 10
- **Funded Campaigns:** 7
- **Total Raised:** ~12+ BTC
- **Total Target:** ~30+ BTC

---

## 📋 Available Test Campaigns

### 🌊 Environmental & Conservation (3 campaigns)

**1. Save the Coral Reefs - Marine Conservation**
- Target: 3.5 BTC
- Current: 0.4 BTC (11.4%)
- Status: Active
- Use for: Testing low-progress campaigns

**2. Reforestation Project - Plant 10,000 Trees**
- Target: 1.5 BTC
- Current: 0 BTC (0%)
- Status: Active
- Use for: Testing zero-donation campaigns

**3. Save the Ocean - Marine Conservation**
- Target: 2.5 BTC
- Current: 2.3 BTC (92%)
- Status: Active
- Use for: Testing near-completion campaigns

### 📚 Education & Youth (3 campaigns)

**4. Build a Library in Rural India**
- Target: 4.2 BTC
- Current: 1.2 BTC (28.6%)
- Status: Active
- Use for: Testing mid-progress campaigns

**5. Youth Coding Bootcamp for Underprivileged Teens**
- Target: 2.5 BTC
- Current: 0 BTC (0%)
- Status: Active
- Use for: Testing new campaigns

**6. Renewable Energy for Remote Schools**
- Target: 6.0 BTC (Largest campaign)
- Current: 0 BTC (0%)
- Status: Active
- Use for: Testing high-target campaigns

### 🏥 Emergency & Relief (2 campaigns)

**7. Emergency Medical Supplies for War-Torn Regions**
- Target: 2.0 BTC
- Current: 0.7 BTC (35%)
- Status: Active
- Use for: Testing urgent campaigns

**8. Homeless Shelter Winter Emergency Fund**
- Target: 1.2 BTC
- Current: 0 BTC (0%)
- Status: Active
- Use for: Testing community support

### 🐾 Animals & Welfare (1 campaign)

**9. Street Dog Rescue and Rehabilitation Center**
- Target: 1.8 BTC
- Current: 0 BTC (0%)
- Status: Active
- Use for: Testing animal welfare projects

### 💧 Social Impact (3 campaigns)

**10. Clean Water Wells for African Villages**
- Target: 5.0 BTC
- Current: 0 BTC (0%)
- Status: Active
- Use for: Testing infrastructure projects

**11. Build a School in Rural Africa**
- Target: 5.0 BTC
- Current: 1.92 BTC (38.4%)
- Status: Active
- Use for: Testing education infrastructure

**12. Local Food Bank Support**
- Target: 1.0 BTC
- Current: 2.0 BTC (200%)
- Status: **Funded**
- Use for: Testing over-funded campaigns

### 🎨 Community & Culture (2 campaigns)

**13. Support Local Artists - Community Art Center**
- Target: 2.2 BTC
- Current: 0 BTC (0%)
- Status: Active
- Use for: Testing arts & culture

**14. Community Garden Project**
- Target: 1.0 BTC
- Current: 1.0 BTC (100%)
- Status: **Funded**
- Use for: Testing completed campaigns

### 🏠 Already Funded (5 campaigns)

**15-19. Various Funded Campaigns**
- Status: Funded
- Use for: Testing funded campaign interactions

---

## 🧪 Testing Scenarios

### Scenario 1: Filter by Status
1. Go to "View Campaigns"
2. Filter: "Active" - Should show 10 campaigns
3. Filter: "Funded" - Should show 7 campaigns
4. Filter: "All" - Should show all 17 campaigns

### Scenario 2: Sort Campaigns
1. Sort by "Newest" - Recent campaigns first
2. Sort by "Highest Funded" - Local Food Bank (200%) first
3. Sort by "Closest to Goal" - Save the Ocean (92%) first

### Scenario 3: Search Functionality
- Search "school" - Should find 2 campaigns
- Search "ocean" - Should find 2 campaigns
- Search "community" - Should find multiple campaigns
- Search "water" - Should find 1 campaign

### Scenario 4: Make Donations
**Small Donation:**
- Campaign: Reforestation Project
- Donate: 0.1 BTC
- Result: Progress 0% → 6.7%

**Medium Donation:**
- Campaign: Street Dog Rescue
- Donate: 0.5 BTC
- Result: Progress 0% → 27.8%

**Complete Campaign:**
- Campaign: Save the Ocean (92%)
- Donate: 0.2 BTC
- Result: Status changes to "Funded"

**Over-donate:**
- Campaign: Youth Coding Bootcamp
- Donate: 3.0 BTC
- Result: Progress > 100%

### Scenario 5: Progress Bar Testing
- 0% Progress: Youth Coding Bootcamp
- Low (11%): Coral Reefs
- Mid (35%): Emergency Medical
- High (92%): Save the Ocean
- Complete (100%): Community Garden
- Over (200%): Local Food Bank

### Scenario 6: Update Campaign Status
1. Select any Active campaign
2. Change status to "Closed"
3. Verify it no longer accepts donations
4. Change back to "Active"

### Scenario 7: Statistics Dashboard
1. Go to Home
2. Check if numbers match:
   - Total: 17
   - Active: 10
   - Funded: 7
3. Make a donation
4. Check if statistics update

---

## 💡 Test Ideas

### Edge Cases to Test:

**1. Zero Balance Campaign**
- Campaign: Youth Coding Bootcamp
- Test: Can you donate 0.0001 BTC?

**2. Already Funded Campaign**
- Campaign: Local Food Bank
- Test: Can you still donate? (Should work)

**3. Large Amount Donation**
- Campaign: Renewable Energy (6.0 BTC target)
- Test: Donate 10.0 BTC at once

**4. Multiple Small Donations**
- Campaign: Any active
- Test: Donate 0.01 BTC x 10 times
- Check: Does progress update correctly?

**5. Rapid Filtering**
- Quickly switch between filters
- Test: Does UI respond smoothly?

**6. Search Edge Cases**
- Search with numbers: "10000"
- Search with special chars: "& - ,"
- Empty search
- Very long search term

**7. Progress Bar Edge Cases**
- Campaign at exactly 100%
- Campaign over 100%
- Campaign at 0%
- Campaign at 99.99%

---

## 🎯 Expected Behavior

### When You Donate:
✅ Success message appears
✅ Progress bar updates immediately
✅ Current amount increases
✅ Percentage recalculates
✅ If >= 100%, status changes to "Funded"

### When You Filter:
✅ List updates instantly
✅ Count shows correct number
✅ Empty message if no results
✅ Can combine with search

### When You Search:
✅ Case-insensitive matching
✅ Searches title and owner
✅ Results update as you type
✅ Works with filters

### When You Update Status:
✅ Status changes immediately
✅ If "Closed", donation disabled
✅ Success message appears
✅ Can revert changes

---

## 📸 Screenshots to Capture

Document your testing:

1. **Campaign List View** (all 17 campaigns)
2. **Filter: Active Only** (10 campaigns)
3. **Filter: Funded Only** (7 campaigns)
4. **Search: "school"** (2 results)
5. **Campaign Card** (with progress bar)
6. **Donation Process** (before/after)
7. **Campaign at 100%** (fully funded)
8. **Statistics Dashboard** (updated numbers)
9. **Campaign Over 100%** (Local Food Bank at 200%)
10. **Empty Search Results**

---

## 🔄 Reset Test Data

If you want to start fresh:

```powershell
cd backend
Remove-Item data/openfunds.db -Force
# Restart backend to create new database
```

Or keep existing data and add more:
```powershell
# Run the demo script
cd OpenFunds-v2
.\demo.ps1
# Choose option 4: Create Demo Data
```

---

## 📊 Campaign Categories for Testing

| Category | Count | Use For Testing |
|----------|-------|-----------------|
| Environmental | 3 | Eco-friendly projects |
| Education | 3 | Learning initiatives |
| Emergency | 2 | Urgent needs |
| Animals | 1 | Wildlife/pets |
| Social Impact | 3 | Community services |
| Arts & Culture | 2 | Creative projects |
| Funded | 7 | Completed campaigns |

---

## 🎮 Fun Testing Challenges

**Challenge 1: Fund a Campaign**
- Pick: Street Dog Rescue (0%)
- Goal: Bring it to 100%
- Prize: Satisfaction of helping digital dogs! 🐕

**Challenge 2: Search Master**
- Find all campaigns with "community" (3+)
- Find campaigns about education (3+)
- Find the most expensive campaign (Renewable Energy)

**Challenge 3: Progress Hunter**
- Find campaign at 0%
- Find campaign at ~25%
- Find campaign at ~90%
- Find campaign at 100%+

**Challenge 4: Filter Champion**
- Use all 3 filter options
- Combine with all 3 sort options
- Add search to each combination
- Count: 3×3 = 9 combinations!

---

## ✅ Testing Checklist

- [ ] View all 17 campaigns
- [ ] Filter by each status
- [ ] Sort by each option
- [ ] Search for "school", "ocean", "community"
- [ ] Make donation to 0% campaign
- [ ] Make donation to bring campaign to 100%
- [ ] Try to donate to funded campaign
- [ ] Update campaign status
- [ ] Check statistics update
- [ ] Test progress bars display correctly
- [ ] Verify BTC amounts are accurate
- [ ] Test rapid clicking (UI stability)
- [ ] Test with slow internet (optional)
- [ ] Test on different browsers (optional)

---

## 🆘 Troubleshooting

**Problem:** Campaigns not showing
- **Solution:** Refresh browser (F5)

**Problem:** Donation doesn't update
- **Solution:** Check backend logs for errors

**Problem:** Statistics wrong
- **Solution:** Backend might be calculating, refresh

**Problem:** Too many test campaigns
- **Solution:** Use filters to organize them

---

## 🎉 You Now Have:

✅ **17 diverse test campaigns**
✅ **Multiple funding stages** (0%, 25%, 90%, 100%, 200%)
✅ **Different categories** (education, environment, social, etc.)
✅ **Various target amounts** (1.2 to 6.0 BTC)
✅ **Mix of active and funded** campaigns
✅ **Realistic descriptions** and addresses
✅ **Perfect for comprehensive testing!**

---

**Happy Testing! 🚀**

**Refresh your browser:** http://localhost:8501
