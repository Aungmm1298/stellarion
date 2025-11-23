// Advanced Image Processing Functions
// Extends the main script.js with histogram, spatial filtering, frequency domain, edge detection, segmentation, and morphology features

// Advanced processing DOM elements
const toggleAdvancedBtn = document.getElementById('toggleAdvancedBtn');
const advancedContent = document.getElementById('advancedContent');

// Histogram Processing
const histogramMethod = document.getElementById('histogramMethod');
const applyHistogramBtn = document.getElementById('applyHistogramBtn');
const brightnessSlider = document.getElementById('brightnessSlider');
const contrastSlider = document.getElementById('contrastSlider');
const gammaSlider = document.getElementById('gammaSlider');
const brightnessValue = document.getElementById('brightnessValue');
const contrastValue = document.getElementById('contrastValue');
const gammaValue = document.getElementById('gammaValue');
const applyBrightnessContrastBtn = document.getElementById('applyBrightnessContrastBtn');

// Spatial Filtering
const spatialFilterType = document.getElementById('spatialFilterType');
const kernelSizeSlider = document.getElementById('kernelSizeSlider');
const sigmaSlider = document.getElementById('sigmaSlider');
const kernelSizeValue = document.getElementById('kernelSizeValue');
const sigmaValue = document.getElementById('sigmaValue');
const applySpatialFilterBtn = document.getElementById('applySpatialFilterBtn');

// Frequency Domain Filtering
const frequencyFilterType = document.getElementById('frequencyFilterType');
const cutoffSlider = document.getElementById('cutoffSlider');
const cutoffValue = document.getElementById('cutoffValue');
const bandpassControls = document.getElementById('bandpassControls');
const lowCutoffSlider = document.getElementById('lowCutoffSlider');
const highCutoffSlider = document.getElementById('highCutoffSlider');
const lowCutoffValue = document.getElementById('lowCutoffValue');
const highCutoffValue = document.getElementById('highCutoffValue');
const applyFrequencyFilterBtn = document.getElementById('applyFrequencyFilterBtn');

// Edge Detection
const edgeMethod = document.getElementById('edgeMethod');
const cannyControls = document.getElementById('cannyControls');
const threshold1Slider = document.getElementById('threshold1Slider');
const threshold2Slider = document.getElementById('threshold2Slider');
const threshold1Value = document.getElementById('threshold1Value');
const threshold2Value = document.getElementById('threshold2Value');
const applyEdgeDetectionBtn = document.getElementById('applyEdgeDetectionBtn');
const compareEdgeDetectorsBtn = document.getElementById('compareEdgeDetectorsBtn');

// Segmentation
const segmentMethod = document.getElementById('segmentMethod');
const kmeansControls = document.getElementById('kmeansControls');
const colorSegmentControls = document.getElementById('colorSegmentControls');
const clustersSlider = document.getElementById('clustersSlider');
const clustersValue = document.getElementById('clustersValue');
const colorSpace = document.getElementById('colorSpace');
const lowerHueSlider = document.getElementById('lowerHueSlider');
const upperHueSlider = document.getElementById('upperHueSlider');
const hueRangeValue = document.getElementById('hueRangeValue');
const applySegmentationBtn = document.getElementById('applySegmentationBtn');

// Morphological Operations
const morphologyOperation = document.getElementById('morphologyOperation');
const morphKernelSlider = document.getElementById('morphKernelSlider');
const iterationsSlider = document.getElementById('iterationsSlider');
const morphKernelValue = document.getElementById('morphKernelValue');
const iterationsValue = document.getElementById('iterationsValue');
const applyMorphologyBtn = document.getElementById('applyMorphologyBtn');

// Reset buttons
const resetToOriginalBtn = document.getElementById('resetToOriginalBtn');
const resetToProcessedBtn = document.getElementById('resetToProcessedBtn');

// State management for advanced features
let workingImage = null; // Current image being worked on
let savedProcessedImage = null; // Save the initial processed result

