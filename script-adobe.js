// Adobe-Style Background Remover - Enhanced Frontend
// Professional workflow with instant processing and comparison slider

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
const originalCanvas = document.getElementById('originalCanvas');
const processedCanvas = document.getElementById('processedCanvas');
const singleView = document.getElementById('singleView');
const comparisonGrid = document.getElementById('comparisonGrid');
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
            console.log('✓ Backend connected:', data.device);
        } else {
            showNotification('Please start the backend server', 'error');
        }
    } catch (error) {
        backendAvailable = false;
        showNotification('Cannot connect to backend. Please start the server.', 'error');
    }
}

// Setup all event listeners
function setupEventListeners() {
    // Upload triggers
    uploadBtn.addEventListener('click', () => fileInput.click());
    uploadBox.addEventListener('click', (e) => {
        if (e.target !== uploadBtn) fileInput.click();
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
    
    // Background option buttons - update to use .bg-option class
    document.querySelectorAll('.bg-option').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const color = btn.dataset.color;
            handleBackgroundPreset(color, btn);
        });
    });
    
    // Feature checkboxes - reprocess on change
    autoCropCheck.addEventListener('change', reprocessWithFeatures);
    edgeRefinementCheck.addEventListener('change', reprocessWithFeatures);
}

// Comparison is now simple toggle - no complex slider needed

// Drag and drop handlers
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadBox.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadBox.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadBox.classList.remove('dragover');
    
    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
        processFile(files[0]); // Single file only
    }
}

// File selection handler
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        processFile(file);
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
    
    // Store file
    currentFile = file;
    
    // Load and display original image
    const reader = new FileReader();
    reader.onload = async (e) => {
        originalImage = new Image();
        originalImage.onload = async () => {
            // Show editor
            uploadSection.classList.add('hidden');
            editorSection.classList.remove('hidden');
            
            // Display original image temporarily
            displayImage(originalImage, imageCanvas);
            updateStatus('Processing with AI...');
            
            // Automatically process the image
            await processImageWithBackend(file);
        };
        originalImage.src = e.target.result;
    };
    reader.readAsDataURL(file);
}

// Process image with backend API
async function processImageWithBackend(file) {
    try {
        processingStartTime = performance.now();
        showLoading('Removing background...');
        
        // Create form data
        const formData = new FormData();
        formData.append('file', file);
        formData.append('auto_crop', autoCropCheck.checked);
        formData.append('add_bg_color', 'false');
        
        // Call ADVANCED processing endpoint
        const response = await fetch(`${API_BASE_URL}/api/process-advanced`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`Processing failed: ${response.statusText}`);
        }
        
        // Get processed image
        const blob = await response.blob();
        const imageUrl = URL.createObjectURL(blob);
        
        processedImage = new Image();
        processedImage.onload = () => {
            currentImage = processedImage;
            displayImage(processedImage, imageCanvas);
            
            const processingTime = ((performance.now() - processingStartTime) / 1000).toFixed(2);
            updateStatus('Background removed');
            updateProcessingStats(`${processingTime}s • ${processedImage.width} × ${processedImage.height}px • Professional quality`);
            hideLoading();
            showNotification('Background removed successfully!', 'success');
        };
        processedImage.src = imageUrl;
        
    } catch (error) {
        console.error('Processing error:', error);
        hideLoading();
        showNotification(`Processing failed: ${error.message}`, 'error');
        updateStatus('Processing failed');
    }
}

// Handle AI Enhance button
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
        showLoading('Enhancing quality (2x upscale)...');
        
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
            throw new Error('Enhancement not available');
        }
        
        // Get enhanced image
        const enhancedBlob = await response.blob();
        const imageUrl = URL.createObjectURL(enhancedBlob);
        
        const enhancedImage = new Image();
        enhancedImage.onload = () => {
            currentImage = enhancedImage;
            displayImage(enhancedImage, imageCanvas);
            
            const processingTime = ((performance.now() - processingStartTime) / 1000).toFixed(2);
            updateStatus('Enhanced with AI');
            updateProcessingStats(`${processingTime}s • ${enhancedImage.width} × ${enhancedImage.height}px • 2x upscaled`);
            hideLoading();
            showNotification('Image enhanced successfully!', 'success');
        };
        enhancedImage.src = imageUrl;
        
    } catch (error) {
        console.error('Enhancement error:', error);
        hideLoading();
        showNotification('Enhancement requires Real-ESRGAN model', 'warning');
    }
}

// Reprocess with current feature settings
async function reprocessWithFeatures() {
    if (!currentFile) return;
    await processImageWithBackend(currentFile);
}

// Handle background preset selection
function handleBackgroundPreset(color, button) {
    if (!processedImage) {
        showNotification('No processed image available', 'error');
        return;
    }
    
    // Update active state
    document.querySelectorAll('.bg-option').forEach(btn => {
        btn.classList.remove('border-adobe-blue', 'ring-2', 'ring-adobe-blue/20');
        btn.classList.add('border-gray-300');
    });
    button.classList.remove('border-gray-300');
    button.classList.add('border-adobe-blue', 'ring-2', 'ring-adobe-blue/20');
    
    if (color === 'custom') {
        customColorSection.classList.remove('hidden');
        return;
    } else {
        customColorSection.classList.add('hidden');
    }
    
    if (color === 'transparent') {
        currentImage = processedImage;
        displayImage(processedImage, imageCanvas);
        updateStatus('Transparent background');
        return;
    }
    
    // Apply colored background - INSTANT!
    applyBackgroundColorDirect(color);
}

