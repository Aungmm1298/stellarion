# 🚀 AI Background Remover + Image Enhancer

A complete full-stack application with **Python FastAPI backend** and **JavaScript frontend** for removing backgrounds and enhancing images using state-of-the-art AI models.

## 🎯 Features

### Backend (Python + FastAPI)
- **rembg (U²Net)**: Advanced background removal using U²Net deep learning model
- **Real-ESRGAN**: Super-resolution image enhancement (2x or 4x upscaling)
- **Alpha Matting**: Better edge quality for transparent images
- **Fast Processing**: GPU acceleration (CUDA) when available
- **RESTful API**: Clean endpoints for all operations

### Frontend (Vanilla JavaScript)
- Drag & Drop image upload
- Real-time preview with checkerboard transparency
- Compare original vs processed images
- Client-side fallback when backend unavailable
- Responsive design

## 📋 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **rembg** - U²Net background removal
- **Real-ESRGAN** - Image super-resolution
- **PyTorch** - Deep learning framework
- **Pillow** - Image processing

### Frontend
- **Vanilla JavaScript** - No frameworks needed
- **HTML5 Canvas** - Image rendering
- **CSS3** - Modern styling

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+ (3.10 recommended)
- pip (Python package manager)
- 4GB+ RAM (8GB recommended for GPU)
- NVIDIA GPU with CUDA (optional, for faster processing)

### Backend Setup

#### Windows
```powershell
cd backend
setup.bat
```

#### Linux/Mac
```bash
cd backend
chmod +x setup.sh
./setup.sh
```

#### Manual Setup
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Start the Backend Server

```bash
# Make sure virtual environment is activated
cd backend
python main.py
```

Server will start at: **http://localhost:8000**

API Documentation: **http://localhost:8000/docs**

### Start the Frontend

#### Option 1: Live Server (VS Code)
1. Install "Live Server" extension
2. Right-click `index.html`
3. Select "Open with Live Server"

#### Option 2: Python HTTP Server
```bash
# In the root directory (not backend folder)
python -m http.server 8080
```

Then open: **http://localhost:8080**

#### Option 3: Direct File
Simply double-click `index.html` (limited functionality without backend)

## 🎮 Usage

### Using the Web Interface

1. **Start Backend**: Run `python main.py` in the backend folder
2. **Open Frontend**: Open `index.html` in your browser
3. **Upload Image**: Click or drag & drop furniture/product image
4. **Auto Process**: Background removal happens automatically
5. **AI Enhance**: Click "✨ AI Enhance" for Real-ESRGAN upscaling
6. **Compare**: Toggle between original and processed
7. **Download**: Save your transparent PNG

### API Endpoints

#### 1. Remove Background
```bash
POST http://localhost:8000/api/remove-background
Content-Type: multipart/form-data

Parameters:
- file: Image file
- alpha_matting: boolean (optional, default: false)
- alpha_matting_foreground_threshold: int (0-255, default: 240)
- alpha_matting_background_threshold: int (0-255, default: 10)

Response: PNG image with transparent background
```

#### 2. Enhance Image
```bash
POST http://localhost:8000/api/enhance-image
Content-Type: multipart/form-data

Parameters:
- file: Image file
- scale: int (2 or 4, default: 2)

Response: Enhanced PNG image
```

#### 3. Process All (Remove + Enhance)
```bash
POST http://localhost:8000/api/process-all
Content-Type: multipart/form-data

Parameters:
- file: Image file
- remove_bg: boolean (default: true)
- enhance: boolean (default: true)
- alpha_matting: boolean (default: false)
- scale: int (2 or 4, default: 2)

Response: Processed PNG image (background removed + enhanced)
```

#### 4. Check Status
```bash
GET http://localhost:8000/api/status

Response:
{
  "api_status": "online",
  "models": {
    "rembg": "available",
    "realesrgan": "loaded"
  },
  "device": "cuda"
}
```

### Testing with cURL