// Initialize advanced features
function initializeAdvancedFeatures() {
    // Toggle advanced panel
    toggleAdvancedBtn.addEventListener('click', toggleAdvancedPanel);
    
    // Histogram processing
    applyHistogramBtn.addEventListener('click', applyHistogramEqualization);
    applyBrightnessContrastBtn.addEventListener('click', applyBrightnessContrast);
    
    // Update slider values
    brightnessSlider.addEventListener('input', () => {
        brightnessValue.textContent = brightnessSlider.value;
    });
    contrastSlider.addEventListener('input', () => {
        contrastValue.textContent = contrastSlider.value;
    });
    gammaSlider.addEventListener('input', () => {
        gammaValue.textContent = gammaSlider.value;
    });
    
    // Spatial filtering
    applySpatialFilterBtn.addEventListener('click', applySpatialFilter);
    kernelSizeSlider.addEventListener('input', () => {
        kernelSizeValue.textContent = kernelSizeSlider.value;
    });
    sigmaSlider.addEventListener('input', () => {
        sigmaValue.textContent = sigmaSlider.value;
    });
    
    // Frequency domain filtering
    applyFrequencyFilterBtn.addEventListener('click', applyFrequencyFilter);
    frequencyFilterType.addEventListener('change', updateFrequencyControls);
    cutoffSlider.addEventListener('input', () => {
        cutoffValue.textContent = cutoffSlider.value;
    });
    lowCutoffSlider.addEventListener('input', () => {
        lowCutoffValue.textContent = lowCutoffSlider.value;
    });
    highCutoffSlider.addEventListener('input', () => {
        highCutoffValue.textContent = highCutoffSlider.value;
    });
    
    // Edge detection
    applyEdgeDetectionBtn.addEventListener('click', applyEdgeDetection);
    compareEdgeDetectorsBtn.addEventListener('click', compareEdgeDetectors);
    edgeMethod.addEventListener('change', updateEdgeControls);
    threshold1Slider.addEventListener('input', () => {
        threshold1Value.textContent = threshold1Slider.value;
    });
    threshold2Slider.addEventListener('input', () => {
        threshold2Value.textContent = threshold2Slider.value;
    });
    
    // Segmentation
    applySegmentationBtn.addEventListener('click', applySegmentation);
    segmentMethod.addEventListener('change', updateSegmentationControls);
    clustersSlider.addEventListener('input', () => {
        clustersValue.textContent = clustersSlider.value;
    });
    lowerHueSlider.addEventListener('input', updateHueRange);
    upperHueSlider.addEventListener('input', updateHueRange);
    
    // Morphological operations
    applyMorphologyBtn.addEventListener('click', applyMorphology);
    morphKernelSlider.addEventListener('input', () => {
        morphKernelValue.textContent = morphKernelSlider.value;
    });
    iterationsSlider.addEventListener('input', () => {
        iterationsValue.textContent = iterationsSlider.value;
    });
    
    // Reset buttons
    resetToOriginalBtn.addEventListener('click', resetToOriginal);
    resetToProcessedBtn.addEventListener('click', resetToProcessed);
}

// Call initialization when DOM loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeAdvancedFeatures);
} else {
    initializeAdvancedFeatures();
}

// Toggle advanced processing panel
function toggleAdvancedPanel() {
    advancedContent.classList.toggle('hidden');
    toggleAdvancedBtn.classList.toggle('active');
}

// Update frequency filter controls based on selected type
function updateFrequencyControls() {
    if (frequencyFilterType.value === 'bandpass') {
        bandpassControls.style.display = 'block';
    } else {
        bandpassControls.style.display = 'none';
    }
}

// Update edge detection controls based on method
function updateEdgeControls() {
    if (edgeMethod.value === 'canny') {
        cannyControls.style.display = 'block';
    } else {
        cannyControls.style.display = 'none';
    }
}

// Update segmentation controls based on method
function updateSegmentationControls() {
    const method = segmentMethod.value;
    
    kmeansControls.style.display = method === 'kmeans' ? 'block' : 'none';
    colorSegmentControls.style.display = method === 'color' ? 'block' : 'none';
}

// Update hue range display
function updateHueRange() {
    hueRangeValue.textContent = `${lowerHueSlider.value}-${upperHueSlider.value}`;
}

