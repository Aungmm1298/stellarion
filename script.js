// AI Background Remover - Frontend JavaScript
// Connects to FastAPI backend with U2Net + Real-ESRGAN

const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const uploadSection = document.getElementById('uploadSection');
const editorSection = document.getElementById('editorSection');
const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const backBtn = document.getElementById('backBtn');
const compareBtn = document.getElementById('compareBtn');
const enhanceBtn = document.getElementById('enhanceBtn');
const downloadBtn = document.getElementById('downloadBtn');
const imageCanvas = document.getElementById('imageCanvas');
const loadingOverlay = document.getElementById('loadingOverlay');
const statusText = document.getElementById('statusText');
const processingStats = document.getElementById('processingStats');

// AI Feature controls
const autoCropCheck = document.getElementById('autoCropCheck');
const edgeRefinementCheck = document.getElementById('edgeRefinementCheck');
const bgColorPicker = document.getElementById('bgColorPicker');
const applyCustomColorBtn = document.getElementById('applyCustomColorBtn');
const customColorSection = document.getElementById('customColorSection');

// State management
let originalImage = null;
let processedImage = null;
let currentImage = null;
let currentFile = null;
let isComparing = false;
let backendAvailable = false;
let processingStartTime = 0;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    checkBackendStatus();
    setupEventListeners();
});

