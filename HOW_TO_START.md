# 🚀 How to Start the Application

## ⚠️ Important: Backend Must Run First!

The website **CANNOT work without the backend server running**. Here's why:

- **Frontend** (`index.html`) = The user interface (runs in browser)
- **Backend** (`api.py`) = The AI brain (Python server with all processing)

When you open `index.html` directly, it's just a static webpage. All the AI magic happens in the Python backend server that must be running at `http://localhost:8000`.

---

## 🎯 Three Ways to Start

### **Option 1: One-Click Startup (Easiest)** ⭐

Double-click: **`START_EVERYTHING.bat`**

This will:
1. Start the backend server in a new window
2. Wait for models to load (5-10 seconds)
3. Open the project folder
4. Then you manually open `index.html` in your browser

---

### **Option 2: Manual Startup (Recommended)**

**Step 1 - Start Backend:**
```bash
cd backend
python api.py
```
Wait until you see:
```
✓ U2Net model loaded successfully
✓ Real-ESRGAN model loaded successfully
Uvicorn running on http://0.0.0.0:8000
```

**Step 2 - Open Frontend:**
- Open `index.html` in your browser
- OR use VS Code Live Server extension (right-click → "Open with Live Server")

---

### **Option 3: Use Existing START.bat**

Double-click: **`START.bat`**

This attempts to:
1. Start backend with virtual environment
2. Auto-open `index.html`

**Note:** Requires virtual environment setup first.

---

## 🔍 Troubleshooting "Cannot Connect to Backend"

### **Check if Backend is Running:**

Open a browser and visit: **http://localhost:8000**

**✅ If you see JSON like this:**
```json
{
  "status": "online",
  "service": "AI Background Remover API",
  "models": {...}
}
```
→ Backend is running! Refresh your main page.

**❌ If you see "Unable to connect":**
→ Backend is NOT running. Start it first!

---

## 📝 Startup Checklist

Every time you want to use the application:

- [ ] Open terminal/command prompt
- [ ] Navigate to backend folder: `cd backend`
- [ ] Run: `python api.py`
- [ ] Wait for "Uvicorn running on http://0.0.0.0:8000"
- [ ] See both models load successfully (U2Net + Real-ESRGAN)
- [ ] Keep this terminal window open (don't close it!)
- [ ] NOW open `index.html` in browser
- [ ] Check connection indicator turns green

---

## 🎮 Quick Commands

### Start Backend Only:
```bash
cd backend
python api.py
```

### Check if Backend is Running:
```bash
curl http://localhost:8000/api/status
```
Or open in browser: http://localhost:8000

### Stop Backend:
Press `CTRL+C` in the terminal where it's running

---

## 💡 Pro Tips

1. **Keep backend terminal open** - Don't close the window where `python api.py` is running
2. **Use VS Code Live Server** - Better than opening HTML directly (avoids CORS issues)
3. **Bookmark the status page** - http://localhost:8000/api/status to quickly check if backend is up
4. **Check backend logs** - If something fails, the terminal shows detailed error messages
5. **Restart when needed** - If something breaks, `CTRL+C` to stop, then run `python api.py` again

---

## 🔧 First Time Setup

If you haven't installed dependencies yet:

```bash
cd backend
pip install -r requirements.txt
```

This installs:
- FastAPI (web server)
- OpenCV (image processing)
- NumPy, SciPy (math operations)
- rembg (U²Net background removal)
- Real-ESRGAN (image enhancement)
- All other dependencies

---

## 📊 Startup Sequence Visual

```
Step 1: Terminal              Step 2: Browser
┌─────────────────┐          ┌──────────────────┐
│ cd backend      │          │ Open index.html  │
│ python api.py   │    →     │                  │
│                 │          │ ✅ Connected!    │
│ [Server Running]│          │                  │
└─────────────────┘          └──────────────────┘
  Keep this open!              Can now use app
```

---

## ❓ Common Questions

**Q: Why doesn't the website work when I open index.html?**  
A: Because the Python backend isn't running. Start it first!

**Q: Do I need to start the backend every time?**  
A: Yes, unless you set it up as a system service (advanced).

**Q: Can I use the app without the backend?**  
A: No, all AI processing happens in the backend. The frontend is just UI.

**Q: The backend window closed, what do I do?**  
A: Reopen terminal and run `cd backend; python api.py` again.

**Q: How do I know if backend is working?**  
A: Visit http://localhost:8000 - you should see JSON status response.

---

## 🎯 Remember

**Always start the backend BEFORE opening the website!**

Backend → Frontend → Use Application

---

**Having issues?** Check:
1. Python 3.8+ installed: `python --version`
2. Dependencies installed: `pip list | grep fastapi`
3. Port 8000 available (not used by another app)
4. No firewall blocking localhost:8000

---

**Quick Test:**
```bash
# Terminal 1
cd backend
python api.py

# Browser
http://localhost:8000       ← Should show status JSON
http://localhost:8000/docs  ← Should show API documentation

# Then open index.html
```

---

**Version:** 2.0.0  
**Last Updated:** November 23, 2025
