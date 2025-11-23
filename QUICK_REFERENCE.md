# 🎨 Advanced Image Processing - Quick Reference

## 📊 Histogram Processing

| Feature | Purpose | When to Use |
|---------|---------|-------------|
| **Global Equalization** | Enhance contrast uniformly | General purpose contrast enhancement |
| **Adaptive Equalization** | Local contrast enhancement | Images with varying lighting |
| **CLAHE** | Noise-limited contrast | Best for most images, prevents over-amplification |
| **Brightness** (-100 to +100) | Make lighter/darker | Adjust overall brightness |
| **Contrast** (0.5 to 3.0) | Increase/decrease difference | Adjust dynamic range |
| **Gamma** (0.1 to 3.0) | Non-linear adjustment | Fine-tune brightness curve |

---

## 🔲 Spatial Filtering

### Smoothing (Noise Reduction)

| Filter | Best For | Edge Preservation |
|--------|----------|-------------------|
| **Mean** | Uniform noise | Low |
| **Median** | Salt-and-pepper noise | Medium |
| **Gaussian** | General smoothing | Low |
| **Bilateral** | Photographic images | High ⭐ |

### Sharpening (Edge Enhancement)

| Filter | Best For | Strength |
|--------|----------|----------|
| **Laplacian** | Text, documents | High |
| **Unsharp Mask** | Photography | Adjustable ⭐ |
| **High-Pass** | Edge emphasis | High |

**Parameters:**
- Kernel Size: 3-15 (larger = stronger effect)
- Sigma: 0.1-5.0 (Gaussian spread)

---

## 🌊 Frequency Domain Filtering

| Filter Type | Effect | Use Case |
|-------------|--------|----------|
| **Low-Pass** | Smoothing, blur | Noise removal |
| **High-Pass** | Edge enhancement | Detail extraction |
| **Band-Pass** | Specific frequencies | Texture analysis |
| **Butterworth** | Smooth cutoff | Professional filtering |

**Cutoff Frequency:**
- Lower = more smoothing/less detail
- Higher = less smoothing/more detail

---

## 🔍 Edge Detection

| Method | Speed | Quality | Best For |
|--------|-------|---------|----------|
| **Sobel** | Fast | Good | Real-time applications |
| **Prewitt** | Fast | Good | Simple edge detection |
| **Canny** | Medium | Excellent ⭐ | Best overall quality |
| **Laplacian** | Fast | Fair | Quick detection |

**Canny Parameters:**
- Lower Threshold (50-100): Weak edge detection
- Upper Threshold (150-200): Strong edge detection
- Gap between thresholds: Controls edge connectivity

---

## 🎯 Image Segmentation

| Method | Speed | Parameters | Best For |
|--------|-------|-----------|----------|
| **Otsu's Threshold** | Fast | None (automatic) | Bimodal histograms ⭐ |
| **Adaptive Threshold** | Medium | Block size, C | Varying lighting |
| **K-Means** | Slow | k (clusters) | Color segmentation |
| **Color-Based** | Fast | Color ranges | Specific color isolation |
| **Watershed** | Medium | None | Touching object separation |

**K-Means Cluster Guide:**
- k=2: Binary segmentation
- k=3-5: General purpose ⭐
- k=6-10: Complex scenes

---

## 🔷 Morphological Operations

| Operation | Effect | Common Use |
|-----------|--------|------------|
| **Dilate** | Expands white regions | Fill gaps, connect objects |
| **Erode** | Shrinks white regions | Remove noise, separate objects |
| **Opening** | Remove small objects | Noise removal ⭐ |
| **Closing** | Fill small holes | Gap filling ⭐ |
| **Gradient** | Extract boundaries | Edge detection |
| **Top-Hat** | Bright on dark | Feature extraction |
| **Black-Hat** | Dark on bright | Shadow detection |

**Kernel Size Guide:**
- 3-5: Fine details
- 7-11: Medium features
- 13-21: Large features