// Check if backend is available
async function checkBackendStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/status`);
        const data = await response.json();
        backendAvailable = data.api_status === 'online';
        
        if (backendAvailable) {
            showNotification('Backend connected! AI ready.', 'success');
            console.log(`Backend: ${data.api_status}, Device: ${data.device}, U²Net: ${data.models.u2net}`);
            console.log(`Enhancement: ${data.models.enhancement || 'Unknown'}`);
        } else {
            showNotification('Backend is not available. Please start the server.', 'error');
        }
    } catch (error) {
        backendAvailable = false;
        showNotification('Cannot connect to backend. Please start the server.', 'error');
        console.error('Backend connection error:', error);
    }
}

// Setup all event listeners
function setupEventListeners() {
    // Upload triggers
    uploadBtn.addEventListener('click', () => fileInput.click());
    uploadBox.addEventListener('click', (e) => {
        if (e.target !== uploadBtn) {
            fileInput.click();
        }
    });
    
    // File input change
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop
    uploadBox.addEventListener('dragover', handleDragOver);
    uploadBox.addEventListener('dragleave', handleDragLeave);
    uploadBox.addEventListener('drop', handleDrop);
    
    // Navigation
    backBtn.addEventListener('click', goBackToUpload);
    
    // Actions
    compareBtn.addEventListener('click', toggleCompare);
    enhanceBtn.addEventListener('click', handleEnhance);
    downloadBtn.addEventListener('click', downloadImage);
    
    // AI Features
    if (applyCustomColorBtn) {
        applyCustomColorBtn.addEventListener('click', applyBackgroundColor);
    }
    
    // Background preset buttons
    document.querySelectorAll('.bg-preset').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const color = btn.dataset.color;
            handleBackgroundPreset(color, btn);
        });
    });
    
    // Feature checkboxes - reprocess on change
    autoCropCheck.addEventListener('change', reprocessWithFeatures);
    edgeRefinementCheck.addEventListener('change', reprocessWithFeatures);
}

// No need for setupSliders - removed sliders from HTML

// Drag and drop handlers
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadBox.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadBox.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadBox.classList.remove('drag-over');
    
    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
        if (files.length === 1) {
            processFile(files[0]);
        } else {
            processBatchFiles(files);
        }
    }
}

// File selection handler - SUPPORTS MULTIPLE FILES
function handleFileSelect(e) {
    const files = Array.from(e.target.files);
    if (files.length === 0) return;
    
    if (files.length === 1) {
        // Single file processing
        processFile(files[0]);
    } else {
        // Batch processing
        processBatchFiles(files);
    }
}

// Process uploaded file
async function processFile(file) {
    // Validate file
    if (!file.type.startsWith('image/')) {
        showNotification('Please upload a valid image file', 'error');
        return;
    }
    
    if (file.size > 10 * 1024 * 1024) {
        showNotification('File size must be less than 10MB', 'error');
        return;
    }
    
    // Check backend
    if (!backendAvailable) {
        showNotification('Backend server is not running. Please start the server first.', 'error');
        return;
    }
    
    // Store file for enhancement later
    currentFile = file;
    
    // Load and display original image
    const reader = new FileReader();
    reader.onload = async (e) => {
        originalImage = new Image();
        originalImage.onload = async () => {
            // Show editor
            uploadSection.classList.add('hidden');
            editorSection.classList.remove('hidden');
            
            // Display original image
            displayImage(originalImage);
            updateStatus('Original image loaded');
            
            // Automatically process the image
            await processImageWithBackend(file);
        };
        originalImage.src = e.target.result;
    };
    reader.readAsDataURL(file);
}

// Batch process multiple files
async function processBatchFiles(files) {
    if (files.length > 10) {
        showNotification('Maximum 10 images per batch', 'error');
        return;
    }
    
    // Validate all files
    const validFiles = files.filter(file => {
        if (!file.type.startsWith('image/')) return false;
        if (file.size > 10 * 1024 * 1024) return false;
        return true;
    });
    
    if (validFiles.length === 0) {
        showNotification('No valid images found', 'error');
        return;
    }
    
    if (validFiles.length !== files.length) {
        showNotification(`${files.length - validFiles.length} files were skipped (invalid or too large)`, 'warning');
    }
    
    // Check backend
    if (!backendAvailable) {
        showNotification('Backend server is not running. Please start the server first.', 'error');
        return;
    }
    
    try {
        showLoading(`Processing ${validFiles.length} images...`);
        updateStatus(`Batch processing ${validFiles.length} images...`);
        
        // Create form data
        const formData = new FormData();
        validFiles.forEach(file => {
            formData.append('files', file);
        });
        
        // Call batch processing endpoint
        const response = await fetch(`${API_BASE_URL}/api/batch-process`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Batch processing failed');
        }
        
        const result = await response.json();
        hideLoading();
        
        // Show results
        showBatchResults(result);
        
    } catch (error) {
        console.error('Batch processing error:', error);
        hideLoading();
        showNotification(`Batch processing failed: ${error.message}`, 'error');
    }
}

// Show batch processing results
function showBatchResults(result) {
    const { total, successful, failed, results } = result;
    
    // Create results modal
    const modal = document.createElement('div');
    modal.className = 'batch-results-modal';
    modal.innerHTML = `
        <div class="batch-results-content">
            <div class="batch-results-header">
                <h2>🎉 Batch Processing Complete</h2>
                <button class="close-modal" onclick="this.parentElement.parentElement.parentElement.remove()">✕</button>
            </div>
            <div class="batch-results-summary">
                <div class="summary-item">
                    <span class="summary-label">Total:</span>
                    <span class="summary-value">${total}</span>
                </div>
                <div class="summary-item success">
                    <span class="summary-label">Successful:</span>
                    <span class="summary-value">${successful}</span>
                </div>
                ${failed > 0 ? `
                <div class="summary-item error">
                    <span class="summary-label">Failed:</span>
                    <span class="summary-value">${failed}</span>
                </div>
                ` : ''}
            </div>
            <div class="batch-results-grid">
                ${results.map((r, idx) => `
                    <div class="batch-result-item ${r.status}">
                        <div class="result-header">
                            <span class="result-filename">${r.filename}</span>
                            <span class="result-status ${r.status}">${r.status === 'success' ? '✓' : '✕'}</span>
                        </div>
                        ${r.status === 'success' ? `
                            <img src="${r.image}" alt="${r.filename}" class="result-preview">
                            <button class="btn-small download-single" data-image="${r.image}" data-filename="${r.filename}">
                                Download
                            </button>
                        ` : `
                            <p class="result-error">${r.error}</p>
                        `}
                    </div>
                `).join('')}
            </div>
            <div class="batch-results-actions">
                <button class="btn-primary" id="downloadAllBtn">Download All (${successful})</button>
                <button class="btn-secondary" onclick="this.parentElement.parentElement.parentElement.remove()">Close</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Add download handlers
    modal.querySelectorAll('.download-single').forEach(btn => {
        btn.addEventListener('click', () => {
            const image = btn.dataset.image;
            const filename = btn.dataset.filename;
            downloadBase64Image(image, filename);
        });
    });
    
    // Download all button
    const downloadAllBtn = modal.querySelector('#downloadAllBtn');
    if (downloadAllBtn) {
        downloadAllBtn.addEventListener('click', () => {
            results.forEach((r, idx) => {
                if (r.status === 'success') {
                    setTimeout(() => {
                        downloadBase64Image(r.image, r.filename);
                    }, idx * 200); // Stagger downloads
                }
            });
            showNotification(`Downloading ${successful} images...`, 'success');
        });
    }
    
    showNotification(`Batch processing complete! ${successful}/${total} successful`, 'success');
}

