# 🔬 Advanced Image Processing Features

## Overview
Comprehensive image processing toolkit with professional-grade algorithms for enhancement, filtering, edge detection, and segmentation.

---

## 📊 Histogram Processing

### 1. Histogram Equalization
Enhance image contrast by redistributing pixel intensities.

**Endpoint:** `POST /api/histogram-equalization`

**Methods:**
- **Global**: Standard histogram equalization
- **Adaptive**: Locally adaptive equalization
- **CLAHE**: Contrast Limited Adaptive Histogram Equalization (best quality)

**Parameters:**
```json
{
  "file": "image file",
  "method": "clahe"  // 'global', 'adaptive', or 'clahe'
}
```

**Use Cases:**
- Improve low-contrast images
- Enhance details in dark/bright regions
- Prepare images for analysis

**Example:**
```python
# Using cURL
curl -X POST http://localhost:8000/api/histogram-equalization \
  -F "file=@image.jpg" \
  -F "method=clahe" \
  -o enhanced.png
```

---

### 2. Brightness & Contrast Adjustment
Fine-tune image appearance with gray-level transformations.

**Endpoint:** `POST /api/adjust-brightness-contrast`

**Parameters:**
```json
{
  "file": "image file",
  "brightness": 0,      // -100 to 100
  "contrast": 1.0,      // 0.5 to 3.0
  "gamma": 1.0          // 0.1 to 3.0 (< 1 brightens, > 1 darkens)
}
```

**Adjustments:**
- **Brightness**: Linear shift of pixel values
- **Contrast**: Multiplicative scaling
- **Gamma**: Non-linear power-law transformation

**Use Cases:**
- Correct underexposed/overexposed images
- Adjust for display calibration
- Artistic tone adjustments

---

## 🔧 Spatial Filtering

### Smoothing Filters (Noise Reduction)

**Endpoint:** `POST /api/spatial-filter`

#### 1. Mean Filter
Fast averaging filter for general noise reduction.

```json
{
  "filter_type": "mean",
  "kernel_size": 5
}
```

#### 2. Median Filter
Best for salt-and-pepper noise, preserves edges better than mean.

```json
{
  "filter_type": "median",
  "kernel_size": 5
}
```

#### 3. Gaussian Filter
Smooth, weighted averaging with bell-curve kernel.

```json
{
  "filter_type": "gaussian",
  "kernel_size": 5,
  "sigma": 1.0
}
```

#### 4. Bilateral Filter
**Edge-preserving smoothing** - smooths noise while keeping edges sharp.

```json
{
  "filter_type": "bilateral",
  "kernel_size": 9
}
```

**Best for:** Photo retouching, detail preservation

---

### Sharpening Filters (Edge Enhancement)

#### 1. Laplacian Sharpening
Detect and enhance edges using second derivative.

```json
{
  "filter_type": "laplacian",
  "kernel_size": 3
}
```

#### 2. Unsharp Mask
**Professional sharpening** - subtract blurred version from original.

```json
{
  "filter_type": "unsharp",
  "kernel_size": 5,
  "sigma": 1.0
}
```

**Best for:** Print preparation, detail enhancement

#### 3. High-Pass Filter
Remove low frequencies, keeping only edges and details.

```json
{
  "filter_type": "highpass",
  "kernel_size": 3
}
```

---

## 🌊 Frequency Domain Filtering

Apply filters in Fourier space for advanced frequency manipulation.

**Endpoint:** `POST /api/frequency-filter`

### 1. Low-Pass Filter (Blur/Smooth)
Remove high-frequency noise and details.

```json
{
  "filter_type": "lowpass",
  "cutoff": 30.0  // Lower = more blur
}
```

**Use Cases:**
- Noise reduction
- Anti-aliasing
- Creating smooth backgrounds

### 2. High-Pass Filter (Sharpen/Edges)
Remove low frequencies, enhance edges and fine details.

```json
{
  "filter_type": "highpass",
  "cutoff": 30.0  // Higher = more edge detail
}
```

**Use Cases:**
- Edge detection
- Texture analysis
- Detail enhancement

### 3. Band-Pass Filter
Keep only frequencies within a specific range.

```json
{
  "filter_type": "bandpass",
  "low_cutoff": 20.0,
  "high_cutoff": 60.0
}
```

**Use Cases:**
- Isolate specific patterns
- Texture extraction
- Periodic noise removal

### 4. Butterworth Low-Pass Filter
Smooth, gradual frequency rolloff (no ringing artifacts).

```json
{
  "filter_type": "butterworth_lowpass",
  "cutoff": 30.0,
  "order": 2  // Higher order = sharper cutoff
}
```

**Best for:** High-quality smoothing without artifacts

---

## 🔍 Edge Detection

Detect and extract object boundaries and features.