// Get current working image as blob
async function getCurrentImageBlob() {
    return new Promise((resolve) => {
        imageCanvas.toBlob(resolve, 'image/png');
    });
}

// Apply histogram equalization
async function applyHistogramEqualization() {
    if (!currentImage || !backendAvailable) {
        showNotification('No image available or backend not connected', 'error');
        return;
    }
    
    try {
        showLoading('Applying histogram equalization...');
        
        const blob = await getCurrentImageBlob();
        const formData = new FormData();
        formData.append('file', blob, 'image.png');
        formData.append('method', histogramMethod.value);
        
        const response = await fetch(`${API_BASE_URL}/api/histogram-equalization`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) throw new Error('Histogram equalization failed');
        
        const resultBlob = await response.blob();
        const imageUrl = URL.createObjectURL(resultBlob);
        
        const resultImage = new Image();
        resultImage.onload = () => {
            currentImage = resultImage;
            workingImage = resultImage;
            displayImage(resultImage);
            updateStatus(`Histogram equalization (${histogramMethod.value}) applied`);
            hideLoading();
            showNotification('Histogram equalization applied successfully!', 'success');
        };
        resultImage.src = imageUrl;
        
    } catch (error) {
        console.error('Error:', error);
        hideLoading();
        showNotification('Failed to apply histogram equalization', 'error');
    }
}

// Apply brightness/contrast adjustments
async function applyBrightnessContrast() {
    if (!currentImage || !backendAvailable) {
        showNotification('No image available or backend not connected', 'error');
        return;
    }
    
    try {
        showLoading('Adjusting brightness and contrast...');
        
        const blob = await getCurrentImageBlob();
        const formData = new FormData();
        formData.append('file', blob, 'image.png');
        formData.append('brightness', brightnessSlider.value);
        formData.append('contrast', contrastSlider.value);
        formData.append('gamma', gammaSlider.value);
        
        const response = await fetch(`${API_BASE_URL}/api/adjust-brightness-contrast`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) throw new Error('Adjustment failed');
        
        const resultBlob = await response.blob();
        const imageUrl = URL.createObjectURL(resultBlob);
        
        const resultImage = new Image();
        resultImage.onload = () => {
            currentImage = resultImage;
            workingImage = resultImage;
            displayImage(resultImage);
            updateStatus('Brightness and contrast adjusted');
            hideLoading();
            showNotification('Adjustments applied successfully!', 'success');
        };
        resultImage.src = imageUrl;
        
    } catch (error) {
        console.error('Error:', error);
        hideLoading();
        showNotification('Failed to apply adjustments', 'error');
    }
}

// Apply spatial filter
async function applySpatialFilter() {
    if (!currentImage || !backendAvailable) {
        showNotification('No image available or backend not connected', 'error');
        return;
    }
    
    try {
        showLoading(`Applying ${spatialFilterType.value} filter...`);
        
        const blob = await getCurrentImageBlob();
        const formData = new FormData();
        formData.append('file', blob, 'image.png');
        formData.append('filter_type', spatialFilterType.value);
        formData.append('kernel_size', kernelSizeSlider.value);
        formData.append('sigma', sigmaSlider.value);
        
        const response = await fetch(`${API_BASE_URL}/api/spatial-filter`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) throw new Error('Spatial filtering failed');
        
        const resultBlob = await response.blob();
        const imageUrl = URL.createObjectURL(resultBlob);
        
        const resultImage = new Image();
        resultImage.onload = () => {
            currentImage = resultImage;
            workingImage = resultImage;
            displayImage(resultImage);
            updateStatus(`${spatialFilterType.value} filter applied`);
            hideLoading();
            showNotification('Spatial filter applied successfully!', 'success');
        };
        resultImage.src = imageUrl;
        
    } catch (error) {
        console.error('Error:', error);
        hideLoading();
        showNotification('Failed to apply spatial filter', 'error');
    }
}

