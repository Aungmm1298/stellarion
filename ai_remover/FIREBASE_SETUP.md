# 🔥 Firebase Setup Guide for Image Upload

## Quick Start (2 Options)

### Option 1: Use Free Image Hosting (NO SETUP NEEDED!) ✅
The system will automatically use **ImgBB** free image hosting if Firebase is not configured.
Just upload your image and it works!

### Option 2: Setup Firebase (Recommended for Production)
Follow the steps below to use Google Firebase for reliable image hosting.

---

## 🚀 Firebase Setup (5 Minutes)

### Step 1: Create Firebase Project

1. Go to https://console.firebase.google.com/
2. Click **"Add project"** or **"Create a project"**
3. Enter project name: `stellarion-3d` (or your choice)
4. Disable Google Analytics (optional, not needed)
5. Click **"Create project"**
6. Wait for setup to complete

### Step 2: Enable Storage

1. In your Firebase project, click **"Storage"** in left sidebar
2. Click **"Get Started"**
3. Click **"Next"** (default security rules)
4. Choose location: **"us-central1"** or your preferred region
5. Click **"Done"**

### Step 3: Update Security Rules

1. Click **"Rules"** tab in Storage
2. Replace the rules with:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /product-images/{allPaths=**} {
      allow read: if true;  // Anyone can read
      allow write: if request.resource.size < 10 * 1024 * 1024  // Max 10MB
                   && request.resource.contentType.matches('image/.*');  // Only images
    }
  }
}
```

3. Click **"Publish"**

### Step 4: Get Firebase Config

1. Click the **gear icon** (Settings) near "Project Overview"
2. Select **"Project settings"**
3. Scroll down to **"Your apps"** section
4. Click the **web icon (</>)** to add a web app
5. Enter app nickname: `Stellarion Website`
6. Click **"Register app"**
7. Copy the **firebaseConfig** object

### Step 5: Update Your Website

Open `index.html` and find this section (around line 1005):

```javascript
// Firebase Configuration
const firebaseConfig = {
    apiKey: "AIzaSyBXXXXXXXXXXXXXXXXXXXXXXXXXXXX", // Replace
    authDomain: "stellarion-3d.firebaseapp.com", // Replace
    projectId: "stellarion-3d", // Replace
    storageBucket: "stellarion-3d.appspot.com", // Replace
    messagingSenderId: "123456789012", // Replace
    appId: "1:123456789012:web:xxxxxxxxxxxxx" // Replace
};
```

**Replace with YOUR values from Firebase:**

```javascript
const firebaseConfig = {
    apiKey: "YOUR_ACTUAL_API_KEY",
    authDomain: "your-project-id.firebaseapp.com",
    projectId: "your-project-id",
    storageBucket: "your-project-id.appspot.com",
    messagingSenderId: "YOUR_SENDER_ID",
    appId: "YOUR_APP_ID"
};
```

### Step 6: Test It!

1. Save `index.html`
2. Refresh your website
3. Open browser console (F12)
4. Look for: `"Firebase initialized successfully"`
5. If you see it, Firebase is ready! ✅

---

## 📤 How to Use Image Upload

### Method 1: Upload File (With Firebase or ImgBB)

1. Click **cube icon (🧊)** to open admin panel
2. Switch to **"Upload File"** tab
3. Click **"Click to upload image"** or drag & drop
4. Wait for upload (5-30 seconds)
5. See ✅ "Upload complete!"
6. Enter product name
7. Click **"Generate 3D Model"**

### Method 2: Use URL (No Upload Needed)

1. Click **cube icon (🧊)**
2. Stay on **"From URL"** tab
3. Enter product name
4. Paste public image URL:
   ```
   https://images.unsplash.com/photo-1555041469-a586c61ea9bc
   ```
5. Click **"Generate 3D Model"**

---

## 🎯 Which Method to Use?

### Use "Upload File" when:
- ✅ You have local images on your computer
- ✅ You want to use your own product photos
- ✅ Images are not publicly available online

### Use "From URL" when:
- ✅ Image is already online (Unsplash, Imgur, etc.)
- ✅ You want to test quickly
- ✅ You don't want to wait for upload

---

## ⚠️ Common Issues

### "Firebase not configured"
**Cause:** Firebase config not set up
**Solution:** Either:
1. Follow setup steps above, OR
2. Just use it as-is! ImgBB will work automatically

### "Upload failed"
**Causes:**
- File too large (max 10MB)
- Not an image file
- Internet connection issue
- Firebase rules not set correctly

**Solutions:**
1. Check file size (must be under 10MB)
2. Use JPG, PNG, or WEBP format
3. Check internet connection
4. Verify Firebase Storage rules

### "Cannot use local file paths"
**Cause:** You entered `C:\Users\...` instead of URL
**Solution:** 
1. Switch to **"Upload File"** tab
2. Upload your local file
3. System will convert it to public URL automatically

---

## 💰 Firebase Pricing

### Free Tier (Spark Plan):
- ✅ **5 GB storage** - Enough for ~5,000 product images
- ✅ **1 GB/day download** - Plenty for testing
- ✅ **20,000 reads/day** - More than enough
- ✅ **20,000 writes/day** - Sufficient

### Paid Tier (Blaze Plan):
- Only if you exceed free tier
- Pay-as-you-go pricing
- Very cheap for most use cases

**For this project:** Free tier is MORE than enough!

---

## 🔧 Alternative: ImgBB (Built-in!)

If you don't want to setup Firebase, the system automatically uses **ImgBB** free hosting:

### Advantages:
- ✅ No setup needed
- ✅ Free forever
- ✅ Works immediately
- ✅ Fast uploads

### Limitations:
- ⚠️ Demo API key (limited rate)
- ⚠️ Less reliable than Firebase
- ⚠️ No control over storage

### Get Your Own ImgBB Key (Optional):
1. Go to https://api.imgbb.com/
2. Sign up for free account
3. Get your API key
4. Update in `script.js` line ~1340:
   ```javascript
   const response = await fetch('https://api.imgbb.com/1/upload?key=YOUR_KEY', {
   ```

---

## 🎨 Recommended Image Specs

For best 3D model results:

### Resolution:
- **Minimum:** 1024 x 1024 px
- **Recommended:** 2048 x 2048 px
- **Maximum:** 4096 x 4096 px (10MB limit)

### Format:
- ✅ **JPG** - Best for photos
- ✅ **PNG** - Best for transparent backgrounds
- ✅ **WEBP** - Best compression

### Content:
- ✅ Product centered in frame
- ✅ Good lighting (no harsh shadows)
- ✅ Clean background (white/neutral)
- ✅ Single product (not group shots)
- ✅ Front-facing angle

---

## 📊 Testing Checklist

### Without Firebase:
- [ ] Open website
- [ ] Click cube icon
- [ ] Switch to "Upload File" tab
- [ ] Upload an image (under 10MB)
- [ ] See "Uploading to ImgBB..."
- [ ] See "✅ Upload complete!"
- [ ] Generate 3D model works

### With Firebase:
- [ ] Open website
- [ ] Check console for "Firebase initialized"
- [ ] Click cube icon
- [ ] Upload an image
- [ ] See "Uploading to Firebase..."
- [ ] See progress percentage
- [ ] See "✅ Upload complete!"
- [ ] Generate 3D model works

---

## 🆘 Get Help

### Firebase Issues:
- **Documentation:** https://firebase.google.com/docs/storage
- **Console:** https://console.firebase.google.com/
- **Support:** https://firebase.google.com/support

### ImgBB Issues:
- **Documentation:** https://api.imgbb.com/
- **Get API Key:** https://imgbb.com/signup

### General Upload Issues:
1. Check browser console (F12) for errors
2. Try smaller image (under 5MB)
3. Try different image format
4. Use URL method instead
5. Check internet connection

---

## 🎉 You're Ready!

Your website now supports **TWO methods** for image input:

1. **Upload File** - Upload from computer (Firebase or ImgBB)
2. **From URL** - Use public URLs (Unsplash, Imgur, etc.)

**No Firebase setup needed** - ImgBB works out of the box!
**Want better control?** - Setup Firebase in 5 minutes!

---

**Last Updated:** November 18, 2025
**Firebase SDK Version:** 10.7.1
