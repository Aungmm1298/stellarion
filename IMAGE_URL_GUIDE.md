# 🖼️ How to Get Direct Image URLs

## ❌ The Problem

You entered: `https://www.bing.com/images/search?view=detailV2&ccid=...`

**This is a Bing search page URL, NOT a direct image URL!**

Meshy API needs a **direct link to the image file**, like:
- `https://images.unsplash.com/photo-1555041469-a586c61ea9bc.jpg` ✅
- `https://i.imgur.com/abc123.png` ✅

---

## ✅ Solution 1: Get Direct Image URL from Bing

### Step-by-Step:

1. **Go to Bing Image Search** results
2. **Click the image** to open it
3. **Right-click the large image**
4. Select **"Copy image address"** or **"Open image in new tab"**
5. **Paste that URL** in the admin panel

**The URL should end with:** `.jpg`, `.png`, `.webp`, or `.jpeg`

---

## ✅ Solution 2: Upload Your File (EASIEST!)

**Don't bother with URLs!** Just upload directly:

1. Click **"Upload File"** tab in admin panel
2. Click or drag your image
3. Wait for upload (5-30 seconds)
4. System automatically creates public URL
5. Click "Generate 3D Model"

**No URL needed!** 🎉

---

## ✅ Solution 3: Use Free Image Hosting

### Option A: Imgur (Recommended)

1. Go to **https://imgur.com/upload**
2. Upload your image
3. Right-click uploaded image
4. Select **"Copy image address"**
5. URL looks like: `https://i.imgur.com/abc123.jpg`
6. Use this URL ✅

### Option B: Unsplash (For Test Images)

1. Go to **https://unsplash.com/s/photos/sofa**
2. Click any image
3. Click **"Download"** button
4. Right-click downloaded image → "Copy image address"
5. Or use Unsplash source: `https://source.unsplash.com/1600x900/?sofa`

### Option C: ImgBB

1. Go to **https://imgbb.com/**
2. Upload image
3. Copy direct link
4. Use it!

---

## 🔍 How to Identify Direct Image URLs

### ✅ VALID (Direct Image URLs):
```
https://images.unsplash.com/photo-1555041469-a586c61ea9bc
https://i.imgur.com/abc123.jpg
https://cdn.example.com/sofa.png
https://example.com/images/product.webp
```

**Key features:**
- ✅ Ends with `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`
- ✅ Direct link to image file
- ✅ Opens the image directly when clicked

### ❌ INVALID (Search/Page URLs):
```
https://www.bing.com/images/search?view=detailV2&ccid=...
https://www.google.com/search?q=sofa&tbm=isch
https://pinterest.com/pin/123456789/
https://www.facebook.com/photo.php?fbid=...
```

**These are:**
- ❌ Search result pages
- ❌ Image viewer pages
- ❌ Social media links
- ❌ Won't work with Meshy API!

---

## 🎯 Quick Test

### Test Your URL:

**Paste the URL in a new browser tab:**
- If you see **ONLY the image** → ✅ Valid!
- If you see a **webpage with the image** → ❌ Invalid!

---

## 📋 Step-by-Step: Bing to Direct URL

### Method 1: Copy Image Address

1. **Find your sofa image** in Bing search
2. **Click the image** thumbnail
3. **Wait for large preview** to load
4. **Right-click the large image**
5. Select **"Copy image address"** (NOT "Copy image link")
6. **Paste in admin panel**

### Method 2: Open in New Tab

1. **Find your sofa image** in Bing search
2. **Right-click the thumbnail**
3. Select **"Open image in new tab"**
4. **New tab opens** with just the image
5. **Copy URL from address bar**
6. **Paste in admin panel**

---

## 💡 Pro Tips

### Tip 1: Right-Click is Your Friend
Always right-click the image and select "Copy image address"

### Tip 2: Check the URL
Valid URLs usually contain:
- `images.unsplash.com`
- `i.imgur.com`
- `cdn.` or `static.`
- Ends with image extension

### Tip 3: When in Doubt, Upload
**Easiest solution:** Just use "Upload File" tab!
- No URL hunting needed
- Works with any image
- Automatic hosting
- 5 seconds and done!

---

## 🚀 Recommended Workflow

### For Your Own Images:
**Use "Upload File" tab** ← Best option!

### For Test Images:
**Use Unsplash:**
1. Go to https://unsplash.com/s/photos/furniture
2. Click image
3. Right-click → "Copy image address"
4. Paste URL
5. Generate!

---

## 📝 Example: Getting Sofa Image

### From Unsplash (Easy):
```
1. Visit: https://unsplash.com/s/photos/sofa
2. Click any sofa image
3. Right-click → "Copy image address"
4. Get URL like:
   https://images.unsplash.com/photo-1555041469-a586c61ea9bc

✅ Use this URL!
```

### From Your Computer (Easiest):
```
1. Click "Upload File" tab
2. Select your sofa image
3. Wait 10 seconds
4. Click "Generate 3D Model"

✅ Done! No URL needed!
```

---

## ⚠️ Common Mistakes

### Mistake 1: Using Search URLs
```
❌ https://www.bing.com/images/search?...
❌ https://www.google.com/search?...
```
**Fix:** Get the direct image URL instead!

### Mistake 2: Using Social Media Links
```
❌ https://facebook.com/photo/...
❌ https://instagram.com/p/...
```
**Fix:** Download image, then upload!

### Mistake 3: Using Local Paths
```
❌ C:\Users\User\Pictures\sofa.jpg
❌ file:///C:/images/sofa.png
```
**Fix:** Use "Upload File" tab!

---

## ✅ Best Solutions Ranked

1. **🥇 Upload File Tab** (Easiest!)
   - No URL needed
   - Works every time
   - 5 seconds

2. **🥈 Imgur Upload** (Quick!)
   - Free forever
   - Fast upload
   - Reliable

3. **🥉 Unsplash** (For testing)
   - Free stock photos
   - High quality
   - Direct URLs

---

## 🎉 Summary

**Your Bing URL won't work because it's a search page, not an image!**

**Quick Fix:**
1. **Best:** Click "Upload File" tab and upload directly
2. **Alternative:** Right-click image → "Copy image address"
3. **For testing:** Use Unsplash images

**Need help?** Check the examples in the admin panel!

---

**Last Updated:** November 18, 2025  
**Issue:** Bing search URL vs direct image URL