**Endpoint:** `POST /api/edge-detection`

### 1. Sobel Operator
Gradient-based edge detection with directional sensitivity.

```json
{
  "method": "sobel",
  "kernel_size": 3  // 1, 3, 5, or 7
}
```

**Characteristics:**
- Fast computation
- Good noise tolerance
- Directional gradient information

### 2. Prewitt Operator
Similar to Sobel but simpler kernels.

```json
{
  "method": "prewitt"
}
```

**Characteristics:**
- Simpler than Sobel
- Good for learning/comparison
- Slightly less accurate

### 3. Canny Edge Detector
**Industry standard** - multi-stage optimal edge detection.

```json
{
  "method": "canny",
  "threshold1": 50,   // Lower threshold for edge linking
  "threshold2": 150,  // Upper threshold for strong edges
  "kernel_size": 3
}
```

**Characteristics:**
- **Best quality** edge detection
- Thin, connected edges
- Good noise rejection
- Multi-stage algorithm

**Stages:**
1. Noise reduction (Gaussian)
2. Gradient calculation
3. Non-maximum suppression
4. Double thresholding
5. Edge tracking by hysteresis

### 4. Laplacian Operator
Second-derivative edge detection.

```json
{
  "method": "laplacian",
  "kernel_size": 3
}
```

**Characteristics:**
- Isotropic (rotation-invariant)
- Detects edges in all directions
- More sensitive to noise

---

### Edge Detector Comparison

**Endpoint:** `POST /api/compare-edge-detectors`

Returns all four methods for side-by-side comparison.

```json
{
  "results": {
    "sobel": "data:image/png;base64,...",
    "prewitt": "data:image/png;base64,...",
    "canny": "data:image/png;base64,...",
    "laplacian": "data:image/png;base64,..."
  }
}
```

**Choosing the Right Detector:**
- **Canny**: Best overall, production use
- **Sobel**: Fast, good for real-time
- **Prewitt**: Educational/comparison
- **Laplacian**: Special applications, fine details

---

## 🎨 Image Segmentation

Partition images into meaningful regions.

### 1. Otsu's Thresholding
**Automatic threshold selection** - finds optimal separation between foreground/background.

**Endpoint:** `POST /api/segment-threshold`

```json
{
  "method": "otsu"
}
```

**Characteristics:**
- Fully automatic
- Works well for bimodal histograms
- Fast and reliable
- Returns optimal threshold value

**Use Cases:**
- Document scanning
- Binary object extraction
- Automatic foreground/background separation

---

### 2. Adaptive Thresholding
Local thresholding for varying illumination.

```json
{
  "method": "adaptive",
  "block_size": 11,  // Neighborhood size (odd number)
  "C": 2             // Constant subtracted from mean
}
```

**Characteristics:**
- Handles uneven lighting
- Local threshold calculation
- Better for complex scenes

**Use Cases:**
- Document imaging
- Uneven illumination
- Text recognition

---

### 3. Color-Based Segmentation
Segment by color range in RGB or HSV space.

**Endpoint:** `POST /api/segment-color`

```json
{
  "color_space": "hsv",
  "lower_h": 0,
  "lower_s": 50,
  "lower_v": 50,
  "upper_h": 180,
  "upper_s": 255,
  "upper_v": 255
}
```

**Color Spaces:**
- **HSV**: Better for color-based selection (Hue, Saturation, Value)
- **RGB**: Direct color channel values

**HSV Ranges:**
- Hue: 0-180 (color)
- Saturation: 0-255 (color intensity)
- Value: 0-255 (brightness)

**Use Cases:**
- Isolate colored objects
- Green screen removal
- Color-based object tracking
- Skin detection

**Example Ranges:**
```
Red: H(0-10, 170-180), S(100-255), V(100-255)
Green: H(40-80), S(100-255), V(100-255)
Blue: H(100-130), S(100-255), V(100-255)
```

---

### 4. K-Means Clustering
Partition image into K color clusters.

**Endpoint:** `POST /api/segment-kmeans`

```json
{
  "k": 3  // Number of clusters (2-10 typical)
}
```

**Characteristics:**
- Unsupervised learning
- Color quantization
- Iterative optimization

**Use Cases:**
- Color compression
- Simplified representation
- Region extraction
- Artistic effects

---

### 5. Watershed Segmentation
Marker-based region growing algorithm.

**Endpoint:** `POST /api/segment-watershed`

**Characteristics:**
- Treats image as topographic surface
- Separates touching objects
- Automatic marker detection

**Use Cases:**
- Separate overlapping objects
- Cell counting
- Complex shape separation

---

## 🔷 Morphological Operations

Shape-based transformations for binary and grayscale images.

**Endpoint:** `POST /api/morphology`

### Basic Operations