```bash
# Remove background
curl -X POST http://localhost:8000/api/remove-background \
  -F "file=@furniture.jpg" \
  -F "alpha_matting=true" \
  -o output_nobg.png

# Enhance image
curl -X POST http://localhost:8000/api/enhance-image \
  -F "file=@furniture.jpg" \
  -F "scale=2" \
  -o output_enhanced.png

# Full processing
curl -X POST http://localhost:8000/api/process-all \
  -F "file=@furniture.jpg" \
  -F "remove_bg=true" \
  -F "enhance=true" \
  -F "scale=2" \
  -o output_final.png
```

### Testing with Python

```python
import requests

# Remove background
with open('furniture.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/remove-background',
        files={'file': f},
        data={'alpha_matting': 'true'}
    )
    
with open('output.png', 'wb') as f:
    f.write(response.content)
```

## 🏗️ Project Structure

```
AI background remover (Hylife)/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── setup.bat           # Windows setup script
│   ├── setup.sh            # Linux/Mac setup script
│   ├── .env.example        # Environment variables template
│   └── .gitignore          # Git ignore rules
├── index.html              # Frontend HTML
├── styles.css              # Frontend styling
├── script.js               # Frontend JavaScript
└── README.md               # This file
```

## 🤖 AI Models

### rembg (U²Net)
- **Purpose**: Background removal
- **Model**: U²Net (U-square Net)
- **Size**: ~176 MB
- **Download**: Automatic on first use
- **Accuracy**: State-of-the-art segmentation
- **Speed**: ~1-2 seconds per image (CPU)

### Real-ESRGAN
- **Purpose**: Image super-resolution
- **Model**: RealESRGAN_x4plus
- **Size**: ~64 MB
- **Download**: Automatic on first use
- **Quality**: 4x upscaling with detail enhancement
- **Speed**: ~2-5 seconds per image (GPU), ~10-30s (CPU)

## ⚡ Performance

### CPU Mode
- Background Removal: 1-3 seconds
- Image Enhancement: 10-30 seconds
- Full Processing: 15-35 seconds

### GPU Mode (CUDA)
- Background Removal: 0.5-1 second
- Image Enhancement: 2-5 seconds
- Full Processing: 3-6 seconds

## 🔧 Configuration

### Backend (.env file)
```env
PORT=8000
HOST=0.0.0.0
DEVICE=cuda  # or cpu
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5500
```

### Frontend (script.js)
```javascript
const CONFIG = {
    API_BASE_URL: 'http://localhost:8000/api'
};
```

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check logs
python main.py  # Look for error messages
```

### CUDA/GPU issues
```bash
# Check if CUDA is available
python -c "import torch; print(torch.cuda.is_available())"

# Install CPU-only PyTorch
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### Frontend not connecting
1. Check backend is running: http://localhost:8000
2. Check CORS settings in `main.py`
3. Check browser console for errors
4. Try using 127.0.0.1 instead of localhost

### Model download fails
- Models download automatically on first use
- Requires internet connection
- Downloads to: `~/.u2net/` and `~/.cache/`
- Manual download: Check Real-ESRGAN GitHub releases

## 📝 API Documentation

FastAPI provides automatic interactive documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎨 Use Cases

- E-commerce product images
- Furniture catalogs
- Social media content
- Presentation materials
- Marketing assets
- Photo editing workflows

## 🚀 Deployment

### Docker (Coming Soon)
```dockerfile
# Dockerfile example
FROM python:3.10
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["python", "main.py"]
```

### Cloud Deployment
- **Heroku**: Use `Procfile` with uvicorn
- **AWS EC2**: Install dependencies and run
- **Google Cloud Run**: Containerize and deploy
- **Railway**: Direct deployment from GitHub

## 📄 License

This project is open source and available for personal and commercial use.

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation
3. Check backend logs
4. Open an issue on GitHub

## 🙏 Acknowledgments

- **rembg**: Daniel Gatis
- **Real-ESRGAN**: Xintao Wang et al.
- **U²Net**: Xuebin Qin et al.
- **FastAPI**: Sebastián Ramírez

---

**Made with ❤️ | Powered by AI | © 2025 Hylife**