---

## 🎯 Common Processing Pipelines

### **Enhance Low-Quality Image**
1. CLAHE Histogram Equalization
2. Bilateral Filter (noise reduction)
3. Unsharp Mask (sharpening)

### **Document Cleanup**
1. Otsu's Threshold
2. Opening (remove noise)
3. Closing (fill holes)

### **Object Detection Prep**
1. Gaussian Smoothing
2. Canny Edge Detection
3. Morphological Closing

### **Color Object Extraction**
1. Color-Based Segmentation (HSV)
2. Morphological Opening
3. Morphological Closing

### **Edge Enhancement**
1. Gaussian Smoothing (optional)
2. Histogram Equalization
3. High-Pass or Laplacian Filter

---

## ⚡ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `ESC` | Back to upload |
| `SPACE` | Toggle compare |
| `D` | Download image |

---

## 🔧 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Image too noisy | Use Median or Bilateral filter first |
| Too many edges detected | Increase Canny lower threshold |
| Segmentation not working | Try CLAHE before segmentation |
| Morphology too strong | Reduce kernel size or iterations |
| Frequency filter unclear | Adjust cutoff frequency |

---

## 📊 Parameter Quick Reference

### **Brightness & Contrast**
```
Brightness: -100 (darker) ←→ +100 (brighter)
Contrast:   0.5 (low)     ←→ 3.0 (high)
Gamma:      0.1 (bright)  ←→ 3.0 (dark)
```

### **Spatial Filters**
```
Kernel Size: 3 (subtle) ←→ 15 (strong)
Sigma:       0.1 (tight) ←→ 5.0 (wide)
```

### **Edge Detection**
```
Sobel/Prewitt: Kernel 3, 5, or 7
Canny Lower:   50 (more edges) ←→ 150 (fewer)
Canny Upper:   100 (loose) ←→ 300 (strict)
```

### **Segmentation**
```
K-Means: 2 (simple) ←→ 10 (complex)
HSV Hue: 0 (red) → 60 (yellow) → 120 (green) → 180 (red)
```

### **Morphology**
```
Kernel:     3 (fine) ←→ 21 (coarse)
Iterations: 1 (subtle) ←→ 5 (strong)
```

---

## 💡 Pro Tips

1. **Always save your original**: Use Reset buttons to recover
2. **Process incrementally**: Apply one operation at a time
3. **Preview before downloading**: Check results carefully
4. **Use CLAHE first**: Often improves subsequent operations
5. **Bilateral for photos**: Best quality for photographic content
6. **Median for noise**: Excellent for salt-and-pepper noise
7. **Canny for edges**: Most reliable edge detection
8. **Opening for cleanup**: Removes noise without changing size
9. **Closing for gaps**: Fills holes without changing size
10. **Compare edge methods**: Use comparison tool to choose best

---

## 🎯 Feature Selection Guide

**Choose by Goal:**

| Goal | Recommended Feature |
|------|-------------------|
| Improve contrast | CLAHE Histogram Equalization |
| Remove noise | Bilateral or Median Filter |
| Sharpen image | Unsharp Mask |
| Find edges | Canny Edge Detection |
| Separate objects | Otsu Threshold + Morphology |
| Extract color | Color-Based Segmentation |
| Clean binary image | Opening + Closing |
| Enhance details | High-Pass Filter |
| Smooth texture | Low-Pass Frequency Filter |
| Object boundaries | Morphological Gradient |

---

## 📈 Performance Tips

- **Fastest**: Mean Filter, Otsu Threshold, Sobel
- **Best Quality**: CLAHE, Bilateral, Canny, K-Means
- **Balanced**: Gaussian, Median, Prewitt, Adaptive Threshold

---

**Quick Start**: Upload image → Expand Advanced Processing → Choose operation → Adjust parameters → Apply → Download!

---

**For detailed documentation, see:** `ADVANCED_FEATURES_GUIDE.md`