// Apply background color directly - CLIENT-SIDE (INSTANT!)
function applyBackgroundColorDirect(color) {
    if (!processedImage) return;
    
    try {
        const rgb = hexToRgb(color);
        
        // Create a temporary canvas to composite background
        const tempCanvas = document.createElement('canvas');
        tempCanvas.width = processedImage.width;
        tempCanvas.height = processedImage.height;
        const ctx = tempCanvas.getContext('2d');
        
        // Fill background color
        ctx.fillStyle = color;
        ctx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);
        
        // Draw processed image on top
        ctx.drawImage(processedImage, 0, 0);
        
        // Convert to image and display
        const dataUrl = tempCanvas.toDataURL('image/png');
        const resultImage = new Image();
        resultImage.onload = () => {
            currentImage = resultImage;
            displayImage(resultImage, imageCanvas);
            updateStatus(`Background: ${color}`);
            showNotification('Background applied instantly!', 'success');
        };
        resultImage.src = dataUrl;
        
    } catch (error) {
        console.error('Background error:', error);
        showNotification('Failed to apply background', 'error');
    }
}

function hexToRgb(hex) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : { r: 255, g: 255, b: 255 };
}

// Apply custom background color
function applyBackgroundColor() {
    const color = bgColorPicker.value;
    applyBackgroundColorDirect(color);
    
    document.querySelectorAll('.bg-option').forEach(btn => {
        btn.classList.remove('border-adobe-blue', 'ring-2', 'ring-adobe-blue/20');
        btn.classList.add('border-gray-300');
    });
    const customBtn = document.querySelector('.bg-option[data-color="custom"]');
    customBtn.classList.remove('border-gray-300');
    customBtn.classList.add('border-adobe-blue', 'ring-2', 'ring-adobe-blue/20');
}

function updateProcessingStats(text) {
    if (processingStats) {
        processingStats.textContent = text;
    }
}

// Display image on canvas
function displayImage(image, canvas) {
    const ctx = canvas.getContext('2d');
    
    // Set canvas size to match image
    const maxWidth = 1200;
    const maxHeight = 800;
    let width = image.width;
    let height = image.height;
    
    // Scale down if too large
    if (width > maxWidth || height > maxHeight) {
        const ratio = Math.min(maxWidth / width, maxHeight / height);
        width *= ratio;
        height *= ratio;
    }
    
    canvas.width = width;
    canvas.height = height;
    
    // Draw image
    ctx.clearRect(0, 0, width, height);
    ctx.drawImage(image, 0, 0, width, height);
}

// Toggle compare view - GRID COMPARISON
function toggleCompare() {
    if (!originalImage || !processedImage) {
        showNotification('Process an image first', 'info');
        return;
    }
    
    isComparing = !isComparing;
    
    if (isComparing) {
        // Show grid comparison
        singleView.classList.add('hidden');
        comparisonGrid.classList.remove('hidden');
        
        // Display both images side by side
        displayImage(originalImage, originalCanvas);
        displayImage(currentImage, processedCanvas);
        
        compareBtn.classList.add('bg-adobe-blue', 'text-white', 'border-adobe-blue');
        compareBtn.classList.remove('bg-white', 'text-gray-900');
        compareBtn.innerHTML = `
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="7" height="7"/>
                <rect x="14" y="3" width="7" height="7"/>
            </svg>
            <span>Single View</span>
        `;
        updateStatus('Comparing: Original vs Processed');
    } else {
        // Show single view
        singleView.classList.remove('hidden');
        comparisonGrid.classList.add('hidden');
        
        displayImage(currentImage, imageCanvas);
        
        compareBtn.classList.remove('bg-adobe-blue', 'text-white', 'border-adobe-blue');
        compareBtn.classList.add('bg-white', 'text-gray-900');
        compareBtn.innerHTML = `
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 3v18M3 12h18"/>
                <circle cx="12" cy="12" r="1"/>
            </svg>
            <span>Compare</span>
        `;
        updateStatus('Background removed');
    }
}

// Download processed image
function downloadImage() {
    if (!imageCanvas) {
        showNotification('No image to download', 'error');
        return;
    }
    
    const link = document.createElement('a');
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
    link.download = `removed-bg-${timestamp}.png`;
    link.href = imageCanvas.toDataURL('image/png', 1.0);
    link.click();
    
    showNotification('Image downloaded!', 'success');
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
    
    // Reset UI
    fileInput.value = '';
    if (comparisonGrid) comparisonGrid.classList.add('hidden');
    if (singleView) singleView.classList.remove('hidden');
    if (compareBtn) {
        compareBtn.classList.remove('bg-adobe-blue', 'text-white', 'border-adobe-blue');
        compareBtn.classList.add('bg-white', 'text-gray-900');
        compareBtn.innerHTML = `
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 3v18M3 12h18"/>
                <circle cx="12" cy="12" r="1"/>
            </svg>
            <span>Compare</span>
        `;
    }
    
    // Clear canvas
    if (imageCanvas) {
        const ctx = imageCanvas.getContext('2d');
        ctx.clearRect(0, 0, imageCanvas.width, imageCanvas.height);
    }
}

// Show loading overlay
function showLoading(message = 'Processing...') {
    loadingOverlay.classList.remove('hidden');
    const loadingText = loadingOverlay.querySelector('.loading-text');
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
    if (statusText) {
        statusText.textContent = message;
    }
}

// Show notification toast
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideInUp 0.3s ease reverse';
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (editorSection.classList.contains('hidden')) return;
    
    // ESC to go back
    if (e.key === 'Escape') {
        goBackToUpload();
    }
    
    // C to toggle compare
    if (e.key === 'c' || e.key === 'C') {
        toggleCompare();
    }
    
    // D to download
    if (e.key === 'd' || e.key === 'D') {
        e.preventDefault();
        downloadImage();
    }
});

console.log('✓ Adobe-style Background Remover loaded');
console.log('→ Keyboard: ESC (back) • C (compare) • D (download)');
