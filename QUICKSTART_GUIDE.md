# 🚀 Quick Start Guide - Advanced Image Processing

## ⚡ 3-Step Quick Start

### 1️⃣ Start the Backend Server

**Windows:**
```bash
cd backend
python main.py
```

**Or use the batch file:**
```bash
cd backend
START.bat
```

**Linux/Mac:**
```bash
cd backend
python3 main.py
```

The server will start at: `http://localhost:8000`

### 2️⃣ Open the Frontend

**Option A - Simple:**
- Open `index.html` in your browser

**Option B - Live Server (Recommended):**
- Use VS Code Live Server extension
- Right-click `index.html` → "Open with Live Server"

### 3️⃣ Start Processing

1. Upload an image (drag & drop or click)
2. Background is automatically removed
3. Click "⚙️ Advanced Image Processing" to access all features
4. Adjust parameters and click "Apply"
5. Download your result!

---

## 🎨 Feature Quick Access

### 📊 **Histogram Processing**
**Location:** Advanced Processing → Histogram Processing

**Quick Tasks:**
- Enhance contrast → Select "CLAHE" → Click Apply
- Adjust brightness → Move brightness slider → Click Apply
- Fine-tune gamma → Adjust gamma slider → Click Apply

### 🔲 **Noise Reduction**
**Location:** Advanced Processing → Spatial Filtering

**Quick Tasks:**
- Remove noise → Select "Median Filter" → Apply
- Smooth edges → Select "Bilateral Filter" → Apply
- Quick blur → Select "Gaussian Filter" → Apply

### ✨ **Sharpen Images**
**Location:** Advanced Processing → Spatial Filtering

**Quick Tasks:**
- Professional sharpening → Select "Unsharp Mask" → Apply
- Edge enhancement → Select "Laplacian Sharpening" → Apply
- High detail → Select "High-Pass Filter" → Apply

### 🔍 **Find Edges**
**Location:** Advanced Processing → Edge Detection

**Quick Tasks:**
- Best quality → Select "Canny" → Adjust thresholds → Apply
- Fast detection → Select "Sobel" → Apply
- Compare all methods → Click "Compare All Methods"

### 🎯 **Segment Objects**
**Location:** Advanced Processing → Image Segmentation

**Quick Tasks:**
- Simple separation → Select "Otsu's Threshold" → Apply
- Color isolation → Select "Color-Based" → Adjust hue range → Apply
- Multiple regions → Select "K-Means" → Set clusters → Apply

### 🔷 **Clean Up Images**
**Location:** Advanced Processing → Morphological Operations

**Quick Tasks:**
- Remove noise → Select "Opening" → Apply
- Fill holes → Select "Closing" → Apply
- Extract boundaries → Select "Gradient" → Apply

---

## 🎯 Common Workflows

### **Enhance Low-Quality Photo**
```
1. Upload image
2. Histogram Processing → CLAHE → Apply
3. Spatial Filtering → Bilateral Filter → Apply
4. Spatial Filtering → Unsharp Mask → Apply
5. Download result
```

### **Extract Object Edges**
```
1. Upload image
2. Spatial Filtering → Gaussian Filter (kernel=3) → Apply
3. Edge Detection → Canny → Adjust thresholds → Apply
4. Download result
```

### **Clean Binary Image**
```
1. Upload image
2. Segmentation → Otsu's Threshold → Apply
3. Morphology → Opening (kernel=3) → Apply
4. Morphology → Closing (kernel=5) → Apply
5. Download result
```

### **Isolate Specific Color**
```
1. Upload image
2. Segmentation → Color-Based → Select HSV
3. Adjust hue range sliders
4. Click Apply
5. Download result
```

---

## 🔧 Parameter Guidelines

### **Histogram Processing**
- **CLAHE**: Best for most images
- **Brightness**: 0 = unchanged, +50 = brighter, -50 = darker
- **Contrast**: 1.0 = unchanged, 2.0 = high contrast
- **Gamma**: 1.0 = unchanged, <1.0 = brighter, >1.0 = darker

### **Spatial Filtering**
- **Kernel Size**: 3-5 = subtle, 7-11 = moderate, 13-15 = strong
- **Sigma**: 1.0 = tight, 3.0 = wide spread

