# 🔧 Meshy API Troubleshooting Guide

## Error: "NoMatchingRoute"

This error typically means one of the following:

### 1. **API Endpoint Issue**
The Meshy API endpoint might have changed or the route doesn't exist.

**Check:**
- Visit https://docs.meshy.ai/ for latest API documentation
- Verify endpoint is: `https://api.meshy.ai/v2/image-to-3d`
- Ensure using POST method

### 2. **API Key Invalid/Expired**
Your API key might be incorrect, expired, or revoked.

**Solution:**
1. Go to https://app.meshy.ai/
2. Log in to your account
3. Navigate to API settings
4. Copy your current API key
5. Update in `script.js` line 15:
   ```javascript
   const API_KEY = 'YOUR_NEW_KEY_HERE';
   ```

### 3. **API Credits Exhausted**
You might have used up your free/paid credits.

**Check:**
- Visit https://app.meshy.ai/dashboard
- Look at your remaining credits
- Purchase more if needed

### 4. **Account Issues**
Your Meshy account might have issues.

**Solutions:**
- Verify your email address
- Check account status
- Ensure payment method is valid (if paid plan)

---

## 🧪 How to Test & Fix

### Step 1: Test API Connection
1. Open your website (`index.html`)
2. Click the cube icon (🧊)
3. Click **"Test API"** button
4. Read the response message

### Step 2: Check Browser Console
1. Press **F12** to open developer tools
2. Go to **Console** tab
3. Look for detailed error messages
4. Screenshot any errors you see

### Step 3: Verify API Key
```javascript
// In browser console, run:
console.log('API Key:', 'kiri_oZ9V44rQlpQrD5lG8nLZs0fJLlwxBssAU6nRqtkuKUM');
```

### Step 4: Test with Standalone Tool
Open `test-meshy-api.html` and try:
- Click "List All Models" first
- Then try a new generation
- This isolated test will show exact errors

---

## 📞 Common Solutions

### Solution A: Get New API Key
1. Go to https://app.meshy.ai/
2. Sign in / Sign up for account
3. Go to Settings → API
4. Generate new API key
5. Copy the key
6. Update `script.js`:
   ```javascript
   const API_KEY = 'YOUR_NEW_KEY_HERE';
   ```
7. Save and refresh website

### Solution B: Check API Documentation
1. Visit https://docs.meshy.ai/
2. Look for "Image to 3D" endpoint
3. Check if endpoint URL changed
4. Verify request body format
5. Update code if needed

### Solution C: Use Alternative Method
If direct API doesn't work, use the backend approach:

1. Install Node.js from https://nodejs.org/
2. Open PowerShell in project folder
3. Run: `npm install`
4. Run: `npm start`
5. Backend server will handle API calls
6. Update `script.js` to use `http://localhost:3000/api/...`

---

## 🔍 Detailed Error Checking

### Check 1: Network Request
**In browser console:**
```javascript
fetch('https://api.meshy.ai/v2/image-to-3d', {
    method: 'GET',
    headers: {
        'Authorization': 'Bearer kiri_oZ9V44rQlpQrD5lG8nLZs0fJLlwxBssAU6nRqtkuKUM'
    }
}).then(r => r.json()).then(console.log).catch(console.error);
```

### Check 2: API Status
Visit: https://status.meshy.ai/ (if exists)
Or check their support channels

### Check 3: CORS Issues
**In console, look for:**
- "CORS policy" errors
- "Access-Control-Allow-Origin" errors

**Fix:** Use backend server (server.js with Node.js)

---

## 🆘 Getting Help

### 1. Meshy Support
- Email: support@meshy.ai
- Discord: https://discord.gg/meshy (check for invite link)
- Documentation: https://docs.meshy.ai/

### 2. Check Your Settings
Go to https://app.meshy.ai/ and verify:
- [x] Account is active
- [x] Email is verified
- [x] Credits remaining
- [x] API key is active
- [x] No rate limits hit

