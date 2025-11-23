# AI Background Remover - Setup Instructions

## 📁 Folder Structure

Your project should look like this:

```
AI background remover (Hylife)/
├── backend/
│   ├── api.py                    # Main FastAPI server
│   ├── requirements.txt          # Python dependencies
│   ├── models/                   # AI model files (create this folder)
│   │   └── RealESRGAN_x2plus.pth # Download this model
│   └── SETUP_INSTRUCTIONS.md     # This file
├── index.html                    # Your frontend HTML
├── styles.css                    # Your styles
└── script.js                     # Frontend JavaScript
```

## 🚀 Installation Steps

### Step 1: Create Python Virtual Environment

```powershell
cd "C:\Users\User\Documents\AI background remover (Hylife)\backend"
python -m venv venv
.\venv\Scripts\Activate
```

### Step 2: Install Dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

**Note:** This will take 5-10 minutes as it downloads PyTorch and other large libraries.

### Step 3: Download Real-ESRGAN Model

1. Create the `models` folder:
   ```powershell
   mkdir models
   ```

2. Download the model file:
   - Go to: https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth
   - Save it to: `backend/models/RealESRGAN_x2plus.pth`

**Alternative (using PowerShell):**
```powershell
Invoke-WebRequest -Uri "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth" -OutFile "models\RealESRGAN_x2plus.pth"
```

### Step 4: Start the Backend Server

```powershell
python api.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
✓ U2Net model loaded successfully
✓ Real-ESRGAN model loaded successfully
```

## 🌐 Start the Frontend

### Option 1: VS Code Live Server
1. Right-click `index.html`
2. Select "Open with Live Server"
3. Browser opens at `http://127.0.0.1:5500/`

### Option 2: Python HTTP Server
```powershell
cd "C:\Users\User\Documents\AI background remover (Hylife)"
python -m http.server 5500
```

Visit: http://localhost:5500

## 🧪 Testing

1. Open your browser to the frontend URL
2. Upload a furniture image (or any object photo)
3. Wait for AI processing (10-30 seconds depending on image size)
4. Download the result as transparent PNG

## 🔧 Troubleshooting

### Backend won't start
- Make sure virtual environment is activated
- Check all dependencies installed: `pip list`
- Try: `pip install --force-reinstall rembg`

### "Enhancement model not available"
- Verify `RealESRGAN_x2plus.pth` is in `backend/models/` folder
- Check file size (should be ~67MB)
- Re-download if corrupted

### CORS errors
- Make sure backend is running on port 8000
- Check `script.js` has correct API_BASE_URL
- Clear browser cache

### Out of memory
- Reduce image size before uploading
- Close other applications
- Consider using CPU mode (already set in api.py)

## 📊 API Endpoints

### Main Processing
- `POST /process` - Remove background + enhance
- `POST /remove-background` - Only remove background
- `POST /enhance-only` - Only enhance quality

### Health Checks
- `GET /` - Basic status
- `GET /health` - Detailed health check

## 🎨 Model Information

### U²Net (Background Removal)
- Auto-downloaded by rembg on first use
- Size: ~176 MB
- Cached in: `~/.u2net/`

### Real-ESRGAN (Enhancement)
- Manual download required
- Size: ~67 MB
- Location: `backend/models/RealESRGAN_x2plus.pth`
- 2x upscaling with quality enhancement

## 💡 Tips

- First run will be slow (downloading U²Net model)
- Processing time: 10-30 seconds per image
- Recommended image size: < 2000x2000 pixels
- Output format: PNG with transparency
- GPU not required (runs on CPU)

## 🆘 Support

If you encounter issues:
1. Check logs in terminal where backend is running
2. Open browser console (F12) for frontend errors
3. Verify all files are in correct locations
4. Ensure Python 3.8+ is installed

## ✅ Verification Checklist

- [ ] Virtual environment created and activated
- [ ] All pip packages installed successfully
- [ ] Real-ESRGAN model downloaded to `models/` folder
- [ ] Backend starts without errors
- [ ] Frontend loads in browser
- [ ] Can upload images
- [ ] Background removal works
- [ ] Enhancement works
- [ ] Can download processed images

## 🚀 Production Deployment

For production use:
1. Use proper secrets management
2. Add rate limiting
3. Implement authentication
4. Use production ASGI server (Gunicorn + Uvicorn)
5. Add image size limits
6. Set up monitoring
7. Configure CORS properly

Good luck! 🎉
