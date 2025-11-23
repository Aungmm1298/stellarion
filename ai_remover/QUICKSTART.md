# Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Setup Backend (One-time)

**Windows:**
```powershell
cd backend
setup.bat
```

**Mac/Linux:**
```bash
cd backend
chmod +x setup.sh
./setup.sh
```

This will:
- Create Python virtual environment
- Install all dependencies
- Download AI models (first run only)

### Step 2: Start Backend Server

```bash
cd backend
venv\Scripts\activate    # Windows
source venv/bin/activate # Mac/Linux
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Loading Real-ESRGAN model...
INFO:     Real-ESRGAN model loaded successfully!
```

### Step 3: Open Frontend

1. Open VS Code
2. Right-click `index.html`
3. Select "Open with Live Server"

OR simply open `index.html` in your browser!

## ✅ Verify It's Working

1. Go to http://localhost:8000/docs - You should see API documentation
2. On the frontend, you should see: "Ready! Using Python AI backend (CPU)" or "(CUDA)"
3. Upload an image - it should process automatically!

## 🎯 What You Can Do

### Background Removal
- Upload furniture/product images
- Automatic background removal using U²Net AI
- Download transparent PNG

### Image Enhancement
- Click "✨ AI Enhance" button
- Uses Real-ESRGAN for 2x upscaling
- Improves image quality and details

### API Usage
```python
import requests

# Remove background
with open('furniture.jpg', 'rb') as f:
    r = requests.post('http://localhost:8000/api/remove-background',
                      files={'file': f})
    
with open('output.png', 'wb') as f:
    f.write(r.content)
```

## 🐛 Common Issues

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Port 8000 already in use"
```bash
# Find and kill process on port 8000
# Windows: netstat -ano | findstr :8000
# Mac/Linux: lsof -ti:8000 | xargs kill
```

### Frontend not connecting
1. Make sure backend is running (http://localhost:8000)
2. Check browser console for errors
3. Update `API_BASE_URL` in script.js if needed

## 📚 More Info

- Full documentation: See `BACKEND_README.md`
- API docs: http://localhost:8000/docs
- Test API: http://localhost:8000/api/status

## 🎉 You're Ready!

Upload an image and watch the AI magic happen! 🪄