// Download base64 encoded image
function downloadBase64Image(dataUrl, filename) {
    const link = document.createElement('a');
    link.href = dataUrl;
    link.download = `processed-${filename}`;
    link.click();
}

// Process image with backend API - ENHANCED with High Quality
async function processImageWithBackend(file) {
    try {
        processingStartTime = performance.now();
        showLoading('Removing background with AI... (High Quality Mode)');
        
        // Create form data with HIGH QUALITY settings
        const formData = new FormData();
        formData.append('file', file);
        formData.append('auto_crop', autoCropCheck.checked);
        formData.append('add_bg_color', 'false'); // Transparent by default
        
        // Call ADVANCED processing endpoint for best quality
        const response = await fetch(`${API_BASE_URL}/api/process-advanced`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Server error: ${response.statusText} - ${errorText}`);
        }
        
        // Get processed image
        const blob = await response.blob();
        const imageUrl = URL.createObjectURL(blob);
        
        processedImage = new Image();
        processedImage.onload = () => {
            currentImage = processedImage;
            displayImage(processedImage);
            
            const processingTime = ((performance.now() - processingStartTime) / 1000).toFixed(2);
            updateStatus(`Background removed successfully! (High Quality) ✓`);
            updateProcessingStats(`Processing time: ${processingTime}s | Quality: Professional | Resolution: ${processedImage.width}x${processedImage.height}`);
            hideLoading();
            showNotification('✓ High-quality background removal complete! Clear & sharp edges!', 'success');
        };
        processedImage.src = imageUrl;
        
    } catch (error) {
        console.error('Processing error:', error);
        hideLoading();
        showNotification(`Processing failed: ${error.message}`, 'error');
        updateStatus('Processing failed');
    }
}

// Handle AI Enhance button - Enhanced quality improvement
async function handleEnhance() {
    if (!currentImage) {
        showNotification('No image to enhance', 'error');
        return;
    }
    
    if (!backendAvailable) {
        showNotification('Backend not available', 'error');
        return;
    }
    
    try {
        processingStartTime = performance.now();
        showLoading('Enhancing image quality with AI...');
        
        // Convert canvas to blob
        const blob = await new Promise(resolve => {
            imageCanvas.toBlob(resolve, 'image/png');
        });
        
        // Create form data
        const formData = new FormData();
        formData.append('file', blob, 'image.png');
        
        // Call enhance API
        const response = await fetch(`${API_BASE_URL}/api/enhance-image`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(errorText);
        }
        
        // Get enhanced image
        const enhancedBlob = await response.blob();
        const imageUrl = URL.createObjectURL(enhancedBlob);
        
        const enhancedImage = new Image();
        enhancedImage.onload = () => {
            currentImage = enhancedImage;
            displayImage(enhancedImage);
            
            const processingTime = ((performance.now() - processingStartTime) / 1000).toFixed(2);
            updateStatus('Image enhanced with AI! ✓');
            updateProcessingStats(`Enhancement time: ${processingTime}s | Resolution: 2x upscaled`);
            hideLoading();
            showNotification('Enhancement applied! Better quality & resolution! ✓', 'success');
        };
        enhancedImage.src = imageUrl;
        
    } catch (error) {
        console.error('Enhancement error:', error);
        hideLoading();
        showNotification(`Enhancement not available. Feature requires Real-ESRGAN model.`, 'warning');
    }
}

// Reprocess with current feature settings
async function reprocessWithFeatures() {
    if (!currentFile) {
        return;
    }
    
    showNotification('Reprocessing with updated settings...', 'info');
    await processImageWithBackend(currentFile);
}

// Handle background preset selection
async function handleBackgroundPreset(color, button) {
    if (!processedImage) {
        showNotification('No processed image available', 'error');
        return;
    }
    
    // Update active state
    document.querySelectorAll('.bg-preset').forEach(btn => btn.classList.remove('active'));
    button.classList.add('active');
    
    if (color === 'custom') {
        // Show custom color picker
        customColorSection.classList.remove('hidden');
        return;
    } else {
        // Hide custom color picker
        customColorSection.classList.add('hidden');
    }
    
    if (color === 'transparent') {
        // Restore transparent version
        currentImage = processedImage;
        displayImage(processedImage);
        updateStatus('Transparent background restored');
        showNotification('Background cleared! ✓', 'success');
        return;
    }
    
    // Apply colored background
    await applyBackgroundColorDirect(color);
}

// Apply background color directly (for presets)
async function applyBackgroundColorDirect(color) {
    if (!processedImage || !backendAvailable) {
        return;
    }
    
    try {
        showLoading('Applying background color...');
        
        const rgb = hexToRgb(color);
        
        // Convert canvas to blob
        const blob = await new Promise(resolve => {
            imageCanvas.toBlob(resolve, 'image/png');
        });
        
        // Create form data
        const formData = new FormData();
        formData.append('file', blob, 'image.png');
        formData.append('auto_crop', autoCropCheck.checked);
        formData.append('add_bg_color', 'true');
        formData.append('bg_color', `${rgb.r},${rgb.g},${rgb.b}`);
        
        // Call advanced processing API
        const response = await fetch(`${API_BASE_URL}/api/process-advanced`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(await response.text());
        }
        
        // Get result
        const resultBlob = await response.blob();
        const imageUrl = URL.createObjectURL(resultBlob);
        
        const resultImage = new Image();
        resultImage.onload = () => {
            currentImage = resultImage;
            displayImage(resultImage);
            updateStatus(`Background color applied: ${color}`);
            hideLoading();
            showNotification('Background color applied! ✓', 'success');
        };
        resultImage.src = imageUrl;
        
    } catch (error) {
        console.error('Background color error:', error);
        hideLoading();
        showNotification(`Failed to apply background color`, 'error');
    }
}

// Helper function to convert hex to RGB
function hexToRgb(hex) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : { r: 255, g: 255, b: 255 };
}

// Apply background color (custom color picker)
async function applyBackgroundColor() {
    const color = bgColorPicker.value;
    await applyBackgroundColorDirect(color);
    
    // Update active state
    document.querySelectorAll('.bg-preset').forEach(btn => btn.classList.remove('active'));
    document.querySelector('.bg-preset.custom').classList.add('active');
}

// Update processing stats display
function updateProcessingStats(text) {
    if (processingStats) {
        processingStats.textContent = text;
    }
}

// Display image on canvas
function displayImage(image) {
    const ctx = imageCanvas.getContext('2d');
    
    // Set canvas size to match image (with max constraints)
    const maxWidth = 800;
    const maxHeight = 600;
    let width = image.width;
    let height = image.height;
    
    // Scale down if too large for display
    if (width > maxWidth || height > maxHeight) {
        const ratio = Math.min(maxWidth / width, maxHeight / height);
        width *= ratio;
        height *= ratio;
    }
    
    imageCanvas.width = width;
    imageCanvas.height = height;
    
    // Draw checkerboard background for transparency
    drawCheckerboard(ctx, width, height);
    
    // Draw image
    ctx.drawImage(image, 0, 0, width, height);
}

// Draw checkerboard pattern (for transparency visualization)
function drawCheckerboard(ctx, width, height) {
    const squareSize = 20;
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, width, height);
    
    ctx.fillStyle = '#e0e0e0';
    for (let y = 0; y < height; y += squareSize) {
        for (let x = 0; x < width; x += squareSize) {
            if ((x / squareSize + y / squareSize) % 2 === 0) {
                ctx.fillRect(x, y, squareSize, squareSize);
            }
        }
    }
}

// Toggle compare view (original vs processed)
function toggleCompare() {
    if (!originalImage || !processedImage) {
        showNotification('No comparison available yet', 'info');
        return;
    }
    
    isComparing = !isComparing;
    
    if (isComparing) {
        displayImage(originalImage);
        compareBtn.innerHTML = '👁️ Show Result';
        updateStatus('Showing original image');
    } else {
        displayImage(currentImage);
        compareBtn.innerHTML = '👁️ Compare';
        updateStatus('Showing processed image');
    }
}

// Download processed image as PNG
function downloadImage() {
    if (!imageCanvas) {
        showNotification('No image to download', 'error');
        return;
    }
    
    // Get full resolution image from canvas
    const link = document.createElement('a');
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
    link.download = `background-removed-${timestamp}.png`;
    
    // Use full canvas data
    link.href = imageCanvas.toDataURL('image/png', 1.0);
    link.click();
    
    showNotification('Image downloaded successfully! ✓', 'success');
}

// Go back to upload screen
function goBackToUpload() {
    uploadSection.classList.remove('hidden');
    editorSection.classList.add('hidden');
    
    // Reset state
    originalImage = null;
    processedImage = null;
    currentImage = null;
    currentFile = null;
    isComparing = false;
    
    // Reset file input
    fileInput.value = '';
    
    // Clear canvas
    const ctx = imageCanvas.getContext('2d');
    ctx.clearRect(0, 0, imageCanvas.width, imageCanvas.height);
}

// Reset enhancement settings (UI placeholders)
function resetEnhancementSettings() {
    edgeSlider.value = 50;
    smoothSlider.value = 50;
    toleranceSlider.value = 60;
    edgeValue.textContent = '50%';
    smoothValue.textContent = '50%';
    toleranceValue.textContent = '60';
    showNotification('Settings reset to default', 'info');
}

// Show loading overlay
function showLoading(message = 'Processing...') {
    loadingOverlay.classList.remove('hidden');
    const loadingText = loadingOverlay.querySelector('p');
    if (loadingText) {
        loadingText.textContent = message;
    }
}

// Hide loading overlay
function hideLoading() {
    loadingOverlay.classList.add('hidden');
}

// Update status text
function updateStatus(message) {
    statusText.textContent = message;
}

// Show notification toast
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Style the notification
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '15px 25px',
        borderRadius: '8px',
        backgroundColor: type === 'error' ? '#ff4444' : 
                        type === 'success' ? '#00C851' : 
                        type === 'warning' ? '#ffbb33' : '#33b5e5',
        color: 'white',
        fontWeight: '500',
        fontSize: '14px',
        boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
        zIndex: '10000',
        maxWidth: '400px',
        animation: 'slideInRight 0.3s ease'
    });
    
    document.body.appendChild(notification);
    
    // Remove after 4 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}

// Add CSS animations
const styleSheet = document.createElement('style');
styleSheet.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
    
    .drag-over {
        border-color: #6c5ce7 !important;
        background-color: rgba(108, 92, 231, 0.05) !important;
        transform: scale(1.02);
        transition: all 0.3s ease;
    }
    
    .upload-box {
        transition: all 0.3s ease;
    }
`;
document.head.appendChild(styleSheet);

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // ESC to go back
    if (e.key === 'Escape' && !editorSection.classList.contains('hidden')) {
        goBackToUpload();
    }
    
    // Space to toggle compare
    if (e.key === ' ' && !editorSection.classList.contains('hidden')) {
        e.preventDefault();
        toggleCompare();
    }
    
    // D to download
    if (e.key === 'd' && !editorSection.classList.contains('hidden')) {
        downloadImage();
    }
});

console.log('🎨 AI Background Remover Loaded');
console.log('📡 Backend URL:', API_BASE_URL);
console.log('📋 Keyboard shortcuts: ESC (back), SPACE (compare), D (download)');
console.log('🔗 Backend running at: http://localhost:8000');
