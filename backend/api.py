"""
AI Background Remover + Real-ESRGAN Enhancement API
FastAPI backend for removing backgrounds and enhancing images with advanced AI features
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageFilter, ImageEnhance
from typing import Optional, List
import io
import torch
from rembg import remove, new_session
try:
    from basicsr.archs.rrdbnet_arch import RRDBNet
    from realesrgan import RealESRGANer
    REALESRGAN_AVAILABLE = True
except ImportError:
    REALESRGAN_AVAILABLE = False
    RRDBNet = None
    RealESRGANer = None
import cv2
import numpy as np
import logging
import os
from scipy import ndimage
from scipy.ndimage import zoom
import base64

# Import advanced image processing functions
from image_processing import (
    # Histogram processing
    histogram_equalization, histogram_matching, adjust_brightness_contrast, gamma_correction,
    # Spatial filtering
    apply_mean_filter, apply_median_filter, apply_gaussian_filter, apply_bilateral_filter,
    apply_laplacian_sharpening, apply_unsharp_mask, apply_highpass_filter,
    # Frequency domain filtering
    apply_frequency_filter,
    # Edge detection
    detect_edges_sobel, detect_edges_prewitt, detect_edges_canny, 
    detect_edges_laplacian, compare_edge_detectors,
    # Segmentation
    segment_otsu_threshold, segment_adaptive_threshold, segment_region_growing,
    segment_watershed, segment_color_based, segment_kmeans,
    # Morphological operations
    morphology_dilate, morphology_erode, morphology_opening, morphology_closing,
    morphology_gradient, morphology_tophat, morphology_blackhat,
    apply_morphological_operations
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Background Remover API", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for models
rembg_session = None
upsampler = None

@app.on_event("startup")
async def startup_event():
    """Initialize AI models on startup"""
    global rembg_session, upsampler
    
    try:
        # Initialize rembg session with U2Net model
        logger.info("Loading U2Net model for background removal...")
        rembg_session = new_session("u2net")
        logger.info("✓ U2Net model loaded successfully")
        
        # Initialize Real-ESRGAN model (optional)
        if REALESRGAN_AVAILABLE:
            logger.info("Loading Real-ESRGAN model for enhancement...")
            model_path = os.path.join(os.path.dirname(__file__), "models", "RealESRGAN_x2plus.pth")
            
            # Check if model file exists
            if not os.path.exists(model_path):
                logger.warning(f"Real-ESRGAN model not found at {model_path}")
                logger.warning("Download from: https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth")
                logger.info("API will work without enhancement feature")
                upsampler = None
            else:
                # Create RRDBNet model
                model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
                
                # Initialize upsampler
                upsampler = RealESRGANer(
                    scale=2,
                    model_path=model_path,
                    model=model,
                    tile=0,
                    tile_pad=10,
                    pre_pad=0,
                    half=False  # Set to True if you have GPU
                )
                logger.info("✓ Real-ESRGAN model loaded successfully")
        else:
            logger.warning("Real-ESRGAN not available (basicsr import failed)")
            logger.info("API will work with background removal only")
            upsampler = None
        
    except Exception as e:
        logger.error(f"Error loading models: {str(e)}")
        logger.info("API will run with limited functionality")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "AI Background Remover API",
        "version": "2.0.0",
        "models": {
            "u2net": rembg_session is not None,
            "realesrgan": upsampler is not None
        },
        "features": [
            "background_removal",
            "image_enhancement",
            "auto_crop",
            "edge_refinement",
            "smart_resize",
            "background_replacement",
            "batch_processing"
        ]
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "models_loaded": {
            "background_removal": rembg_session is not None,
            "enhancement": upsampler is not None
        }
    }

@app.get("/api/status")
async def api_status():
    """Frontend API status check"""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    enhancement_method = "Real-ESRGAN" if upsampler is not None else "Advanced (Lanczos + CLAHE)"
    
    return {
        "api_status": "online",
        "device": device,
        "models": {
            "u2net": "loaded" if rembg_session is not None else "not_loaded",
            "realesrgan": "loaded" if upsampler is not None else "not_loaded",
            "enhancement": enhancement_method
        },
        "features_available": {
            "background_removal": True,
            "enhancement": True,
            "auto_crop": True,
            "edge_refinement": True,
            "smart_resize": True,
            "background_color": True,
            "histogram_processing": True,
            "spatial_filtering": True,
            "frequency_filtering": True,
            "edge_detection": True,
            "image_segmentation": True,
            "morphological_operations": True
        },
        "histogram_methods": ["global", "adaptive", "clahe"],
        "spatial_filters": ["mean", "median", "gaussian", "bilateral", "laplacian", "unsharp", "highpass"],
        "frequency_filters": ["lowpass", "highpass", "bandpass", "butterworth_lowpass"],
        "edge_detectors": ["sobel", "prewitt", "canny", "laplacian"],
        "segmentation_methods": ["otsu", "adaptive", "color", "kmeans", "watershed"],
        "morphology_operations": ["dilate", "erode", "opening", "closing", "gradient", "tophat", "blackhat"]
    }

def remove_background(image: Image.Image) -> Image.Image:
    """
    Remove background from image using rembg with U2Net (Enhanced)
    
    Args:
        image: PIL Image object
        
    Returns:
        PIL Image with transparent background
    """
    try:
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Remove background using rembg with enhanced settings
        output = remove(
            image,
            session=rembg_session,
            alpha_matting=True,
            alpha_matting_foreground_threshold=240,
            alpha_matting_background_threshold=10,
            alpha_matting_erode_size=10
        )
        
        # Convert to RGBA if not already
        if output.mode != 'RGBA':
            output = output.convert('RGBA')
        
        return output
        
    except Exception as e:
        logger.error(f"Background removal error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Background removal failed: {str(e)}")

def refine_edges(image: Image.Image, strength: int = 3) -> Image.Image:
    """
    Refine edges using advanced AI-based edge detection and smoothing
    ENHANCED for maximum quality and clarity
    
    Args:
        image: PIL Image with alpha channel
        strength: Edge refinement strength (1-5)
        
    Returns:
        Image with refined edges
    """
    try:
        if image.mode != 'RGBA':
            return image
        
        # Convert to numpy array
        img_array = np.array(image)
        alpha = img_array[:, :, 3]
        
        # Step 1: Apply bilateral filter for edge-preserving smoothing
        alpha_smooth = cv2.bilateralFilter(alpha, 9, 75, 75)
        
        # Step 2: Apply guided filter for better edge preservation
        alpha_smooth = cv2.ximgproc.guidedFilter(alpha, alpha_smooth, radius=4, eps=50)
        
        # Step 3: Morphological operations for solid edges
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (strength, strength))
        
        # Close small holes
        alpha_closed = cv2.morphologyEx(alpha_smooth, cv2.MORPH_CLOSE, kernel)
        
        # Remove small noise
        alpha_opened = cv2.morphologyEx(alpha_closed, cv2.MORPH_OPEN, kernel)
        
        # Step 4: Final smoothing for natural edges
        alpha_final = cv2.GaussianBlur(alpha_opened, (3, 3), 0.5)
        
        # Replace alpha channel
        img_array[:, :, 3] = alpha_final
        
        return Image.fromarray(img_array, 'RGBA')
        
    except Exception as e:
        logger.error(f"Edge refinement error: {str(e)}")
        # Fallback to basic refinement
        try:
            img_array = np.array(image)
            alpha = img_array[:, :, 3]
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (strength, strength))
            alpha_closed = cv2.morphologyEx(alpha, cv2.MORPH_CLOSE, kernel)
            alpha_final = cv2.GaussianBlur(alpha_closed, (3, 3), 0)
            img_array[:, :, 3] = alpha_final
            return Image.fromarray(img_array, 'RGBA')
        except:
            return image

def auto_crop_subject(image: Image.Image, padding: int = 20) -> Image.Image:
    """
    Automatically crop to subject bounds with padding
    
    Args:
        image: PIL Image with alpha channel
        padding: Padding around subject in pixels
        
    Returns:
        Cropped image
    """
    try:
        if image.mode != 'RGBA':
            return image
        
        # Get alpha channel
        alpha = np.array(image.split()[-1])
        
        # Find non-transparent pixels
        rows = np.any(alpha > 0, axis=1)
        cols = np.any(alpha > 0, axis=0)
        
        if not rows.any() or not cols.any():
            return image
        
        # Get bounding box
        top, bottom = np.where(rows)[0][[0, -1]]
        left, right = np.where(cols)[0][[0, -1]]
        
        # Add padding
        top = max(0, top - padding)
        bottom = min(image.height, bottom + padding)
        left = max(0, left - padding)
        right = min(image.width, right + padding)
        
        # Crop
        return image.crop((left, top, right, bottom))
        
    except Exception as e:
        logger.error(f"Auto-crop error: {str(e)}")
        return image

def smart_resize(image: Image.Image, max_dimension: int = 2048) -> Image.Image:
    """
    Smart resize maintaining aspect ratio and quality
    
    Args:
        image: PIL Image
        max_dimension: Maximum width or height
        
    Returns:
        Resized image
    """
    try:
        width, height = image.size
        
        if width <= max_dimension and height <= max_dimension:
            return image
        
        # Calculate new dimensions
        if width > height:
            new_width = max_dimension
            new_height = int(height * (max_dimension / width))
        else:
            new_height = max_dimension
            new_width = int(width * (max_dimension / height))
        
        # Use LANCZOS for high-quality resizing
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
    except Exception as e:
        logger.error(f"Smart resize error: {str(e)}")
        return image

def add_background_color(image: Image.Image, color: tuple) -> Image.Image:
    """
    Add solid color background to transparent image
    
    Args:
        image: PIL Image with alpha channel
        color: RGB tuple (r, g, b)
        
    Returns:
        Image with colored background
    """
    try:
        if image.mode != 'RGBA':
            return image
        
        # Create background
        background = Image.new('RGB', image.size, color)
        
        # Composite
        background.paste(image, (0, 0), image)
        
        return background
        
    except Exception as e:
        logger.error(f"Add background error: {str(e)}")
        return image

def enhance_image(image: Image.Image) -> Image.Image:
    """
    Enhance image quality using Real-ESRGAN or fallback methods
    
    Args:
        image: PIL Image object
        
    Returns:
        Enhanced PIL Image
    """
    try:
        # Try Real-ESRGAN first if available
        if upsampler is not None:
            logger.info("Using Real-ESRGAN for enhancement")
            # Convert PIL to numpy array
            img_np = np.array(image)
            
            # Handle RGBA images
            if img_np.shape[2] == 4:
                # Separate RGB and alpha
                rgb = img_np[:, :, :3]
                alpha = img_np[:, :, 3]
                
                # Enhance RGB channels
                enhanced_rgb, _ = upsampler.enhance(rgb, outscale=2)
                
                # Resize alpha to match enhanced size
                alpha_resized = cv2.resize(alpha, (enhanced_rgb.shape[1], enhanced_rgb.shape[0]), 
                                          interpolation=cv2.INTER_LINEAR)
                
                # Combine back
                enhanced_np = np.dstack([enhanced_rgb, alpha_resized])
            else:
                # Enhance RGB image
                enhanced_np, _ = upsampler.enhance(img_np, outscale=2)
            
            # Convert back to PIL
            enhanced_image = Image.fromarray(enhanced_np)
            return enhanced_image
        
        # Fallback: Advanced AI-inspired enhancement using OpenCV and PIL
        logger.info("Using advanced fallback enhancement")
        return enhance_image_advanced(image)
        
    except Exception as e:
        logger.error(f"Enhancement error: {str(e)}")
        # Return enhanced version using fallback
        return enhance_image_advanced(image)

def enhance_image_advanced(image: Image.Image) -> Image.Image:
    """
    Advanced image enhancement without Real-ESRGAN
    Uses super-resolution techniques with OpenCV and PIL
    
    Args:
        image: PIL Image object
        
    Returns:
        Enhanced PIL Image
    """
    try:
        # Convert to numpy
        img_array = np.array(image)
        has_alpha = img_array.shape[2] == 4 if len(img_array.shape) == 3 else False
        
        # Separate alpha if present
        if has_alpha:
            rgb = img_array[:, :, :3]
            alpha = img_array[:, :, 3]
        else:
            rgb = img_array
            alpha = None
        
        # 1. Upscale using Lanczos (high-quality interpolation)
        original_size = (rgb.shape[1], rgb.shape[0])
        new_size = (original_size[0] * 2, original_size[1] * 2)
        
        # Use PIL for high-quality upscaling
        rgb_pil = Image.fromarray(rgb)
        rgb_upscaled = rgb_pil.resize(new_size, Image.Resampling.LANCZOS)
        rgb_enhanced = np.array(rgb_upscaled)
        
        # 2. Apply unsharp masking for sharpness
        gaussian = cv2.GaussianBlur(rgb_enhanced, (0, 0), 2.0)
        rgb_enhanced = cv2.addWeighted(rgb_enhanced, 1.5, gaussian, -0.5, 0)
        
        # 3. Denoise while preserving edges
        rgb_enhanced = cv2.bilateralFilter(rgb_enhanced, 9, 75, 75)
        
        # 4. Enhance details using CLAHE (Contrast Limited Adaptive Histogram Equalization)
        lab = cv2.cvtColor(rgb_enhanced, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        rgb_enhanced = cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2RGB)
        
        # 5. Enhance colors slightly
        rgb_enhanced = cv2.convertScaleAbs(rgb_enhanced, alpha=1.1, beta=5)
        
        # 6. Handle alpha channel
        if has_alpha:
            # Upscale alpha with high quality
            alpha_pil = Image.fromarray(alpha)
            alpha_upscaled = alpha_pil.resize(new_size, Image.Resampling.LANCZOS)
            alpha_enhanced = np.array(alpha_upscaled)
            
            # Combine
            enhanced_array = np.dstack([rgb_enhanced, alpha_enhanced])
        else:
            enhanced_array = rgb_enhanced
        
        # Convert back to PIL
        enhanced_image = Image.fromarray(enhanced_array.astype(np.uint8))
        
        # 7. Final PIL enhancements
        enhancer = ImageEnhance.Sharpness(enhanced_image)
        enhanced_image = enhancer.enhance(1.2)
        
        enhancer = ImageEnhance.Color(enhanced_image)
        enhanced_image = enhancer.enhance(1.05)
        
        logger.info("✓ Advanced enhancement complete")
        return enhanced_image
        
    except Exception as e:
        logger.error(f"Advanced enhancement error: {str(e)}")
        # Last resort: simple upscale
        return image.resize((image.width * 2, image.height * 2), Image.Resampling.LANCZOS)

@app.post("/process")
async def process_image(file: UploadFile = File(...)):
    """
    Main endpoint: Remove background and enhance image
    
    Args:
        file: Uploaded image file
        
    Returns:
        Processed PNG image with transparent background
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read uploaded file
        logger.info(f"Processing image: {file.filename}")
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Step 1: Remove background
        logger.info("Removing background...")
        processed_image = remove_background(image)
        logger.info("✓ Background removed")
        
        # Step 2: Enhance quality
        if upsampler is not None:
            logger.info("Enhancing image quality...")
            processed_image = enhance_image(processed_image)
            logger.info("✓ Image enhanced")
        else:
            logger.info("Skipping enhancement (model not available)")
        
        # Convert to PNG bytes
        output_buffer = io.BytesIO()
        processed_image.save(output_buffer, format='PNG', optimize=True, quality=95)
        output_buffer.seek(0)
        
        logger.info(f"✓ Processing complete for {file.filename}")
        
        # Return PNG image
        return Response(
            content=output_buffer.getvalue(),
            media_type="image/png",
            headers={
                "Content-Disposition": f'attachment; filename="processed_{file.filename}"'
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.post("/remove-background")
async def remove_background_only(
    file: UploadFile = File(...),
    refine_edges: bool = Form(True),
    auto_crop: bool = Form(False),
    edge_strength: int = Form(2)
):
    """
    Remove background with advanced options
    
    Args:
        file: Uploaded image file
        refine_edges: Apply edge refinement
        auto_crop: Auto-crop to subject
        edge_strength: Edge refinement strength (1-5)
        
    Returns:
        PNG image with transparent background
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read and process
        logger.info(f"Removing background from: {file.filename}")
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Remove background
        processed_image = remove_background(image)
        logger.info("✓ Background removed")
        
        # Apply edge refinement if requested
        if refine_edges:
            processed_image = refine_edges(processed_image, edge_strength)
            logger.info("✓ Edges refined")
        
        # Auto-crop if requested
        if auto_crop:
            processed_image = auto_crop_subject(processed_image)
            logger.info("✓ Auto-cropped")
        
        # Convert to PNG
        output_buffer = io.BytesIO()
        processed_image.save(output_buffer, format='PNG', optimize=True, quality=95)
        output_buffer.seek(0)
        
        logger.info(f"✓ Processing complete for {file.filename}")
        
        return Response(
            content=output_buffer.getvalue(),
            media_type="image/png"
        )
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/enhance-only")
async def enhance_only(file: UploadFile = File(...)):
    """
    Enhance image quality only (no background removal)
    
    Args:
        file: Uploaded image file
        
    Returns:
        Enhanced PNG image
    """
    try:
        if upsampler is None:
            raise HTTPException(status_code=503, detail="Enhancement model not available")
        
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read and process
        logger.info(f"Enhancing: {file.filename}")
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Enhance
        enhanced_image = enhance_image(image)
        
        # Convert to PNG
        output_buffer = io.BytesIO()
        enhanced_image.save(output_buffer, format='PNG', optimize=True, quality=95)
        output_buffer.seek(0)
        
        logger.info(f"✓ Enhanced {file.filename}")
        
        return Response(
            content=output_buffer.getvalue(),
            media_type="image/png"
        )
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/remove-background")
async def api_remove_background(
    file: UploadFile = File(...)
):
    """
    Enhanced background removal endpoint for frontend
    Automatically applies edge refinement and smart processing
    
    Args:
        file: Uploaded image file
        
    Returns:
        PNG image with transparent background and refined edges
    """
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        logger.info(f"Processing: {file.filename}")
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Remove background
        processed_image = remove_background(image)
        logger.info("✓ Background removed")
        
        # Apply automatic edge refinement
        processed_image = refine_edges(processed_image, strength=2)
        logger.info("✓ Edges refined")
        
        # Convert to PNG
        output_buffer = io.BytesIO()
        processed_image.save(output_buffer, format='PNG', optimize=True, quality=95)
        output_buffer.seek(0)
        
        logger.info(f"✓ Complete: {file.filename}")
        
        return Response(
            content=output_buffer.getvalue(),
            media_type="image/png"
        )
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/enhance-image")
async def api_enhance_image(file: UploadFile = File(...)):
    """
    Enhanced image quality enhancement endpoint for frontend
    
    Args:
        file: Uploaded image file
        
    Returns:
        Enhanced PNG image
    """
    try:
        if upsampler is None:
            raise HTTPException(status_code=503, detail="Enhancement model not available")
        
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        logger.info(f"Enhancing: {file.filename}")
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Enhance
        enhanced_image = enhance_image(image)
        
        # Convert to PNG
        output_buffer = io.BytesIO()
        enhanced_image.save(output_buffer, format='PNG', optimize=True, quality=95)
        output_buffer.seek(0)
        
        logger.info(f"✓ Enhanced: {file.filename}")
        
        return Response(
            content=output_buffer.getvalue(),
            media_type="image/png"
        )
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/process-advanced")
async def api_process_advanced(
    file: UploadFile = File(...),
    auto_crop: bool = Form(True),
    add_bg_color: bool = Form(False),
    bg_color: str = Form("255,255,255")
):
    """
    Advanced processing with MAXIMUM QUALITY settings
    - Enhanced edge refinement (strength 3)
    - Better alpha matting
    - Solid background removal
    - Clear, sharp resolution
    
    Args:
        file: Uploaded image file
        auto_crop: Auto-crop to subject (default: True)
        add_bg_color: Add colored background
        bg_color: Background color as "r,g,b" string
        
    Returns:
        Processed image with maximum quality
    """
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        logger.info(f"High-quality processing: {file.filename}")
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Step 1: Remove background with enhanced alpha matting
        logger.info("Step 1: Removing background (enhanced alpha matting)...")
        processed_image = remove(
            image,
            session=rembg_session,
            alpha_matting=True,
            alpha_matting_foreground_threshold=250,  # Higher for better quality
            alpha_matting_background_threshold=5,     # Lower for cleaner removal
            alpha_matting_erode_size=15               # Larger for smoother edges
        )
        if processed_image.mode != 'RGBA':
            processed_image = processed_image.convert('RGBA')
        logger.info("✓ Background removed")
        
        # Step 2: Apply MAXIMUM edge refinement (strength=3 for solid edges)
        logger.info("Step 2: Refining edges (maximum quality)...")
        processed_image = refine_edges(processed_image, strength=3)
        logger.info("✓ Edges refined")
        
        # Step 3: Auto-crop if requested
        if auto_crop:
            logger.info("Step 3: Auto-cropping subject...")
            processed_image = auto_crop_subject(processed_image, padding=30)
            logger.info("✓ Auto-cropped")
        
        # Step 4: Add background color if requested
        if add_bg_color:
            try:
                r, g, b = map(int, bg_color.split(','))
                processed_image = add_background_color(processed_image, (r, g, b))
                logger.info(f"✓ Background color added: {bg_color}")
            except:
                logger.warning("Invalid background color format")
        
        # Convert to appropriate format
        output_buffer = io.BytesIO()
        if processed_image.mode == 'RGBA':
            processed_image.save(output_buffer, format='PNG', optimize=True, quality=100)
            media_type = "image/png"
        else:
            processed_image.save(output_buffer, format='JPEG', optimize=True, quality=100)
            media_type = "image/jpeg"
        output_buffer.seek(0)
        
        logger.info(f"✓ High-quality processing complete: {file.filename}")
        logger.info(f"  Output size: {processed_image.width}x{processed_image.height}")
        
        return Response(
            content=output_buffer.getvalue(),
            media_type=media_type
        )
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/batch-process")
async def api_batch_process(files: List[UploadFile] = File(...)):
    """
    Batch process multiple images
    
    Args:
        files: List of uploaded image files
        
    Returns:
        JSON with processing results and image URLs
    """
    try:
        if len(files) > 10:
            raise HTTPException(status_code=400, detail="Maximum 10 images per batch")
        
        logger.info(f"Batch processing {len(files)} images")
        results = []
        
        for idx, file in enumerate(files):
            try:
                if not file.content_type.startswith('image/'):
                    results.append({
                        "filename": file.filename,
                        "status": "error",
                        "error": "Not an image file"
                    })
                    continue
                
                # Process image
                contents = await file.read()
                image = Image.open(io.BytesIO(contents))
                
                # Remove background with edge refinement
                processed_image = remove_background(image)
                processed_image = refine_edges(processed_image, strength=2)
                
                # Convert to PNG bytes
                output_buffer = io.BytesIO()
                processed_image.save(output_buffer, format='PNG', optimize=True, quality=95)
                output_buffer.seek(0)
                
                # For batch processing, we return base64 encoded images
                image_base64 = base64.b64encode(output_buffer.getvalue()).decode('utf-8')
                
                results.append({
                    "filename": file.filename,
                    "status": "success",
                    "image": f"data:image/png;base64,{image_base64}",
                    "width": processed_image.width,
                    "height": processed_image.height
                })
                
                logger.info(f"✓ Processed {idx + 1}/{len(files)}: {file.filename}")
                
            except Exception as e:
                logger.error(f"Error processing {file.filename}: {str(e)}")
                results.append({
                    "filename": file.filename,
                    "status": "error",
                    "error": str(e)
                })
        
        successful = sum(1 for r in results if r["status"] == "success")
        logger.info(f"✓ Batch complete: {successful}/{len(files)} successful")
        
        return JSONResponse(content={
            "total": len(files),
            "successful": successful,
            "failed": len(files) - successful,
            "results": results
        })
        
    except Exception as e:
        logger.error(f"Batch processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== HISTOGRAM PROCESSING ENDPOINTS ====================

@app.post("/api/histogram-equalization")
async def api_histogram_equalization(
    file: UploadFile = File(...),
    method: str = Form('clahe')
):
    """
    Apply histogram equalization for contrast enhancement
    
    Args:
        file: Input image
        method: 'global', 'adaptive', or 'clahe'
        
    Returns:
        Enhanced image
    """
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        logger.info(f"Applying histogram equalization ({method}): {file.filename}")
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        img_array = np.array(image)
        
        # Apply histogram equalization
        result = histogram_equalization(img_array, method=method)
        
        # Convert back to PIL
        result_image = Image.fromarray(result)
        
        # Return image
        output_buffer = io.BytesIO()
        result_image.save(output_buffer, format='PNG', optimize=True, quality=95)
        output_buffer.seek(0)
        
        logger.info(f"✓ Histogram equalization complete: {file.filename}")
        
        return Response(
            content=output_buffer.getvalue(),
            media_type="image/png"
        )
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/adjust-brightness-contrast")
async def api_adjust_brightness_contrast(
    file: UploadFile = File(...),
    brightness: int = Form(0),
    contrast: float = Form(1.0),
    gamma: float = Form(1.0)
):
    """
    Adjust image brightness, contrast, and gamma
    
    Args:
        file: Input image
        brightness: Brightness adjustment (-100 to 100)
        contrast: Contrast multiplier (0.5 to 3.0)
        gamma: Gamma correction (0.1 to 3.0)
        
    Returns:
        Adjusted image
    """
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        logger.info(f"Adjusting brightness/contrast: {file.filename}")
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        img_array = np.array(image)
        
        # Apply adjustments
        result = adjust_brightness_contrast(img_array, brightness, contrast)
        if gamma != 1.0:
            result = gamma_correction(result, gamma)
        
        # Convert back to PIL
        result_image = Image.fromarray(result)
        
        output_buffer = io.BytesIO()
        result_image.save(output_buffer, format='PNG', optimize=True, quality=95)
        output_buffer.seek(0)
        
        logger.info(f"✓ Adjustments complete: {file.filename}")
        
        return Response(
            content=output_buffer.getvalue(),
            media_type="image/png"
        )
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== SPATIAL FILTERING ENDPOINTS ====================

@app.post("/api/spatial-filter")
async def api_spatial_filter(
    file: UploadFile = File(...),
    filter_type: str = Form('gaussian'),
    kernel_size: int = Form(5),
    sigma: float = Form(1.0)
):
    """
    Apply spatial domain filters for smoothing or sharpening
    
    Args:
        file: Input image
        filter_type: 'mean', 'median', 'gaussian', 'bilateral', 'laplacian', 'unsharp', 'highpass'
        kernel_size: Kernel size (odd number)
        sigma: Sigma value for Gaussian filter
        
    Returns:
        Filtered image
    """
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        logger.info(f"Applying {filter_type} filter: {file.filename}")
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        img_array = np.array(image)
        
        # Apply filter
        if filter_type == 'mean':
            result = apply_mean_filter(img_array, kernel_size)
        elif filter_type == 'median':
            result = apply_median_filter(img_array, kernel_size)
        elif filter_type == 'gaussian':
            result = apply_gaussian_filter(img_array, kernel_size, sigma)
        elif filter_type == 'bilateral':
            result = apply_bilateral_filter(img_array)
        elif filter_type == 'laplacian':
            result = apply_laplacian_sharpening(img_array)
        elif filter_type == 'unsharp':
            result = apply_unsharp_mask(img_array, kernel_size, sigma)
        elif filter_type == 'highpass':
            result = apply_highpass_filter(img_array, kernel_size)
        else:
            raise HTTPException(status_code=400, detail="Invalid filter type")
        
        # Convert back to PIL
        result_image = Image.fromarray(result)
        
        output_buffer = io.BytesIO()
        result_image.save(output_buffer, format='PNG', optimize=True, quality=95)
        output_buffer.seek(0)
        
        logger.info(f"✓ Filter applied: {file.filename}")
        
        return Response(
            content=output_buffer.getvalue(),
            media_type="image/png"
        )
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== FREQUENCY DOMAIN FILTERING ENDPOINTS ====================

@app.post("/api/frequency-filter")
async def api_frequency_filter(
    file: UploadFile = File(...),
    filter_type: str = Form('lowpass'),
    cutoff: float = Form(30.0),
    order: int = Form(2),
    low_cutoff: float = Form(20.0),
    high_cutoff: float = Form(60.0)
):
    """
    Apply frequency domain filtering using Fourier Transform
    
    Args:
        file: Input image
        filter_type: 'lowpass', 'highpass', 'bandpass', 'butterworth_lowpass'
        cutoff: Cutoff frequency for low/high-pass
        order: Order for Butterworth filter
        low_cutoff: Low cutoff for band-pass
        high_cutoff: High cutoff for band-pass
        
    Returns:
        Filtered image
    """
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        logger.info(f"Applying {filter_type} frequency filter: {file.filename}")
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        img_array = np.array(image)
        
        # Apply frequency filter
        result = apply_frequency_filter(img_array, filter_type, cutoff, order, 
                                       low_cutoff, high_cutoff)
        
        # Convert back to PIL
        result_image = Image.fromarray(result)
        
        output_buffer = io.BytesIO()
        result_image.save(output_buffer, format='PNG', optimize=True, quality=95)
        output_buffer.seek(0)
        
        logger.info(f"✓ Frequency filter applied: {file.filename}")
        
        return Response(
            content=output_buffer.getvalue(),
            media_type="image/png"
        )
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== EDGE DETECTION ENDPOINTS ====================

@app.post("/api/edge-detection")
async def api_edge_detection(
    file: UploadFile = File(...),
    method: str = Form('canny'),
    threshold1: int = Form(50),
    threshold2: int = Form(150),
    kernel_size: int = Form(3)
):
    """
    Detect edges using various operators
    
    Args:
        file: Input image
        method: 'sobel', 'prewitt', 'canny', 'laplacian'
        threshold1: Lower threshold (for Canny)
        threshold2: Upper threshold (for Canny)
        kernel_size: Kernel size
        
    Returns:
        Edge-detected image
    """
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        logger.info(f"Detecting edges ({method}): {file.filename}")
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        img_array = np.array(image)
        
        # Apply edge detection
        if method == 'sobel':
            result = detect_edges_sobel(img_array, kernel_size)
        elif method == 'prewitt':
            result = detect_edges_prewitt(img_array)
        elif method == 'canny':
            result = detect_edges_canny(img_array, threshold1, threshold2, kernel_size)
        elif method == 'laplacian':
            result = detect_edges_laplacian(img_array, kernel_size)
        else:
            raise HTTPException(status_code=400, detail="Invalid edge detection method")
        
        # Convert back to PIL
        result_image = Image.fromarray(result)
        
        output_buffer = io.BytesIO()
        result_image.save(output_buffer, format='PNG', optimize=True, quality=95)
        output_buffer.seek(0)
        
        logger.info(f"✓ Edge detection complete: {file.filename}")
        
        return Response(
            content=output_buffer.getvalue(),
            media_type="image/png"
        )
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/compare-edge-detectors")
async def api_compare_edge_detectors(file: UploadFile = File(...)):
    """
    Compare different edge detection methods
    
    Args:
        file: Input image
        
    Returns:
        JSON with base64-encoded results for each method
    """
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        logger.info(f"Comparing edge detectors: {file.filename}")
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        img_array = np.array(image)
        
        # Get all edge detection results
        results_dict = compare_edge_detectors(img_array)
        
        # Convert to base64
        encoded_results = {}
        for method, result_array in results_dict.items():
            result_image = Image.fromarray(result_array)
            buffer = io.BytesIO()
            result_image.save(buffer, format='PNG')
            buffer.seek(0)
            encoded = base64.b64encode(buffer.getvalue()).decode('utf-8')
            encoded_results[method] = f"data:image/png;base64,{encoded}"
        
        logger.info(f"✓ Edge detector comparison complete: {file.filename}")
        
        return JSONResponse(content={
            "filename": file.filename,
            "results": encoded_results
        })
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== SEGMENTATION ENDPOINTS ====================

@app.post("/api/segment-threshold")
async def api_segment_threshold(
    file: UploadFile = File(...),
    method: str = Form('otsu'),
    block_size: int = Form(11),
    C: int = Form(2)
):
    """
    Segment image using thresholding methods
    
    Args:
        file: Input image
        method: 'otsu' or 'adaptive'
        block_size: Block size for adaptive threshold
        C: Constant for adaptive threshold
        
    Returns:
        Binary segmented image
    """
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        logger.info(f"Segmenting with {method} threshold: {file.filename}")
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        img_array = np.array(image)
        
        # Apply segmentation
        if method == 'otsu':
            result, threshold_value = segment_otsu_threshold(img_array)
            logger.info(f"Otsu threshold value: {threshold_value}")
        elif method == 'adaptive':
            result = segment_adaptive_threshold(img_array, 'gaussian', block_size, C)
        else:
            raise HTTPException(status_code=400, detail="Invalid threshold method")
        
        # Convert back to PIL
        result_image = Image.fromarray(result)
        
        output_buffer = io.BytesIO()
        result_image.save(output_buffer, format='PNG', optimize=True, quality=95)
        output_buffer.seek(0)
        
        logger.info(f"✓ Segmentation complete: {file.filename}")
        
        return Response(
            content=output_buffer.getvalue(),
            media_type="image/png"
        )
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/segment-color")
async def api_segment_color(
    file: UploadFile = File(...),
    color_space: str = Form('hsv'),
    lower_h: int = Form(0),
    lower_s: int = Form(50),
    lower_v: int = Form(50),
    upper_h: int = Form(180),
    upper_s: int = Form(255),
    upper_v: int = Form(255)
):
    """
    Segment image based on color in RGB or HSV space
    
    Args:
        file: Input image
        color_space: 'rgb' or 'hsv'
        lower_h, lower_s, lower_v: Lower bounds
        upper_h, upper_s, upper_v: Upper bounds
        
    Returns:
        Binary mask of segmented region
    """
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        logger.info(f"Color-based segmentation ({color_space}): {file.filename}")
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        img_array = np.array(image)
        
        # Apply color segmentation
        lower_bound = (lower_h, lower_s, lower_v)
        upper_bound = (upper_h, upper_s, upper_v)
        result = segment_color_based(img_array, color_space, lower_bound, upper_bound)
        
        # Convert back to PIL
        result_image = Image.fromarray(result)
        
        output_buffer = io.BytesIO()
        result_image.save(output_buffer, format='PNG', optimize=True, quality=95)
        output_buffer.seek(0)
        
        logger.info(f"✓ Color segmentation complete: {file.filename}")
        
        return Response(
            content=output_buffer.getvalue(),
            media_type="image/png"
        )
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/segment-kmeans")
async def api_segment_kmeans(
    file: UploadFile = File(...),
    k: int = Form(3)
):
    """
    Segment image using K-means clustering
    
    Args:
        file: Input image
        k: Number of clusters
        
    Returns:
        Segmented image
    """
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        logger.info(f"K-means segmentation (k={k}): {file.filename}")
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        img_array = np.array(image)
        
        # Apply K-means segmentation
        result = segment_kmeans(img_array, k)
        
        # Convert back to PIL
        result_image = Image.fromarray(result)
        
        output_buffer = io.BytesIO()
        result_image.save(output_buffer, format='PNG', optimize=True, quality=95)
        output_buffer.seek(0)
        
        logger.info(f"✓ K-means segmentation complete: {file.filename}")
        
        return Response(
            content=output_buffer.getvalue(),
            media_type="image/png"
        )
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/segment-watershed")
async def api_segment_watershed(file: UploadFile = File(...)):
    """
    Segment image using watershed algorithm
    
    Args:
        file: Input image
        
    Returns:
        Segmented image
    """
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        logger.info(f"Watershed segmentation: {file.filename}")
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        img_array = np.array(image)
        
        # Apply watershed segmentation
        result = segment_watershed(img_array)
        
        # Convert back to PIL
        result_image = Image.fromarray(result)
        
        output_buffer = io.BytesIO()
        result_image.save(output_buffer, format='PNG', optimize=True, quality=95)
        output_buffer.seek(0)
        
        logger.info(f"✓ Watershed segmentation complete: {file.filename}")
        
        return Response(
            content=output_buffer.getvalue(),
            media_type="image/png"
        )
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== MORPHOLOGICAL OPERATIONS ENDPOINTS ====================

@app.post("/api/morphology")
async def api_morphology(
    file: UploadFile = File(...),
    operation: str = Form('opening'),
    kernel_size: int = Form(5),
    iterations: int = Form(1)
):
    """
    Apply morphological operations
    
    Args:
        file: Input image
        operation: 'dilate', 'erode', 'opening', 'closing', 'gradient', 'tophat', 'blackhat'
        kernel_size: Size of structuring element
        iterations: Number of iterations (for dilate/erode)
        
    Returns:
        Morphologically processed image
    """
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        logger.info(f"Applying {operation} morphology: {file.filename}")
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        img_array = np.array(image)
        
        # Convert to grayscale if needed for morphology
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        # Apply morphological operation
        if operation == 'dilate':
            result = morphology_dilate(gray, kernel_size, iterations)
        elif operation == 'erode':
            result = morphology_erode(gray, kernel_size, iterations)
        elif operation == 'opening':
            result = morphology_opening(gray, kernel_size)
        elif operation == 'closing':
            result = morphology_closing(gray, kernel_size)
        elif operation == 'gradient':
            result = morphology_gradient(gray, kernel_size)
        elif operation == 'tophat':
            result = morphology_tophat(gray, kernel_size)
        elif operation == 'blackhat':
            result = morphology_blackhat(gray, kernel_size)
        else:
            raise HTTPException(status_code=400, detail="Invalid morphological operation")
        
        # Convert back to PIL
        result_image = Image.fromarray(result)
        
        output_buffer = io.BytesIO()
        result_image.save(output_buffer, format='PNG', optimize=True, quality=95)
        output_buffer.seek(0)
        
        logger.info(f"✓ Morphology complete: {file.filename}")
        
        return Response(
            content=output_buffer.getvalue(),
            media_type="image/png"
        )
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
