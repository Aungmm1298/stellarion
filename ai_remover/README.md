# AI Background Remover - Hylife

A professional AI-powered background remover for furniture and product images with comprehensive advanced image processing features including histogram processing, spatial/frequency domain filtering, edge detection, segmentation, and morphological operations.

## 🚀 Features

### Core AI Features
- **🎯 Advanced Background Removal**: Powered by U²Net deep learning model with alpha matting
- **✨ Real-ESRGAN Enhancement**: 2x resolution upscaling with professional quality
- **🔍 Edge Refinement**: AI-based edge smoothing and anti-aliasing
- **✂️ Auto-Crop**: Intelligent subject detection and cropping
- **🎨 Background Replacement**: Presets (transparent, white, black, gray) + custom colors
- **📦 Batch Processing**: Process up to 10 images simultaneously
- **⚡ Real-time Preview**: Instant results with compare mode
- **💾 One-Click Download**: Save as optimized PNG or JPEG

### 🆕 Advanced Image Processing Features

#### 📊 Histogram Processing
- **Histogram Equalization**: Global, Adaptive, and CLAHE methods
- **Brightness & Contrast**: Precise adjustments with real-time preview
- **Gamma Correction**: Non-linear brightness adjustment
- **Gray-level Transformations**: Professional color grading tools

#### 🔲 Spatial Filtering
**Smoothing Filters (Noise Reduction):**
- Mean Filter - Uniform noise reduction
- Median Filter - Salt-and-pepper noise removal
- Gaussian Filter - Smooth noise reduction
- Bilateral Filter - Edge-preserving smoothing

**Sharpening Filters (Edge Enhancement):**
- Laplacian Sharpening - Edge enhancement
- Unsharp Mask - Professional sharpening
- High-Pass Filter - Detail enhancement

#### 🌊 Frequency Domain Filtering
- **Low-Pass Filter**: Remove high-frequency noise
- **High-Pass Filter**: Edge enhancement and detail extraction
- **Band-Pass Filter**: Selective frequency range filtering
- **Butterworth Filter**: Smooth frequency response filtering

#### 🔍 Edge Detection
- **Sobel Operator**: Fast gradient-based edge detection
- **Prewitt Operator**: Horizontal and vertical edge detection
- **Canny Edge Detector**: Multi-stage optimal edge detection
- **Laplacian Operator**: Second derivative edge detection
- **Compare All Methods**: Side-by-side comparison of all edge detectors

#### 🎯 Image Segmentation
- **Otsu's Threshold**: Automatic threshold calculation
- **Adaptive Threshold**: Local thresholding for varying lighting
- **K-Means Clustering**: Color-based segmentation (2-10 clusters)
- **Color-Based Segmentation**: RGB/HSV color space segmentation
- **Watershed Algorithm**: Region-based object separation

#### 🔷 Morphological Operations
- **Dilation**: Expand bright regions
- **Erosion**: Shrink bright regions
- **Opening**: Remove small objects (noise removal)
- **Closing**: Fill small holes (gap filling)
- **Morphological Gradient**: Extract object boundaries
- **Top-Hat Transform**: Extract bright objects on dark background
- **Black-Hat Transform**: Extract dark objects on bright background

### User Experience
- **Drag & Drop Upload**: Easy image upload with multi-file support
- **Advanced Processing Panel**: Collapsible panel with organized feature sections
- **Parameter Sliders**: Real-time parameter adjustment with visual feedback
- **Compare Mode**: Toggle between original and processed images
- **Reset Options**: Reset to original or processed image
- **Keyboard Shortcuts**: ESC (back), SPACE (compare), D (download)
- **Responsive Design**: Works perfectly on desktop and mobile
- **Clean UI**: Modern, professional interface with gradient styling
- **Processing Stats**: Real-time performance metrics

## 📋 Requirements

### Frontend
- Modern web browser (Chrome, Firefox, Safari, Edge)
- JavaScript enabled

### Backend (Required for AI Features)
- Python 3.8+
- CUDA-capable GPU (optional, for faster processing)
- 8GB RAM minimum (16GB recommended)
- 2GB disk space for models

### Python Dependencies
- FastAPI
- OpenCV (cv2)
- NumPy
- SciPy
- Pillow (PIL)
- rembg (U²Net)
- Real-ESRGAN (optional)