#### 1. Dilation
Expand bright regions, fill small holes.

```json
{
  "operation": "dilate",
  "kernel_size": 5,
  "iterations": 1
}
```

**Effects:**
- Enlarges objects
- Fills small gaps
- Connects nearby regions

#### 2. Erosion
Shrink bright regions, remove small noise.

```json
{
  "operation": "erode",
  "kernel_size": 5,
  "iterations": 1
}
```

**Effects:**
- Reduces object size
- Removes small objects
- Separates touching objects

---

### Compound Operations

#### 3. Opening (Erosion → Dilation)
Remove small noise while preserving shape.

```json
{
  "operation": "opening",
  "kernel_size": 5
}
```

**Use Cases:**
- Remove salt noise
- Smooth object boundaries
- Break thin connections

#### 4. Closing (Dilation → Erosion)
Fill small holes while preserving shape.

```json
{
  "operation": "closing",
  "kernel_size": 5
}
```

**Use Cases:**
- Fill pepper noise
- Close small gaps
- Connect nearby objects

---

### Advanced Operations

#### 5. Morphological Gradient
Edge extraction (Dilation - Erosion).

```json
{
  "operation": "gradient",
  "kernel_size": 5
}
```

**Result:** Object boundaries

#### 6. Top-Hat Transform
Extract bright objects on dark background.

```json
{
  "operation": "tophat",
  "kernel_size": 9
}
```

**Use Cases:**
- Enhance bright features
- Text extraction
- Spot detection

#### 7. Black-Hat Transform
Extract dark objects on bright background.

```json
{
  "operation": "blackhat",
  "kernel_size": 9
}
```

**Use Cases:**
- Enhance dark features
- Valley detection
- Shadow extraction

---

## 🎯 Common Workflows

### Workflow 1: Document Enhancement
```
1. Histogram Equalization (CLAHE)
2. Adaptive Thresholding
3. Morphological Opening (remove noise)
4. Morphological Closing (fill text breaks)
```

### Workflow 2: Object Extraction
```
1. Gaussian Filter (noise reduction)
2. Otsu Thresholding (segmentation)
3. Morphological Opening (clean up)
4. Canny Edge Detection (extract boundaries)
```

### Workflow 3: Color-Based Selection
```
1. Convert to HSV
2. Color-Based Segmentation
3. Morphological Closing (fill holes)
4. Bilateral Filter (smooth edges)
```

### Workflow 4: Edge Enhancement
```
1. Bilateral Filter (reduce noise, preserve edges)
2. Unsharp Mask (enhance edges)
3. Canny Edge Detection (extract edges)
4. Morphological Dilation (thicken edges)
```

### Workflow 5: Texture Analysis
```
1. Frequency Domain High-Pass Filter
2. Histogram Equalization
3. Sobel Edge Detection
4. Morphological Gradient
```

---

## 📖 API Usage Examples

### Python Example
```python
import requests

# Histogram equalization
with open('image.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/histogram-equalization',
        files={'file': f},
        data={'method': 'clahe'}
    )
    with open('enhanced.png', 'wb') as out:
        out.write(response.content)

# Edge detection with Canny
with open('image.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/edge-detection',
        files={'file': f},
        data={
            'method': 'canny',
            'threshold1': 50,
            'threshold2': 150
        }
    )
    with open('edges.png', 'wb') as out:
        out.write(response.content)

# Color segmentation (extract red objects)
with open('image.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/segment-color',
        files={'file': f},
        data={
            'color_space': 'hsv',
            'lower_h': 0, 'lower_s': 100, 'lower_v': 100,
            'upper_h': 10, 'upper_s': 255, 'upper_v': 255
        }
    )
    with open('red_mask.png', 'wb') as out:
        out.write(response.content)
```

### JavaScript Example
```javascript
// Edge detector comparison
const formData = new FormData();
formData.append('file', imageFile);

const response = await fetch('http://localhost:8000/api/compare-edge-detectors', {
    method: 'POST',
    body: formData
});

const data = await response.json();
// data.results contains base64 images for each method
document.getElementById('sobel').src = data.results.sobel;
document.getElementById('canny').src = data.results.canny;
```

### cURL Examples
```bash
# Spatial filtering (Gaussian blur)
curl -X POST http://localhost:8000/api/spatial-filter \
  -F "file=@image.jpg" \
  -F "filter_type=gaussian" \
  -F "kernel_size=7" \
  -F "sigma=2.0" \
  -o blurred.png

# Frequency domain high-pass filter
curl -X POST http://localhost:8000/api/frequency-filter \
  -F "file=@image.jpg" \
  -F "filter_type=highpass" \
  -F "cutoff=40.0" \
  -o highpass.png

# K-means segmentation
curl -X POST http://localhost:8000/api/segment-kmeans \
  -F "file=@image.jpg" \
  -F "k=5" \
  -o segmented.png

# Morphological operations
curl -X POST http://localhost:8000/api/morphology \
  -F "file=@binary.png" \
  -F "operation=opening" \
  -F "kernel_size=5" \
  -o cleaned.png
```