// Apply frequency domain filter
async function applyFrequencyFilter() {
    if (!currentImage || !backendAvailable) {
        showNotification('No image available or backend not connected', 'error');
        return;
    }
    
    try {
        showLoading(`Applying ${frequencyFilterType.value} frequency filter...`);
        
        const blob = await getCurrentImageBlob();
        const formData = new FormData();
        formData.append('file', blob, 'image.png');
        formData.append('filter_type', frequencyFilterType.value);
        formData.append('cutoff', cutoffSlider.value);
        formData.append('order', '2');
        formData.append('low_cutoff', lowCutoffSlider.value);
        formData.append('high_cutoff', highCutoffSlider.value);
        
        const response = await fetch(`${API_BASE_URL}/api/frequency-filter`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) throw new Error('Frequency filtering failed');
        
        const resultBlob = await response.blob();
        const imageUrl = URL.createObjectURL(resultBlob);
        
        const resultImage = new Image();
        resultImage.onload = () => {
            currentImage = resultImage;
            workingImage = resultImage;
            displayImage(resultImage);
            updateStatus(`${frequencyFilterType.value} frequency filter applied`);
            hideLoading();
            showNotification('Frequency filter applied successfully!', 'success');
        };
        resultImage.src = imageUrl;
        
    } catch (error) {
        console.error('Error:', error);
        hideLoading();
        showNotification('Failed to apply frequency filter', 'error');
    }
}

// Apply edge detection
async function applyEdgeDetection() {
    if (!currentImage || !backendAvailable) {
        showNotification('No image available or backend not connected', 'error');
        return;
    }
    
    try {
        showLoading(`Detecting edges using ${edgeMethod.value}...`);
        
        const blob = await getCurrentImageBlob();
        const formData = new FormData();
        formData.append('file', blob, 'image.png');
        formData.append('method', edgeMethod.value);
        formData.append('threshold1', threshold1Slider.value);
        formData.append('threshold2', threshold2Slider.value);
        formData.append('kernel_size', '3');
        
        const response = await fetch(`${API_BASE_URL}/api/edge-detection`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) throw new Error('Edge detection failed');
        
        const resultBlob = await response.blob();
        const imageUrl = URL.createObjectURL(resultBlob);
        
        const resultImage = new Image();
        resultImage.onload = () => {
            currentImage = resultImage;
            workingImage = resultImage;
            displayImage(resultImage);
            updateStatus(`Edge detection (${edgeMethod.value}) applied`);
            hideLoading();
            showNotification('Edge detection applied successfully!', 'success');
        };
        resultImage.src = imageUrl;
        
    } catch (error) {
        console.error('Error:', error);
        hideLoading();
        showNotification('Failed to apply edge detection', 'error');
    }
}

// Compare all edge detectors
async function compareEdgeDetectors() {
    if (!currentImage || !backendAvailable) {
        showNotification('No image available or backend not connected', 'error');
        return;
    }
    
    try {
        showLoading('Comparing edge detection methods...');
        
        const blob = await getCurrentImageBlob();
        const formData = new FormData();
        formData.append('file', blob, 'image.png');
        
        const response = await fetch(`${API_BASE_URL}/api/compare-edge-detectors`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) throw new Error('Edge detector comparison failed');
        
        const data = await response.json();
        hideLoading();
        
        // Display comparison results
        showEdgeComparisonModal(data.results);
        
    } catch (error) {
        console.error('Error:', error);
        hideLoading();
        showNotification('Failed to compare edge detectors', 'error');
    }
}

