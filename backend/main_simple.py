from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from PIL import Image
import io
import logging
import numpy as np
import onnxruntime as ort
from typing import Optional
import requests
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Background Remover",
    description="Remove backgrounds using U²Net AI model",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model paths
MODEL_PATH = Path("u2net.onnx")
MODEL_URL = "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx"

def download_model():
    """Download U2Net model if not exists"""
    if not MODEL_PATH.exists():
        logger.info("Downloading U2Net model...")
        response = requests.get(MODEL_URL, stream=True)
        total = int(response.headers.get('content-length', 0))
        
        with open(MODEL_PATH, 'wb') as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                if total > 0:
                    percent = (downloaded / total) * 100
                    if downloaded % (1024 * 1024) == 0:  # Every MB
                        logger.info(f"Downloaded: {percent:.1f}%")
        
        logger.info("Model downloaded successfully!")

# Global session
ort_session = None

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    global ort_session
    try:
        download_model()
        logger.info("Loading ONNX model...")
        ort_session = ort.InferenceSession(str(MODEL_PATH))
        logger.info("Model loaded successfully!")
    except Exception as e:
        logger.error(f"Error loading model: {e}")

def normalize(img, mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)):
    """Normalize image"""
    img = img.astype(np.float32) / 255.0
    img = (img - mean) / std
    return img.astype(np.float32)

def remove_background_simple(image: Image.Image) -> Image.Image:
    """Remove background using U2Net - high quality like professional tools"""
    # Store original size
    orig_size = image.size
    
    # Convert to RGB for model processing only
    if image.mode != 'RGB':
        image_rgb = image.convert('RGB')
    else:
        image_rgb = image
    
    # Resize to 320x320 for model
    image_resized = image_rgb.resize((320, 320), Image.BILINEAR)
    
    # Convert to numpy
    img_array = np.array(image_resized)
    img_array = normalize(img_array)
    
    # CHW format and add batch dimension
    img_array = img_array.transpose((2, 0, 1))
    img_array = np.expand_dims(img_array, 0)
    
    # Run model
    ort_inputs = {ort_session.get_inputs()[0].name: img_array}
    ort_outs = ort_session.run(None, ort_inputs)
    
    # Get mask - U2Net outputs the main object
    mask = ort_outs[0][0][0]
    
    # Normalize mask to 0-1
    mask_min, mask_max = mask.min(), mask.max()
    if mask_max > mask_min:
        mask = (mask - mask_min) / (mask_max - mask_min)
    
    # Use dynamic threshold based on percentile for better object detection
    threshold = np.percentile(mask[mask > 0.1], 20)  # Keep more detail
    threshold = max(0.15, min(threshold, 0.35))  # Clamp between 0.15-0.35
    
    # Create binary mask
    mask = (mask > threshold).astype(np.float32)
    
    # Advanced morphological operations for clean edges
    from scipy.ndimage import binary_fill_holes, binary_dilation, binary_opening, binary_closing, gaussian_filter
    
    mask_bool = mask > 0.5
    
    # Opening: remove small noise
    mask_bool = binary_opening(mask_bool, iterations=1)
    
    # Fill holes in the main object
    mask_bool = binary_fill_holes(mask_bool)
    
    # Closing: smooth the boundary
    mask_bool = binary_closing(mask_bool, iterations=2)
    
    # Dilate to ensure we keep all object edges (especially important for furniture)
    mask_bool = binary_dilation(mask_bool, iterations=3)
    
    # Convert back to float for smoothing
    mask = mask_bool.astype(np.float32)
    
    # Apply stronger Gaussian blur for very smooth edges (professional quality)
    mask = gaussian_filter(mask, sigma=4)
    
    # Convert to 0-255 range
    mask = (mask * 255).astype(np.uint8)
    
    # Resize mask back to original size with highest quality interpolation
    mask_img = Image.fromarray(mask).resize(orig_size, Image.LANCZOS)
    
    # Create RGBA image with transparent background
    if image.mode == 'RGBA':
        result = image.copy()
    else:
        result = image_rgb.convert('RGBA')
    
    # Apply mask as alpha channel (this makes removed areas transparent)
    result.putalpha(mask_img)
    
    return result

@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "online",
        "message": "AI Background Remover API",
        "model": "U2Net (ONNX)"
    }