## 🔧 Setup Instructions

### Quick Start

1. **Install Backend Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Download Models** (if not included)
   - U²Net model: Auto-downloads on first run
   - Real-ESRGAN model: [Download here](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth)
   - Place `RealESRGAN_x2plus.pth` in `backend/models/` folder

3. **Start Backend Server**
   ```bash
   # Windows
   cd backend
   START.bat
   
   # Or manually
   python -m uvicorn api:app --host 0.0.0.0 --port 8000
   ```

4. **Open Frontend**
   - Double-click `index.html`
   - Or use Live Server in VS Code
   - Or run: `python -m http.server 8080`

### Backend Setup (Detailed)

See `backend/SETUP_INSTRUCTIONS.md` for detailed installation guide including:
- Virtual environment setup
- GPU acceleration configuration
- Model installation
- Troubleshooting

## 💡 How to Use

### Single Image Processing

1. **Upload**: Click "Choose Image(s)" or drag & drop
2. **Automatic Processing**: Background removal starts immediately
3. **AI Features**: 
   - ✅ Edge Refinement (enabled by default)
   - ✅ Auto-Crop Subject (optional)
4. **Compare**: Toggle between original and processed
5. **Enhance**: Click "Enhance Quality" for 2x resolution (optional)
6. **Background**: Choose preset or custom color
7. **Download**: Save as PNG or JPEG

### Batch Processing

1. **Select Multiple Images**: Choose 2-10 images
2. **Automatic Processing**: All images processed in parallel
3. **Review Results**: View individual previews
4. **Download**: Download individually or all at once

### AI Features Panel

**Auto-Crop Subject**: ✅ Recommended for most images
- Removes excess transparent space
- Smaller file sizes
- Better composition

**Edge Refinement**: ✅ Enabled by default
- Smooths rough edges
- Professional quality cutouts
- 5 strength levels available

**Background Options**:
- 🔲 Transparent (default)
- ⚪ White
- ⚫ Black  
- 🔳 Light Gray
- 🎨 Custom Color

### Enhancement (Real-ESRGAN)

Click "✨ Enhance Quality" to:
- 2x resolution upscaling
- Improve texture and details
- Professional print quality
- Note: Takes 5-12 seconds

## 🎯 Use Cases

- **E-commerce**: Product images with white backgrounds
- **Furniture Catalogs**: Professional, consistent presentations
- **Social Media**: Eye-catching visuals with custom backgrounds
- **Marketing Materials**: Print-quality enhanced images
- **Website Assets**: Optimized transparent PNGs

## 🤖 How It Works

This application uses state-of-the-art AI models:

### 1. **U²Net (Background Removal)**
- Deep learning model for salient object detection
- Trained on 10,000+ images
- Industry-leading accuracy
- Alpha matting for smooth edges

### 2. **Real-ESRGAN (Enhancement)**
- Generative Adversarial Network (GAN)
- 2x super-resolution upscaling
- Texture and detail restoration
- Professional print quality

### 3. **Edge Refinement Pipeline**
- Bilateral filtering (edge preservation)
- Morphological operations (gap closing)
- Gaussian smoothing (natural transitions)
- Multi-level strength control

### Architecture
```
Frontend (HTML/CSS/JS) 
    ↓
FastAPI Backend
    ↓
AI Models (U²Net + Real-ESRGAN)
    ↓
Image Processing (PIL + OpenCV)
    ↓
Optimized PNG/JPEG Output
```

## 🔑 Keyboard Shortcuts

- `ESC`: Return to upload screen
- `SPACE`: Toggle compare mode (original vs processed)
- `D`: Download current image

## 📱 Browser Support

- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## 🛠️ Technical Stack

### Frontend
- **Languages**: HTML5, CSS3, Vanilla JavaScript
- **Canvas API**: Image manipulation and display
- **File API**: Drag & drop and multi-file handling
- **Fetch API**: Backend communication

### Backend
- **Framework**: FastAPI (Python)
- **AI Models**: U²Net (rembg), Real-ESRGAN
- **Image Processing**: PIL (Pillow), OpenCV, NumPy
- **Deep Learning**: PyTorch, TorchVision
- **Server**: Uvicorn ASGI server

## 📝 File Structure