// Show edge comparison modal
function showEdgeComparisonModal(results) {
    const modal = document.createElement('div');
    modal.className = 'edge-comparison-modal';
    modal.innerHTML = `
        <div class="edge-comparison-content">
            <div class="batch-results-header">
                <h2>🔍 Edge Detector Comparison</h2>
                <button class="close-modal" onclick="this.parentElement.parentElement.parentElement.remove()">✕</button>
            </div>
            <div class="edge-comparison-grid">
                ${Object.entries(results).map(([method, imageData]) => `
                    <div class="edge-result-item">
                        <h4>${method.toUpperCase()}</h4>
                        <img src="${imageData}" alt="${method}">
                    </div>
                `).join('')}
            </div>
            <div class="batch-results-actions">
                <button class="btn-secondary" onclick="this.parentElement.parentElement.parentElement.remove()">Close</button>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
}

// Apply segmentation
async function applySegmentation() {
    if (!currentImage || !backendAvailable) {
        showNotification('No image available or backend not connected', 'error');
        return;
    }
    
    try {
        const method = segmentMethod.value;
        showLoading(`Applying ${method} segmentation...`);
        
        const blob = await getCurrentImageBlob();
        const formData = new FormData();
        formData.append('file', blob, 'image.png');
        
        let endpoint = '';
        
        if (method === 'otsu' || method === 'adaptive') {
            endpoint = '/api/segment-threshold';
            formData.append('method', method);
            formData.append('block_size', '11');
            formData.append('C', '2');
        } else if (method === 'kmeans') {
            endpoint = '/api/segment-kmeans';
            formData.append('k', clustersSlider.value);
        } else if (method === 'color') {
            endpoint = '/api/segment-color';
            formData.append('color_space', colorSpace.value);
            formData.append('lower_h', lowerHueSlider.value);
            formData.append('lower_s', '50');
            formData.append('lower_v', '50');
            formData.append('upper_h', upperHueSlider.value);
            formData.append('upper_s', '255');
            formData.append('upper_v', '255');
        } else if (method === 'watershed') {
            endpoint = '/api/segment-watershed';
        }
        
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) throw new Error('Segmentation failed');
        
        const resultBlob = await response.blob();
        const imageUrl = URL.createObjectURL(resultBlob);
        
        const resultImage = new Image();
        resultImage.onload = () => {
            currentImage = resultImage;
            workingImage = resultImage;
            displayImage(resultImage);
            updateStatus(`${method} segmentation applied`);
            hideLoading();
            showNotification('Segmentation applied successfully!', 'success');
        };
        resultImage.src = imageUrl;
        
    } catch (error) {
        console.error('Error:', error);
        hideLoading();
        showNotification('Failed to apply segmentation', 'error');
    }
}

// Apply morphological operations
async function applyMorphology() {
    if (!currentImage || !backendAvailable) {
        showNotification('No image available or backend not connected', 'error');
        return;
    }
    
    try {
        showLoading(`Applying ${morphologyOperation.value} operation...`);
        
        const blob = await getCurrentImageBlob();
        const formData = new FormData();
        formData.append('file', blob, 'image.png');
        formData.append('operation', morphologyOperation.value);
        formData.append('kernel_size', morphKernelSlider.value);
        formData.append('iterations', iterationsSlider.value);
        
        const response = await fetch(`${API_BASE_URL}/api/morphology`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) throw new Error('Morphological operation failed');
        
        const resultBlob = await response.blob();
        const imageUrl = URL.createObjectURL(resultBlob);
        
        const resultImage = new Image();
        resultImage.onload = () => {
            currentImage = resultImage;
            workingImage = resultImage;
            displayImage(resultImage);
            updateStatus(`${morphologyOperation.value} operation applied`);
            hideLoading();
            showNotification('Morphological operation applied successfully!', 'success');
        };
        resultImage.src = imageUrl;
        
    } catch (error) {
        console.error('Error:', error);
        hideLoading();
        showNotification('Failed to apply morphological operation', 'error');
    }
}

// Reset to original image
function resetToOriginal() {
    if (!originalImage) {
        showNotification('No original image available', 'error');
        return;
    }
    
    currentImage = originalImage;
    workingImage = originalImage;
    displayImage(originalImage);
    updateStatus('Reset to original image');
    showNotification('Reset to original image', 'info');
}

// Reset to processed image (after background removal)
function resetToProcessed() {
    if (!processedImage) {
        showNotification('No processed image available', 'error');
        return;
    }
    
    currentImage = processedImage;
    workingImage = processedImage;
    displayImage(processedImage);
    updateStatus('Reset to processed image');
    showNotification('Reset to processed image', 'info');
}

// Export functions for use in main script
window.advancedProcessing = {
    saveProcessedImage: () => {
        savedProcessedImage = processedImage;
    }
};

console.log('🎨 Advanced Image Processing Module Loaded');
console.log('✓ Histogram Processing');
console.log('✓ Spatial Filtering');
console.log('✓ Frequency Domain Filtering');
console.log('✓ Edge Detection');
console.log('✓ Image Segmentation');
console.log('✓ Morphological Operations');
