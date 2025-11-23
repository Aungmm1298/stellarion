from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image
import io
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Background Remover & Image Enhancer",
    description="Remove backgrounds and enhance images using AI",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "AI Background Remover API",
        "endpoints": {
            "remove_background": "/api/remove-background",
            "enhance_image": "/api/enhance-image (Coming soon - install Real-ESRGAN)",
            "process_all": "/api/process-all"
        }
    }


@app.post("/api/remove-background")
async def remove_background(
    file: UploadFile = File(...)
):
    """
    Remove background from uploaded image using rembg (U²Net)
    
    Parameters:
    - file: Image file to process
    """
    try:
        logger.info(f"Processing background removal for: {file.filename}")
        
        # Read uploaded file
        contents = await file.read()
        input_image = Image.open(io.BytesIO(contents))
        
        # Convert to RGB if necessary
        if input_image.mode != 'RGB':
            input_image = input_image.convert('RGB')
        
        # Remove background (without alpha matting to avoid numba issues)
        output_image = remove(input_image)
        
        # Convert to bytes
        output_buffer = io.BytesIO()
        output_image.save(output_buffer, format='PNG')
        output_buffer.seek(0)
        
        logger.info("Background removal completed successfully")
        
        return StreamingResponse(
            output_buffer,
            media_type="image/png",
            headers={"Content-Disposition": f"attachment; filename=no_bg_{file.filename}"}
        )
        
    except Exception as e:
        logger.error(f"Error in background removal: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


@app.post("/api/enhance-image")
async def enhance_image(
    file: UploadFile = File(...),
    scale: int = 2
):
    """
    Enhance image quality using PIL (basic upscaling)
    For advanced AI enhancement, install Real-ESRGAN dependencies
    
    Parameters:
    - file: Image file to enhance
    - scale: Upscaling factor (2 or 4, default 2)
    """
    try:
        logger.info(f"Processing basic image enhancement for: {file.filename}")
        
        # Read uploaded file
        contents = await file.read()
        input_image = Image.open(io.BytesIO(contents))
        
        # Basic upscaling with high-quality LANCZOS
        new_size = (input_image.width * scale, input_image.height * scale)
        output_image = input_image.resize(new_size, Image.LANCZOS)
        
        # Save to buffer
        output_buffer = io.BytesIO()
        output_image.save(output_buffer, format='PNG', quality=95)
        output_buffer.seek(0)
        
        logger.info("Image enhancement completed successfully")
        
        return StreamingResponse(
            output_buffer,
            media_type="image/png",
            headers={"Content-Disposition": f"attachment; filename=enhanced_{file.filename}"}
        )
        
    except Exception as e:
        logger.error(f"Error in image enhancement: {e}")
        raise HTTPException(status_code=500, detail=f"Error enhancing image: {str(e)}")


@app.post("/api/process-all")
async def process_all(
    file: UploadFile = File(...),
    remove_bg: bool = True,
    enhance: bool = True,
    scale: int = 2
):
    """
    Remove background AND enhance image in one request
    
    Parameters:
    - file: Image file to process
    - remove_bg: Remove background (default True)
    - enhance: Enhance image quality (default True)
    - scale: Enhancement scale factor (2 or 4)
    """
    try:
        logger.info(f"Processing full pipeline for: {file.filename}")
        
        # Read uploaded file
        contents = await file.read()
        current_image = Image.open(io.BytesIO(contents))
        
        # Step 1: Remove background if requested
        if remove_bg:
            logger.info("Step 1: Removing background...")
            current_image = remove(current_image)
        
        # Step 2: Basic enhancement if requested
        if enhance:
            logger.info("Step 2: Enhancing image quality...")
            
            # Handle transparency for background-removed images
            if current_image.mode == 'RGBA':
                # Split alpha channel
                rgb_image = current_image.convert('RGB')
                alpha_channel = current_image.split()[3]
                
                # Enhance RGB
                new_size = (rgb_image.width * scale, rgb_image.height * scale)
                enhanced_rgb = rgb_image.resize(new_size, Image.LANCZOS)
                
                # Resize alpha channel to match
                alpha_resized = alpha_channel.resize(new_size, Image.LANCZOS)
                
                # Combine
                enhanced_rgb.putalpha(alpha_resized)
                current_image = enhanced_rgb
            else:
                # Regular enhancement
                new_size = (current_image.width * scale, current_image.height * scale)
                current_image = current_image.resize(new_size, Image.LANCZOS)
        
        # Save final result
        output_buffer = io.BytesIO()
        current_image.save(output_buffer, format='PNG', quality=95)
        output_buffer.seek(0)
        
        logger.info("Full processing pipeline completed successfully")
        
        return StreamingResponse(
            output_buffer,
            media_type="image/png",
            headers={"Content-Disposition": f"attachment; filename=processed_{file.filename}"}
        )
        
    except Exception as e:
        logger.error(f"Error in full processing: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


@app.get("/api/status")
async def get_status():
    """Get API and model status"""
    return {
        "api_status": "online",
        "models": {
            "rembg": "available",
            "enhancement": "basic (PIL/LANCZOS)"
        },
        "device": "cpu"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