### 3. Alternative: Manual Test
1. Go to https://app.meshy.ai/
2. Use their web interface to generate a 3D model
3. If that works, problem is with API integration
4. If that doesn't work, problem is with account/credits

---

## 🔄 API Request Format

### Correct Format (Current):
```javascript
POST https://api.meshy.ai/v2/image-to-3d

Headers:
  Authorization: Bearer YOUR_API_KEY
  Content-Type: application/json

Body:
{
  "image_url": "https://...",
  "enable_pbr": true,
  "name": "Product Name",
  "ai_model": "meshy-4",
  "topology": "quad",
  "target_polycount": 30000
}
```

### Response (Success):
```json
{
  "result": "task-id-here-1234567890"
}
```

### Response (Error):
```json
{
  "message": "Error description",
  "error": "ERROR_CODE"
}
```

---

## 🛠️ Quick Fixes

### Fix 1: Update API Endpoint
If Meshy changed their API, update in `script.js`:
```javascript
const MESHY_API_URL = 'https://api.meshy.ai/v2'; // Old
const MESHY_API_URL = 'https://api.meshy.ai/v3'; // New? Check docs
```

### Fix 2: Change AI Model
Try different model version:
```javascript
"ai_model": "meshy-3" // Instead of "meshy-4"
```

### Fix 3: Simplify Request
Remove optional parameters:
```javascript
body: JSON.stringify({
  image_url: imageUrl,
  name: productName
  // Remove: enable_pbr, ai_model, topology, target_polycount
})
```

---

## 📊 Expected Behavior

### Normal Flow:
1. **Input** → Product name + Image URL
2. **Click Generate** → Shows "Starting..."
3. **API Call** → POST to Meshy
4. **Response** → Task ID returned
5. **Polling** → Check status every 5 seconds
6. **Progress** → 0% → 25% → 50% → 75% → 100%
7. **Complete** → GLB URL available
8. **Download/Preview** → Use the model

### If Stuck at "Starting...":
- API call failed immediately
- Check console for error
- Run "Test API" button
- Verify API key

---

## 🔐 Security Note

Your API key is exposed in frontend code:
```javascript
const API_KEY = 'kiri_oZ9V44rQlpQrD5lG8nLZs0fJLlwxBssAU6nRqtkuKUM';
```

**For Production:**
1. Use the `server.js` backend
2. Keep API key server-side only
3. Frontend calls your backend
4. Backend calls Meshy API

**Setup Backend:**
```powershell
# Install Node.js first, then:
npm install
npm start

# Server runs on http://localhost:3000
# Update script.js to use localhost endpoints
```

---

## 📱 Contact Information

**Meshy.ai Resources:**
- Website: https://meshy.ai/
- Dashboard: https://app.meshy.ai/
- Documentation: https://docs.meshy.ai/
- API Reference: https://docs.meshy.ai/api-reference

**Your Current Setup:**
- API Key: `kiri_oZ9V44rQlpQrD5lG8nLZs0fJLlwxBssAU6nRqtkuKUM`
- Endpoint: `https://api.meshy.ai/v2/image-to-3d`
- Method: Direct browser fetch (no backend)

---

## ✅ Checklist Before Asking for Help

When reporting issues, provide:

- [ ] Error message from console (F12)
- [ ] Screenshot of error
- [ ] Result of "Test API" button
- [ ] Your Meshy account status
- [ ] Credits remaining
- [ ] Image URL you're using
- [ ] Browser and version
- [ ] Date/time of error

---

## 🎯 Most Likely Solutions

**90% of issues are:**

1. **Invalid/Expired API Key** → Get new one from Meshy dashboard
2. **No Credits Remaining** → Purchase more credits
3. **Invalid Image URL** → Use publicly accessible URL
4. **Account Not Verified** → Check email and verify account

**Try these in order!**

---

**Last Updated:** November 18, 2025
**Meshy API Version:** v2
