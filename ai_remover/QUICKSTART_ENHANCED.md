# 🚀 Quick Start Guide - AI Background Remover

## Get Started in 3 Steps

### Step 1: Start the Backend
```bash
cd backend
python -m uvicorn api:app --host 0.0.0.0 --port 8000
```
Or double-click `backend/START.bat` (Windows)

### Step 2: Open the Frontend
- Double-click `index.html`
- Or use Live Server in VS Code
- Or visit: `http://localhost:8080`

### Step 3: Process Your First Image
1. Click "Choose Image(s)" or drag & drop
2. Wait 3-8 seconds for AI processing
3. Click "Download" to save result

---

## ✨ Key Features to Try

### 🎯 Basic Usage
1. **Upload** → Automatic background removal
2. **Compare** → Toggle original vs processed
3. **Download** → Save as transparent PNG

### 🔧 AI Features (Check boxes in UI)
- ✅ **Edge Refinement** - Smooth, professional edges (ON by default)
- ✅ **Auto-Crop** - Remove excess space, smaller files

### ⬆️ Quality Enhancement
- Click **"✨ Enhance Quality"** button
- 2x resolution upscaling
- Perfect for print/large displays

### 🎨 Background Options
Click preset buttons:
- 🔲 **Transparent** (default)
- ⚪ **White** (e-commerce)
- ⚫ **Black** (dramatic)
- 🔳 **Gray** (neutral)
- 🎨 **Custom** (any color)

### 📦 Batch Processing
- Select 2-10 images at once
- All processed in parallel
- Download individually or all

---

## ⌨️ Keyboard Shortcuts
- `ESC` - Back to upload
- `SPACE` - Compare mode
- `D` - Download

---

## 🔗 Important Links
- **Frontend**: `index.html` (or http://localhost:8080)
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 📚 Documentation
- `README.md` - Complete guide
- `FEATURES.md` - Detailed features
- `IMPROVEMENTS.md` - What's new
- `backend/SETUP_INSTRUCTIONS.md` - Backend setup

---

## 🆘 Troubleshooting

**Backend not starting?**
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn api:app --reload
```

**Frontend not connecting?**
- Check backend is running: http://localhost:8000/health
- Check browser console for errors
- Ensure CORS is enabled (it should be by default)

**Enhancement not working?**
- Download Real-ESRGAN model: [Link](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth)
- Place in `backend/models/` folder
- Restart backend

---

## 💡 Quick Tips

1. ✅ **Always enable edge refinement** (default ON)
2. ✅ **Use auto-crop** to reduce file size 30-60%
3. ✅ **Batch process** similar images together
4. ⚠️ **Use enhancement** only when needed (slower but better quality)
5. 💾 **Compare mode** before downloading

---

**That's it! Start processing images in under 2 minutes! 🎉**

Need more help? Check `FEATURES.md` for detailed guides.