### **Edge Detection**
- **Canny Lower**: 50 = more edges, 100 = fewer edges
- **Canny Upper**: 150 = connected edges, 200 = strict edges

### **Segmentation**
- **K-Means k**: 2 = binary, 3-5 = most common, 6-10 = complex
- **Hue**: 0-30 = red, 60 = yellow, 120 = green, 180 = red again

### **Morphology**
- **Kernel Size**: 3-5 = fine detail, 7-11 = medium, 13-21 = large
- **Iterations**: 1 = subtle, 2-3 = moderate, 4-5 = strong

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `ESC` | Return to upload screen |
| `SPACE` | Toggle compare (original ↔ processed) |
| `D` | Download current image |

---

## 🔍 Troubleshooting

### **Backend won't start**
```bash
# Check Python version
python --version  # Should be 3.8+

# Install dependencies
cd backend
pip install -r requirements.txt

# Try starting again
python main.py
```

### **"Backend not available" message**
1. Check if backend is running
2. Visit http://localhost:8000 in browser
3. Should see API status JSON

### **Processing fails**
1. Check file size (<10MB)
2. Check file format (PNG, JPG, JPEG)
3. Try smaller image first
4. Check browser console (F12) for errors

### **Slow processing**
1. Reduce image size before upload
2. Close other applications
3. Use simpler operations first
4. Consider GPU acceleration

---

## 📊 Test Your Installation

Run the test suite to verify everything works:

```bash
# Test all API endpoints
python test_api_endpoints.py
```

You should see:
```
✓ API Status: online
✓ Histogram equalization successful
✓ Spatial filter successful
✓ Edge detection successful
... (all tests pass)

📊 Test Summary
Passed: 9/9
✅ All tests passed!
```

---

## 📚 Learn More

**For detailed documentation:**
- `ADVANCED_FEATURES_GUIDE.md` - Complete feature documentation
- `QUICK_REFERENCE.md` - Parameter reference and tips
- `README.md` - Project overview and setup

**For API details:**
- Visit http://localhost:8000/docs (Interactive Swagger UI)
- Visit http://localhost:8000/redoc (ReDoc documentation)

---

## 💡 Tips for Best Results

1. **Start Simple**: Try basic operations before advanced ones
2. **Process Incrementally**: Apply one operation at a time
3. **Use Reset**: Reset to Original or Processed if you go wrong
4. **Experiment**: Try different parameters to see effects
5. **Save Often**: Download intermediate results
6. **Compare Results**: Use Compare button to see changes
7. **Learn by Doing**: Try the example workflows above

---

## 🎯 Feature Recommendations by Use Case

### **Photography Enhancement**
1. CLAHE histogram equalization
2. Bilateral filter (noise reduction)
3. Unsharp mask (sharpening)

### **Document Processing**
1. Otsu's threshold
2. Morphological opening (noise removal)
3. Morphological closing (gap filling)

### **Object Detection Prep**
1. Gaussian smoothing
2. Canny edge detection
3. Morphological operations for cleanup

### **Artistic Effects**
1. High-pass filter (edge emphasis)
2. Frequency domain filtering
3. K-means segmentation (posterize)

### **Quality Control / Inspection**
1. Histogram equalization
2. Edge detection (find defects)
3. Segmentation (isolate areas)

---

## 🎓 Next Steps

Once comfortable with basic operations:

1. **Try Batch Processing**: Upload multiple images at once
2. **Create Pipelines**: Chain multiple operations together
3. **Compare Methods**: Use edge detector comparison
4. **Explore Frequency Domain**: Try FFT-based filtering
5. **Advanced Segmentation**: Use watershed or K-means

---

## 🚀 Ready to Go!

Your advanced image processing system is fully set up and ready to use!

**Start Processing Now:**
1. ✓ Backend running at http://localhost:8000
2. ✓ Open index.html in browser
3. ✓ Upload image
4. ✓ Click "Advanced Image Processing"
5. ✓ Choose feature and apply!

**Have fun processing images! 🎨**

---

**Version**: 2.0.0
**Last Updated**: November 23, 2025
**Status**: Production Ready ✅