```
AI background remover (Hylife)/
├── index.html                      # Main frontend HTML
├── styles.css                      # Styling and layout
├── script.js                       # Core frontend JavaScript
├── script-advanced.js              # Advanced image processing features
├── README.md                       # This file
├── ADVANCED_FEATURES_GUIDE.md      # Comprehensive features guide
├── QUICK_REFERENCE.md              # Quick parameter reference
├── FEATURES.md                     # Core features documentation
├── test_api_endpoints.py           # API test suite
├── test_advanced_features.py       # Advanced features tests
├── backend/
│   ├── api.py                      # FastAPI backend with all endpoints
│   ├── image_processing.py         # Advanced processing algorithms
│   ├── requirements.txt            # Python dependencies
│   ├── SETUP_INSTRUCTIONS.md       # Setup guide
│   ├── START.bat                   # Windows startup script
│   ├── u2net.onnx                  # U²Net model (auto-downloaded)
│   └── models/
│       └── RealESRGAN_x2plus.pth   # Enhancement model
└── START.bat                       # Quick start script
```

## 📚 Documentation

- **README.md** (this file): Quick start and overview
- **ADVANCED_FEATURES_GUIDE.md**: Comprehensive guide to all image processing features
- **QUICK_REFERENCE.md**: Quick reference for parameters and common tasks
- **FEATURES.md**: Core AI features and usage guide
- **backend/SETUP_INSTRUCTIONS.md**: Backend installation guide
- **test_api_endpoints.py**: API test suite for advanced features

## 📡 API Endpoints

### Core Features
- `GET /` - Health check and service info
- `GET /api/status` - Check backend status and available features
- `POST /api/remove-background` - Remove background with edge refinement
- `POST /api/enhance-image` - Enhance image quality (2x resolution)
- `POST /api/process-advanced` - Advanced processing with all features
- `POST /api/batch-process` - Batch process up to 10 images

### 🆕 Histogram Processing
- `POST /api/histogram-equalization` - Apply histogram equalization (global/adaptive/CLAHE)
- `POST /api/adjust-brightness-contrast` - Adjust brightness, contrast, and gamma

### 🆕 Spatial Filtering
- `POST /api/spatial-filter` - Apply spatial domain filters (mean, median, gaussian, bilateral, laplacian, unsharp, highpass)

### 🆕 Frequency Domain
- `POST /api/frequency-filter` - Apply frequency domain filters using Fourier Transform (lowpass, highpass, bandpass, butterworth)

### 🆕 Edge Detection
- `POST /api/edge-detection` - Detect edges using various operators (sobel, prewitt, canny, laplacian)
- `POST /api/compare-edge-detectors` - Compare all edge detection methods side-by-side