---

## 🔬 Technical Details

### Algorithms Implemented

**Histogram Processing:**
- Global histogram equalization
- CLAHE (Contrast Limited Adaptive Histogram Equalization)
- Histogram matching/specification
- Gamma correction (power-law transformation)

**Spatial Filtering:**
- Convolution-based filtering
- Mean filter (box filter)
- Median filter (order statistic)
- Gaussian filter (separable convolution)
- Bilateral filter (edge-preserving)
- Laplacian of Gaussian
- Unsharp masking

**Frequency Domain:**
- 2D Fast Fourier Transform (FFT)
- Ideal filters (low-pass, high-pass, band-pass)
- Butterworth filters
- Frequency domain multiplication
- Inverse FFT

**Edge Detection:**
- Sobel operator (3x3, 5x5, 7x7)
- Prewitt operator
- Canny edge detector (multi-stage)
- Laplacian operator
- Gradient magnitude computation

**Segmentation:**
- Otsu's method (optimal thresholding)
- Adaptive thresholding (local)
- Region growing
- Watershed algorithm
- K-means clustering
- Color space conversion (RGB ↔ HSV)

**Morphology:**
- Binary morphology
- Grayscale morphology
- Structuring elements (elliptical)
- Hit-or-miss transform
- Morphological reconstruction

---

## ⚡ Performance Considerations

**Processing Times** (typical 1920x1080 image):
- Histogram operations: 50-200ms
- Spatial filtering: 100-500ms
- Frequency filtering: 200-800ms
- Edge detection: 100-400ms
- Segmentation: 200-1000ms
- Morphology: 50-300ms

**Optimization Tips:**
1. Resize large images before processing
2. Use appropriate kernel sizes (smaller = faster)
3. Batch similar operations
4. Cache frequently used filters
5. Use GPU acceleration when available

---

## 🎓 Learning Resources

### Understanding Parameters

**Kernel Size:**
- Smaller (3x3): Fast, preserves details, less smoothing
- Medium (5x5, 7x7): Balanced
- Larger (9x9+): Slow, more smoothing, may blur details

**Threshold Values:**
- Experiment with your specific images
- Use comparison endpoints to find optimal values
- Consider image histogram when choosing

**Color Space Selection:**
- **RGB**: Direct, intuitive, lighting-dependent
- **HSV**: Better for color selection, illumination-invariant

---

## 🆘 Troubleshooting

### Common Issues

**Poor edge detection results:**
- Try different thresholds (Canny)
- Pre-process with Gaussian blur
- Adjust image contrast first

**Noisy segmentation:**
- Apply morphological opening/closing
- Use adaptive instead of global thresholding
- Increase smoothing filter strength

**Frequency filter artifacts:**
- Use Butterworth instead of ideal filters
- Lower the filter order
- Adjust cutoff frequency

**Slow processing:**
- Reduce image resolution
- Use smaller kernel sizes
- Choose simpler algorithms

---

## 📚 API Reference Summary

| Category | Endpoint | Methods/Operations |
|----------|----------|-------------------|
| Histogram | `/api/histogram-equalization` | global, adaptive, clahe |
| Brightness | `/api/adjust-brightness-contrast` | brightness, contrast, gamma |
| Spatial | `/api/spatial-filter` | mean, median, gaussian, bilateral, laplacian, unsharp, highpass |
| Frequency | `/api/frequency-filter` | lowpass, highpass, bandpass, butterworth |
| Edges | `/api/edge-detection` | sobel, prewitt, canny, laplacian |
| Compare | `/api/compare-edge-detectors` | All edge methods |
| Threshold | `/api/segment-threshold` | otsu, adaptive |
| Color Seg | `/api/segment-color` | RGB/HSV color ranges |
| K-means | `/api/segment-kmeans` | Clustering (k clusters) |
| Watershed | `/api/segment-watershed` | Marker-based segmentation |
| Morphology | `/api/morphology` | dilate, erode, opening, closing, gradient, tophat, blackhat |

---

## 🔮 Future Enhancements

- [ ] Deep learning-based segmentation (U-Net, Mask R-CNN)
- [ ] Super-resolution neural networks
- [ ] Optical flow estimation
- [ ] Feature extraction (SIFT, SURF, ORB)
- [ ] Image stitching and panorama
- [ ] HDR image processing
- [ ] Denoising autoencoders
- [ ] Style transfer

---

**For setup and basic usage, see:** `README.md` and `QUICKSTART.md`

**For AI background removal features, see:** `FEATURES.md`