@app.post("/api/remove-background")
async def remove_background(file: UploadFile = File(...)):
    """Remove background from image with AI enhancement"""
    try:
        if ort_session is None:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        # Sanitize filename for logging
        safe_filename = file.filename.encode('ascii', 'ignore').decode('ascii')
        logger.info(f"Processing: {safe_filename}")
        
        # Read image
        contents = await file.read()
        input_image = Image.open(io.BytesIO(contents))
        
        # Remove background
        output_image = remove_background_simple(input_image)
        
        # Apply Professional Image Processing Enhancement
        logger.info("Applying advanced image processing...")
        from PIL import ImageEnhance, ImageFilter
        from scipy.ndimage import median_filter, gaussian_filter, uniform_filter
        from scipy.signal import wiener
        
        if output_image.mode == 'RGBA':
            # Separate RGB and alpha
            rgb = output_image.convert('RGB')
            alpha = output_image.split()[3]
            
            # Convert to numpy for advanced processing
            img_array = np.array(rgb, dtype=np.float32) / 255.0
            
            # 1. Median filter for salt & pepper noise removal (preserves edges)
            for i in range(3):  # Process each color channel
                img_array[:,:,i] = median_filter(img_array[:,:,i], size=3)
            
            # 2. Bilateral filtering simulation (edge-preserving smoothing)
            # Combine local mean with gaussian for texture preservation
            for i in range(3):
                img_array[:,:,i] = gaussian_filter(img_array[:,:,i], sigma=0.8)
            
            # 3. Unsharp masking for detail enhancement
            blurred = gaussian_filter(img_array, sigma=2.0)
            sharpened = img_array + 2.5 * (img_array - blurred)  # Strong unsharp mask
            img_array = np.clip(sharpened, 0, 1)
            
            # 4. Contrast enhancement using histogram stretching
            for i in range(3):
                channel = img_array[:,:,i]
                p2, p98 = np.percentile(channel, (2, 98))
                if p98 > p2:
                    img_array[:,:,i] = np.clip((channel - p2) / (p98 - p2), 0, 1)
            
            # 5. Gamma correction for better tonal range
            img_array = np.power(img_array, 0.95)
            
            # Convert back to uint8
            img_array = (img_array * 255).astype(np.uint8)
            rgb = Image.fromarray(img_array)
            
            # 6. Additional PIL enhancements for professional finish
            enhancer = ImageEnhance.Sharpness(rgb)
            rgb = enhancer.enhance(1.3)
            
            color_enhancer = ImageEnhance.Color(rgb)
            rgb = color_enhancer.enhance(1.15)
            
            contrast_enhancer = ImageEnhance.Contrast(rgb)
            rgb = contrast_enhancer.enhance(1.08)
            
            # Recombine with alpha
            rgb.putalpha(alpha)
            output_image = rgb
        
        logger.info("Professional image processing applied!")
        
        # Save to buffer with maximum quality
        output_buffer = io.BytesIO()
        output_image.save(output_buffer, format='PNG', quality=100, optimize=False)
        output_buffer.seek(0)
        
        logger.info("Background removed successfully!")
        
        # Use safe filename for attachment
        safe_output_name = f"no_bg_{safe_filename}" if safe_filename else "no_bg_image.png"
        
        return StreamingResponse(
            output_buffer,
            media_type="image/png",
            headers={"Content-Disposition": f"attachment; filename={safe_output_name}"}
        )
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/enhance-image")
async def enhance_image(file: UploadFile = File(...), scale: int = 2):
    """Enhanced image upscaling with sharpening and quality improvements"""
    try:
        contents = await file.read()
        input_image = Image.open(io.BytesIO(contents))
        
        # Check if image has transparency
        has_alpha = input_image.mode == 'RGBA'
        
        if has_alpha:
            # Separate alpha channel
            rgb_image = input_image.convert('RGB')
            alpha_channel = input_image.split()[3]
            
            # Enhance RGB
            enhanced_rgb = enhance_quality(rgb_image, scale)
            
            # Resize alpha
            new_size = enhanced_rgb.size
            alpha_resized = alpha_channel.resize(new_size, Image.LANCZOS)
            
            # Combine
            enhanced_rgb.putalpha(alpha_resized)
            output_image = enhanced_rgb
        else:
            # Regular enhancement
            output_image = enhance_quality(input_image, scale)
        
        output_buffer = io.BytesIO()
        output_image.save(output_buffer, format='PNG', quality=100)
        output_buffer.seek(0)
        
        logger.info("Image enhanced successfully!")
        
        return StreamingResponse(
            output_buffer,
            media_type="image/png",
            headers={"Content-Disposition": f"attachment; filename=enhanced_image.png"}
        )
    except Exception as e:
        logger.error(f"Enhancement error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def enhance_quality(image: Image.Image, scale: int) -> Image.Image:
    """Enhance image quality with upscaling and sharpening"""
    from PIL import ImageEnhance, ImageFilter
    
    # Upscale
    new_size = (image.width * scale, image.height * scale)
    enhanced = image.resize(new_size, Image.LANCZOS)
    
    # Apply unsharp mask for better details
    enhanced = enhanced.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    
    # Enhance sharpness
    enhancer = ImageEnhance.Sharpness(enhanced)
    enhanced = enhancer.enhance(1.3)
    
    # Enhance color
    color_enhancer = ImageEnhance.Color(enhanced)
    enhanced = color_enhancer.enhance(1.1)
    
    # Enhance contrast slightly
    contrast_enhancer = ImageEnhance.Contrast(enhanced)
    enhanced = contrast_enhancer.enhance(1.05)
    
    return enhanced

@app.post("/api/process-all")
async def process_all(
    file: UploadFile = File(...),
    remove_bg: bool = True,
    enhance: bool = True,
    scale: int = 2
):
    """Remove background and enhance"""
    try:
        contents = await file.read()
        current_image = Image.open(io.BytesIO(contents))
        
        if remove_bg and ort_session:
            current_image = remove_background_simple(current_image)
        
        if enhance:
            if current_image.mode == 'RGBA':
                rgb = current_image.convert('RGB')
                alpha = current_image.split()[3]
                
                new_size = (rgb.width * scale, rgb.height * scale)
                rgb = rgb.resize(new_size, Image.LANCZOS)
                alpha = alpha.resize(new_size, Image.LANCZOS)
                
                rgb.putalpha(alpha)
                current_image = rgb
            else:
                new_size = (current_image.width * scale, current_image.height * scale)
                current_image = current_image.resize(new_size, Image.LANCZOS)
        
        output_buffer = io.BytesIO()
        current_image.save(output_buffer, format='PNG', quality=95)
        output_buffer.seek(0)
        
        return StreamingResponse(
            output_buffer,
            media_type="image/png",
            headers={"Content-Disposition": f"attachment; filename=processed_{file.filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status")
async def get_status():
    """Get API status"""
    return {
        "api_status": "online",
        "models": {
            "u2net": "loaded" if ort_session else "not loaded",
            "enhancement": "advanced (sharpening + quality boost)"
        },
        "device": "cpu"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
