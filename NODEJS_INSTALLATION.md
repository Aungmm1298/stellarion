# 🚀 Node.js Installation Guide

## ⚡ IMPORTANT: You DON'T Need Node.js!

**Your website works WITHOUT Node.js!**

Everything runs directly in the browser:
- ✅ Upload images (uses ImgBB free hosting)
- ✅ Generate 3D models (calls Meshy API directly)
- ✅ Shopping cart, wishlist, profiles
- ✅ 3D viewer with Three.js

**Just open `index.html` in your browser - it works!**

---

## 🤔 When DO You Need Node.js?

Only if you want the **optional backend server** for:
- Hiding API key server-side (security)
- Custom image processing
- Backend database integration

**For now, skip this! Use the browser version!**

---

## 💻 Install Node.js (If You Really Want)

### Step 1: Download Node.js

1. Go to: **https://nodejs.org/**
2. Download the **LTS version** (Long Term Support)
   - Recommended: v20.x or v18.x
3. Run the installer (`.msi` file)

### Step 2: Install

1. Click **"Next"** through the installer
2. Accept license agreement
3. Keep default installation path: `C:\Program Files\nodejs\`
4. Check **"Automatically install necessary tools"** ✅
5. Click **"Install"**
6. Wait 2-3 minutes
7. Click **"Finish"**

### Step 3: Verify Installation

Open PowerShell and run:

```powershell
node --version
npm --version
```

Should show:
```
v20.x.x
10.x.x
```

If you see version numbers, it worked! ✅

### Step 4: Install Project Dependencies

```powershell
cd "C:\Users\User\Documents\Stellarion(Hylife)"
npm install
```

This installs:
- express (web server)
- cors (cross-origin support)
- axios (HTTP client)
- form-data (file uploads)

### Step 5: Start Backend Server

```powershell
npm start
```

Server runs on: `http://localhost:3000`

---

## 🔧 If Installation Fails

### Error: "npm not recognized"

**Solution 1: Restart PowerShell**
```powershell
# Close and reopen PowerShell
node --version
npm --version
```

**Solution 2: Restart Computer**
- Node.js needs system restart to update PATH
- Reboot your PC
- Try again

**Solution 3: Manual PATH Fix**

1. Press `Win + R`
2. Type: `sysdm.cpl`
3. Go to **"Advanced"** tab
4. Click **"Environment Variables"**
5. Under "System variables", find **"Path"**
6. Click **"Edit"**
7. Add: `C:\Program Files\nodejs\`
8. Click **"OK"** on all windows
9. Restart PowerShell

---

## ⚠️ Common Issues

### Issue: "EACCES: permission denied"

**Solution:** Run PowerShell as Administrator
1. Right-click PowerShell
2. Select **"Run as Administrator"**
3. Try `npm install` again

### Issue: "Cannot find module"

**Solution:** Delete and reinstall
```powershell
Remove-Item node_modules -Recurse -Force
Remove-Item package-lock.json
npm install
```

### Issue: "Network error"

**Solution:** Check internet connection or use different npm registry
```powershell
npm config set registry https://registry.npmjs.org/
npm install
```

---

## 🎯 What You Actually Need

### WITHOUT Node.js (Current Setup):
✅ **Works now!**
- Open `index.html` in browser
- Upload images (ImgBB)
- Generate 3D models (Meshy API)
- Everything functional

### WITH Node.js (Optional Backend):
🔒 **Better security**
- API key hidden server-side
- Custom image processing
- More control over uploads

---

## 🚀 Quick Start (No Node.js Needed!)

**Just do this:**

1. Open `index.html` in your browser
2. Click cube icon (🧊)
3. Click "Upload File" tab
4. Upload your image
5. Generate 3D model

**It works! No npm, no Node.js required!**

---

## 📦 What `npm install` Would Install

If you had Node.js, these would be installed:

```json
{
  "express": "^4.18.2",      // Web server
  "cors": "^2.8.5",          // CORS support
  "axios": "^1.6.0",         // HTTP requests
  "form-data": "^4.0.0"      // File uploads
}
```

**But you don't need them!** Browser version works great!

---

## 💡 Recommendation

### For Testing/Personal Use:
**DON'T install Node.js**
- Use current browser setup
- Works perfectly fine
- No installation needed
- Simpler to use

### For Production/Public Website:
**DO install Node.js**
- Setup backend server
- Hide API keys
- Better security
- More reliable

---

## 🆘 Need Help?

### Can't Install Node.js?
**Don't worry!** Your website works without it.

### Want Backend Server?
1. Install Node.js from https://nodejs.org/
2. Restart computer
3. Run `npm install` in project folder
4. Run `npm start` to start server

### Just Want to Generate 3D Models?
**Open `index.html` now!** Everything works!

---

## ✅ Summary

| Feature | Without Node.js | With Node.js |
|---------|----------------|--------------|
| Website works | ✅ Yes | ✅ Yes |
| Upload images | ✅ Yes (ImgBB) | ✅ Yes (Firebase) |
| Generate 3D | ✅ Yes | ✅ Yes |
| API key visible | ⚠️ In browser | ✅ Hidden |
| Setup time | 0 minutes | 10 minutes |
| **Recommended for you** | **✅ YES** | Later |

---

## 🎉 You're Good to Go!

**Don't install Node.js right now.**

**Just:**
1. Open `index.html`
2. Use the website
3. Upload images
4. Generate 3D models

**Everything works!** 🚀

---

**Download Node.js later if needed:** https://nodejs.org/

**For now, just use the browser version!**