### 🆕 Segmentation
- `POST /api/segment-threshold` - Threshold-based segmentation (Otsu's, adaptive)
- `POST /api/segment-color` - Color-based segmentation in RGB/HSV
- `POST /api/segment-kmeans` - K-means clustering segmentation
- `POST /api/segment-watershed` - Watershed algorithm segmentation

### 🆕 Morphological Operations
- `POST /api/morphology` - Apply morphological operations (dilate, erode, opening, closing, gradient, tophat, blackhat)

**Full API Documentation**: http://localhost:8000/docs (Interactive Swagger UI)

## 🧪 Testing

Test all advanced features with the included test suite:

```bash
# Test all API endpoints
python test_api_endpoints.py

# Test specific features
python test_advanced_features.py
```

The test suite verifies:
- ✓ API connectivity and status
- ✓ All histogram processing endpoints
- ✓ Spatial and frequency domain filtering
- ✓ Edge detection (all methods)
- ✓ Segmentation algorithms
- ✓ Morphological operations

## 🔒 Privacy & Security

- **Local Processing**: All AI processing on your server
- **No Cloud Upload**: Images never sent to external services
- **No Tracking**: Zero analytics or data collection
- **Complete Privacy**: Perfect for sensitive/proprietary content
- **CORS Enabled**: Secure cross-origin requests

## ⚡ Performance Tips

### For Best Results
1. **Image Quality**: Use high-resolution originals (1000-3000px)
2. **File Size**: Keep under 10MB per image
3. **Subject Clarity**: Good lighting and clear separation
4. **GPU Acceleration**: Enable CUDA for 3-5x faster processing

### Optimization
- ✅ Enable edge refinement (default)
- ✅ Use auto-crop to reduce file size (30-60% smaller)
- ✅ Batch process similar images together
- ⚠️ Use enhancement only when needed (doubles processing time)

## 🤝 Support

### Troubleshooting

**Backend won't start:**
- Check Python version (3.8+)
- Install dependencies: `pip install -r requirements.txt`
- Check port 8000 is available
- See `backend/SETUP_INSTRUCTIONS.md`

**Processing fails:**
- Ensure backend is running (http://localhost:8000)
- Check image format (PNG, JPG, JPEG)
- Verify file size (<10MB)
- Check browser console for errors

**Enhancement not available:**
- Download RealESRGAN_x2plus.pth model
- Place in `backend/models/` folder
- Restart backend server

**Slow processing:**
- Enable GPU/CUDA acceleration
- Reduce image size before upload
- Close other applications
- Use batch processing for multiple images

## 📄 License

This project is open source and available for personal and commercial use.

---

**Made with ❤️ by Hylife | Powered by AI Technology**

##  API Endpoints

### Backend API (http://localhost:8000)

- `GET /api/status` - Check backend status and features
- `POST /api/remove-background` - Remove background with edge refinement
- `POST /api/enhance-image` - Enhance image quality (2x resolution)
- `POST /api/process-advanced` - Advanced processing with all features
- `POST /api/batch-process` - Batch process multiple images

See `FEATURES.md` for detailed API documentation.

##  Advanced Usage

For advanced features and detailed guides, see **FEATURES.md**

##  Roadmap

###  Completed
- [x] Advanced background removal (U²Net)
- [x] Edge refinement with multiple strength levels
- [x] Auto-crop functionality
- [x] Real-ESRGAN enhancement (2x upscaling)
- [x] Background replacement (presets + custom)
- [x] Batch processing (up to 10 images)
- [x] **Histogram processing** (equalization, brightness, contrast, gamma)
- [x] **Spatial filtering** (mean, median, gaussian, bilateral, laplacian, unsharp, highpass)
- [x] **Frequency domain filtering** (lowpass, highpass, bandpass, butterworth)
- [x] **Edge detection** (sobel, prewitt, canny, laplacian) with comparison tool
- [x] **Image segmentation** (Otsu, adaptive, K-means, color-based, watershed)
- [x] **Morphological operations** (dilate, erode, opening, closing, gradient, tophat, blackhat)

###  Coming Soon
- [ ] Shadow generation and object lighting
- [ ] Background blur with depth estimation
- [ ] Perspective correction and image warping
- [ ] Advanced color grading and LUT application
- [ ] Smart object selection and masking
- [ ] Region growing with interactive seed selection

---

## 🎓 Learning Resources

### Understanding the Algorithms

**Histogram Processing:**
- Improves image contrast and brightness distribution
- CLAHE is best for preventing noise amplification
- Essential preprocessing step for many algorithms

**Spatial Filtering:**
- Operates directly on image pixels
- Smoothing reduces noise, sharpening enhances edges
- Bilateral filter preserves edges while smoothing

**Frequency Domain:**
- Works in Fourier space (frequency components)
- Low frequencies = smooth areas, high frequencies = edges
- Ideal for specific frequency range manipulation

**Edge Detection:**
- Canny is the gold standard (optimal edge detection)
- Uses gradient magnitude and hysteresis thresholding
- Critical for object detection and segmentation

**Segmentation:**
- Divides image into meaningful regions
- Otsu's method automatically finds best threshold
- K-means groups pixels by color similarity

**Morphology:**
- Mathematical operations on image shapes
- Opening removes noise, closing fills holes
- Essential for binary image cleanup

For detailed explanations and examples, see **ADVANCED_FEATURES_GUIDE.md**

---

** Links:**
- Backend API: http://localhost:8000
- API Interactive Docs (Swagger): http://localhost:8000/docs
- API JSON Schema (ReDoc): http://localhost:8000/redoc

 **Documentation:**
- `ADVANCED_FEATURES_GUIDE.md` - Complete feature documentation
- `QUICK_REFERENCE.md` - Quick parameter reference guide
- `FEATURES.md` - Core features guide

 **Need Help?** 
1. Check `QUICK_REFERENCE.md` for quick solutions
2. See `ADVANCED_FEATURES_GUIDE.md` for detailed documentation
3. Run `python test_api_endpoints.py` to test your setup
