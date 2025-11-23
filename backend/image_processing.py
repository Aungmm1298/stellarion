"""
Advanced Image Processing Module
Implements histogram processing, spatial filtering, frequency domain filtering,
edge detection, and image segmentation techniques.
"""

import cv2
import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.fft import fft2, ifft2, fftshift, ifftshift
from typing import Tuple, Optional, Dict, List
import logging

logger = logging.getLogger(__name__)


# ==================== HISTOGRAM PROCESSING ====================

def histogram_equalization(image: np.ndarray, method: str = 'global') -> np.ndarray:
    """
    Perform histogram equalization to enhance contrast
    
    Args:
        image: Input image (grayscale or color)
        method: 'global', 'adaptive', or 'clahe'
        
    Returns:
        Equalized image
    """
    if len(image.shape) == 3:
        # Color image - convert to YCrCb and equalize Y channel
        ycrcb = cv2.cvtColor(image, cv2.COLOR_RGB2YCrCb)
        channels = list(cv2.split(ycrcb))
        
        if method == 'global':
            channels[0] = cv2.equalizeHist(channels[0])
        elif method == 'adaptive':
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            channels[0] = clahe.apply(channels[0])
        elif method == 'clahe':
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            channels[0] = clahe.apply(channels[0])
        
        ycrcb = cv2.merge(channels)
        return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2RGB)
    else:
        # Grayscale image
        if method == 'global':
            return cv2.equalizeHist(image)
        elif method in ['adaptive', 'clahe']:
            clip_limit = 3.0 if method == 'clahe' else 2.0
            clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
            return clahe.apply(image)
    
    return image


def histogram_matching(source: np.ndarray, reference: np.ndarray) -> np.ndarray:
    """
    Match histogram of source image to reference image
    
    Args:
        source: Source image to transform
        reference: Reference image for histogram
        
    Returns:
        Histogram-matched image
    """
    if len(source.shape) == 3:
        # Process each channel separately for color images
        result = np.zeros_like(source)
        for i in range(3):
            result[:, :, i] = _match_histograms_1d(source[:, :, i], reference[:, :, i])
        return result
    else:
        return _match_histograms_1d(source, reference)


def _match_histograms_1d(source: np.ndarray, reference: np.ndarray) -> np.ndarray:
    """Match histograms for single channel"""
    # Calculate histograms
    src_hist, _ = np.histogram(source.flatten(), 256, [0, 256])
    ref_hist, _ = np.histogram(reference.flatten(), 256, [0, 256])
    
    # Calculate CDFs
    src_cdf = src_hist.cumsum()
    src_cdf = src_cdf / src_cdf[-1]
    
    ref_cdf = ref_hist.cumsum()
    ref_cdf = ref_cdf / ref_cdf[-1]
    
    # Create lookup table
    lookup = np.zeros(256, dtype=np.uint8)
    for i in range(256):
        j = np.argmin(np.abs(src_cdf[i] - ref_cdf))
        lookup[i] = j
    
    return lookup[source]


def adjust_brightness_contrast(image: np.ndarray, brightness: int = 0, 
                               contrast: float = 1.0) -> np.ndarray:
    """
    Adjust image brightness and contrast using gray-level transformations
    
    Args:
        image: Input image
        brightness: Brightness adjustment (-100 to 100)
        contrast: Contrast adjustment (0.5 to 3.0)
        
    Returns:
        Adjusted image
    """
    adjusted = cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)
    return adjusted


def gamma_correction(image: np.ndarray, gamma: float = 1.0) -> np.ndarray:
    """
    Apply gamma correction for non-linear brightness adjustment
    
    Args:
        image: Input image
        gamma: Gamma value (< 1 brightens, > 1 darkens)
        
    Returns:
        Gamma-corrected image
    """
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 
                     for i in range(256)]).astype("uint8")
    return cv2.LUT(image, table)


# ==================== SPATIAL FILTERING ====================

def apply_mean_filter(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """
    Apply mean filter for noise reduction (smoothing)
    
    Args:
        image: Input image
        kernel_size: Size of the averaging kernel (odd number)
        
    Returns:
        Smoothed image
    """
    return cv2.blur(image, (kernel_size, kernel_size))


def apply_median_filter(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """
    Apply median filter for noise reduction (better for salt-and-pepper noise)
    
    Args:
        image: Input image
        kernel_size: Size of the median kernel (odd number)
        
    Returns:
        Smoothed image
    """
    return cv2.medianBlur(image, kernel_size)


def apply_gaussian_filter(image: np.ndarray, kernel_size: int = 5, 
                         sigma: float = 1.0) -> np.ndarray:
    """
    Apply Gaussian filter for smooth noise reduction
    
    Args:
        image: Input image
        kernel_size: Size of the Gaussian kernel (odd number)
        sigma: Standard deviation
        
    Returns:
        Smoothed image
    """
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)


def apply_bilateral_filter(image: np.ndarray, d: int = 9, 
                          sigma_color: float = 75, 
                          sigma_space: float = 75) -> np.ndarray:
    """
    Apply bilateral filter (edge-preserving smoothing)
    
    Args:
        image: Input image
        d: Diameter of pixel neighborhood
        sigma_color: Filter sigma in color space
        sigma_space: Filter sigma in coordinate space
        
    Returns:
        Smoothed image with preserved edges
    """
    return cv2.bilateralFilter(image, d, sigma_color, sigma_space)


def apply_laplacian_sharpening(image: np.ndarray, strength: float = 1.0) -> np.ndarray:
    """
    Apply Laplacian sharpening to enhance edges
    
    Args:
        image: Input image
        strength: Sharpening strength (0.5 to 2.0)
        
    Returns:
        Sharpened image
    """
    if len(image.shape) == 3:
        # Convert to grayscale for Laplacian
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        laplacian = cv2.convertScaleAbs(laplacian)
        
        # Apply to each channel
        result = image.copy().astype(np.float32)
        for i in range(3):
            result[:, :, i] = image[:, :, i] + strength * laplacian
        return np.clip(result, 0, 255).astype(np.uint8)
    else:
        laplacian = cv2.Laplacian(image, cv2.CV_64F)
        laplacian = cv2.convertScaleAbs(laplacian)
        result = image.astype(np.float32) + strength * laplacian
        return np.clip(result, 0, 255).astype(np.uint8)


def apply_unsharp_mask(image: np.ndarray, kernel_size: int = 5, 
                       sigma: float = 1.0, amount: float = 1.5, 
                       threshold: int = 0) -> np.ndarray:
    """
    Apply unsharp masking for high-quality sharpening
    
    Args:
        image: Input image
        kernel_size: Gaussian kernel size
        sigma: Gaussian sigma
        amount: Sharpening amount
        threshold: Minimum brightness change to sharpen
        
    Returns:
        Sharpened image
    """
    blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
    sharpened = cv2.addWeighted(image, 1.0 + amount, blurred, -amount, 0)
    
    if threshold > 0:
        low_contrast_mask = np.abs(image - blurred) < threshold
        sharpened[low_contrast_mask] = image[low_contrast_mask]
    
    return sharpened


def apply_highpass_filter(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """
    Apply high-pass filter to enhance edges
    
    Args:
        image: Input image
        kernel_size: Kernel size for low-pass component
        
    Returns:
        High-pass filtered image
    """
    # Create low-pass version
    lowpass = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    
    # High-pass = Original - Low-pass
    highpass = cv2.subtract(image, lowpass)
    
    # Normalize and return
    return cv2.normalize(highpass, None, 0, 255, cv2.NORM_MINMAX)


# ==================== FREQUENCY DOMAIN FILTERING ====================

def create_lowpass_filter(shape: Tuple[int, int], cutoff: float) -> np.ndarray:
    """Create ideal low-pass filter in frequency domain"""
    rows, cols = shape
    crow, ccol = rows // 2, cols // 2
    
    mask = np.zeros((rows, cols), np.float32)
    for i in range(rows):
        for j in range(cols):
            distance = np.sqrt((i - crow) ** 2 + (j - ccol) ** 2)
            if distance <= cutoff:
                mask[i, j] = 1.0
    return mask


def create_highpass_filter(shape: Tuple[int, int], cutoff: float) -> np.ndarray:
    """Create ideal high-pass filter in frequency domain"""
    return 1.0 - create_lowpass_filter(shape, cutoff)


def create_bandpass_filter(shape: Tuple[int, int], low_cutoff: float, 
                          high_cutoff: float) -> np.ndarray:
    """Create ideal band-pass filter in frequency domain"""
    rows, cols = shape
    crow, ccol = rows // 2, cols // 2
    
    mask = np.zeros((rows, cols), np.float32)
    for i in range(rows):
        for j in range(cols):
            distance = np.sqrt((i - crow) ** 2 + (j - ccol) ** 2)
            if low_cutoff <= distance <= high_cutoff:
                mask[i, j] = 1.0
    return mask


def create_butterworth_lowpass(shape: Tuple[int, int], cutoff: float, 
                               order: int = 2) -> np.ndarray:
    """Create Butterworth low-pass filter"""
    rows, cols = shape
    crow, ccol = rows // 2, cols // 2
    
    mask = np.zeros((rows, cols), np.float32)
    for i in range(rows):
        for j in range(cols):
            distance = np.sqrt((i - crow) ** 2 + (j - ccol) ** 2)
            mask[i, j] = 1.0 / (1.0 + (distance / cutoff) ** (2 * order))
    return mask


def apply_frequency_filter(image: np.ndarray, filter_type: str = 'lowpass',
                          cutoff: float = 30, order: int = 2,
                          low_cutoff: float = 20, 
                          high_cutoff: float = 60) -> np.ndarray:
    """
    Apply frequency domain filtering using Fourier Transform
    
    Args:
        image: Input image (grayscale)
        filter_type: 'lowpass', 'highpass', 'bandpass', 'butterworth_lowpass'
        cutoff: Cutoff frequency for low/high-pass
        order: Order for Butterworth filter
        low_cutoff: Low cutoff for band-pass
        high_cutoff: High cutoff for band-pass
        
    Returns:
        Filtered image
    """
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image
    
    # Apply FFT
    f_transform = np.fft.fft2(gray)
    f_shift = np.fft.fftshift(f_transform)
    
    # Create filter
    if filter_type == 'lowpass':
        filter_mask = create_lowpass_filter(gray.shape, cutoff)
    elif filter_type == 'highpass':
        filter_mask = create_highpass_filter(gray.shape, cutoff)
    elif filter_type == 'bandpass':
        filter_mask = create_bandpass_filter(gray.shape, low_cutoff, high_cutoff)
    elif filter_type == 'butterworth_lowpass':
        filter_mask = create_butterworth_lowpass(gray.shape, cutoff, order)
    else:
        filter_mask = np.ones(gray.shape)
    
    # Apply filter
    f_filtered = f_shift * filter_mask
    
    # Inverse FFT
    f_ishift = np.fft.ifftshift(f_filtered)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    
    # Normalize to 0-255
    img_back = cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    # If original was color, apply to all channels
    if len(image.shape) == 3:
        result = np.zeros_like(image)
        for i in range(3):
            f_transform = np.fft.fft2(image[:, :, i])
            f_shift = np.fft.fftshift(f_transform)
            f_filtered = f_shift * filter_mask
            f_ishift = np.fft.ifftshift(f_filtered)
            img_back = np.fft.ifft2(f_ishift)
            result[:, :, i] = np.abs(img_back)
        result = cv2.normalize(result, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        return result
    
    return img_back


# ==================== EDGE DETECTION ====================

def detect_edges_sobel(image: np.ndarray, ksize: int = 3) -> np.ndarray:
    """
    Detect edges using Sobel operator
    
    Args:
        image: Input image
        ksize: Kernel size (1, 3, 5, or 7)
        
    Returns:
        Edge-detected image
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image
    
    # Calculate gradients
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
    
    # Compute magnitude
    magnitude = np.sqrt(sobelx**2 + sobely**2)
    magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    return magnitude


def detect_edges_prewitt(image: np.ndarray) -> np.ndarray:
    """
    Detect edges using Prewitt operator
    
    Args:
        image: Input image
        
    Returns:
        Edge-detected image
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image
    
    # Prewitt kernels
    kernelx = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], dtype=np.float32)
    kernely = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.float32)
    
    # Apply filters
    prewittx = cv2.filter2D(gray, cv2.CV_64F, kernelx)
    prewitty = cv2.filter2D(gray, cv2.CV_64F, kernely)
    
    # Compute magnitude
    magnitude = np.sqrt(prewittx**2 + prewitty**2)
    magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    return magnitude


def detect_edges_canny(image: np.ndarray, threshold1: int = 50, 
                       threshold2: int = 150, aperture_size: int = 3) -> np.ndarray:
    """
    Detect edges using Canny operator
    
    Args:
        image: Input image
        threshold1: Lower threshold for hysteresis
        threshold2: Upper threshold for hysteresis
        aperture_size: Sobel kernel size (3, 5, or 7)
        
    Returns:
        Edge-detected binary image
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image
    
    edges = cv2.Canny(gray, threshold1, threshold2, apertureSize=aperture_size)
    return edges


def detect_edges_laplacian(image: np.ndarray, ksize: int = 3) -> np.ndarray:
    """
    Detect edges using Laplacian operator
    
    Args:
        image: Input image
        ksize: Kernel size
        
    Returns:
        Edge-detected image
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image
    
    laplacian = cv2.Laplacian(gray, cv2.CV_64F, ksize=ksize)
    laplacian = cv2.convertScaleAbs(laplacian)
    
    return laplacian


def compare_edge_detectors(image: np.ndarray) -> Dict[str, np.ndarray]:
    """
    Compare different edge detection methods
    
    Args:
        image: Input image
        
    Returns:
        Dictionary with edge detection results
    """
    return {
        'sobel': detect_edges_sobel(image),
        'prewitt': detect_edges_prewitt(image),
        'canny': detect_edges_canny(image),
        'laplacian': detect_edges_laplacian(image)
    }


# ==================== IMAGE SEGMENTATION ====================

def segment_otsu_threshold(image: np.ndarray) -> Tuple[np.ndarray, int]:
    """
    Segment image using Otsu's thresholding method
    
    Args:
        image: Input image
        
    Returns:
        Tuple of (segmented binary image, threshold value)
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image
    
    # Apply Otsu's thresholding
    threshold_value, binary = cv2.threshold(gray, 0, 255, 
                                           cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return binary, int(threshold_value)


def segment_adaptive_threshold(image: np.ndarray, method: str = 'gaussian',
                               block_size: int = 11, C: int = 2) -> np.ndarray:
    """
    Segment image using adaptive thresholding
    
    Args:
        image: Input image
        method: 'mean' or 'gaussian'
        block_size: Size of pixel neighborhood (odd number)
        C: Constant subtracted from mean/weighted mean
        
    Returns:
        Binary segmented image
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image
    
    adaptive_method = cv2.ADAPTIVE_THRESH_GAUSSIAN_C if method == 'gaussian' else cv2.ADAPTIVE_THRESH_MEAN_C
    
    binary = cv2.adaptiveThreshold(gray, 255, adaptive_method, 
                                   cv2.THRESH_BINARY, block_size, C)
    
    return binary


def segment_region_growing(image: np.ndarray, seed_point: Tuple[int, int],
                          threshold: int = 10) -> np.ndarray:
    """
    Segment image using region growing algorithm
    
    Args:
        image: Input grayscale image
        seed_point: (x, y) starting point
        threshold: Intensity difference threshold
        
    Returns:
        Binary segmented image
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image
    
    h, w = gray.shape
    segmented = np.zeros((h, w), dtype=np.uint8)
    
    # Check if seed point is valid
    x, y = seed_point
    if x < 0 or x >= w or y < 0 or y >= h:
        return segmented
    
    seed_value = int(gray[y, x])
    
    # Region growing using flood fill
    mask = np.zeros((h + 2, w + 2), dtype=np.uint8)
    cv2.floodFill(gray.copy(), mask, (x, y), 255, 
                  loDiff=threshold, upDiff=threshold)
    
    segmented = mask[1:-1, 1:-1]
    
    return segmented


def segment_watershed(image: np.ndarray) -> np.ndarray:
    """
    Segment image using watershed algorithm
    
    Args:
        image: Input color image
        
    Returns:
        Labeled segmentation map
    """
    if len(image.shape) == 2:
        # Convert grayscale to color for watershed
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    # Noise removal
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel, iterations=2)
    
    # Sure background area
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    
    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.5 * dist_transform.max(), 255, 0)
    
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    
    # Marker labeling
    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0
    
    # Apply watershed
    markers = cv2.watershed(image, markers)
    
    # Create visualization
    result = np.zeros_like(gray)
    result[markers > 1] = 255
    
    return result


def segment_color_based(image: np.ndarray, color_space: str = 'hsv',
                        lower_bound: Tuple = None, 
                        upper_bound: Tuple = None) -> np.ndarray:
    """
    Segment image based on color in RGB or HSV space
    
    Args:
        image: Input color image
        color_space: 'rgb' or 'hsv'
        lower_bound: Lower color bound tuple
        upper_bound: Upper color bound tuple
        
    Returns:
        Binary mask of segmented region
    """
    if color_space == 'hsv':
        converted = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        if lower_bound is None:
            lower_bound = (0, 50, 50)
        if upper_bound is None:
            upper_bound = (180, 255, 255)
    else:
        converted = image
        if lower_bound is None:
            lower_bound = (0, 0, 0)
        if upper_bound is None:
            upper_bound = (255, 255, 255)
    
    lower = np.array(lower_bound, dtype=np.uint8)
    upper = np.array(upper_bound, dtype=np.uint8)
    
    mask = cv2.inRange(converted, lower, upper)
    
    return mask


def segment_kmeans(image: np.ndarray, k: int = 3) -> np.ndarray:
    """
    Segment image using K-means clustering
    
    Args:
        image: Input image
        k: Number of clusters
        
    Returns:
        Segmented image
    """
    # Reshape image
    pixel_values = image.reshape((-1, 3 if len(image.shape) == 3 else 1))
    pixel_values = np.float32(pixel_values)
    
    # Define criteria and apply K-means
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixel_values, k, None, criteria, 10, 
                                    cv2.KMEANS_RANDOM_CENTERS)
    
    # Convert back to uint8
    centers = np.uint8(centers)
    segmented = centers[labels.flatten()]
    segmented = segmented.reshape(image.shape)
    
    return segmented


# ==================== MORPHOLOGICAL OPERATIONS ====================

def morphology_dilate(image: np.ndarray, kernel_size: int = 5, 
                     iterations: int = 1) -> np.ndarray:
    """
    Apply morphological dilation
    
    Args:
        image: Input binary/grayscale image
        kernel_size: Size of structuring element
        iterations: Number of times to apply
        
    Returns:
        Dilated image
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, 
                                       (kernel_size, kernel_size))
    dilated = cv2.dilate(image, kernel, iterations=iterations)
    return dilated


def morphology_erode(image: np.ndarray, kernel_size: int = 5,
                    iterations: int = 1) -> np.ndarray:
    """
    Apply morphological erosion
    
    Args:
        image: Input binary/grayscale image
        kernel_size: Size of structuring element
        iterations: Number of times to apply
        
    Returns:
        Eroded image
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                       (kernel_size, kernel_size))
    eroded = cv2.erode(image, kernel, iterations=iterations)
    return eroded


def morphology_opening(image: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    """
    Apply morphological opening (erosion followed by dilation)
    Removes small objects and noise
    
    Args:
        image: Input binary/grayscale image
        kernel_size: Size of structuring element
        
    Returns:
        Opened image
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                       (kernel_size, kernel_size))
    opened = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    return opened


def morphology_closing(image: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    """
    Apply morphological closing (dilation followed by erosion)
    Fills small holes and gaps
    
    Args:
        image: Input binary/grayscale image
        kernel_size: Size of structuring element
        
    Returns:
        Closed image
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                       (kernel_size, kernel_size))
    closed = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    return closed


def morphology_gradient(image: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    """
    Apply morphological gradient (dilation - erosion)
    Extracts object boundaries
    
    Args:
        image: Input binary/grayscale image
        kernel_size: Size of structuring element
        
    Returns:
        Gradient image (edges)
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                       (kernel_size, kernel_size))
    gradient = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)
    return gradient


def morphology_tophat(image: np.ndarray, kernel_size: int = 9) -> np.ndarray:
    """
    Apply morphological top-hat transform
    Extracts bright objects on dark background
    
    Args:
        image: Input grayscale image
        kernel_size: Size of structuring element
        
    Returns:
        Top-hat transformed image
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                       (kernel_size, kernel_size))
    tophat = cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernel)
    return tophat


def morphology_blackhat(image: np.ndarray, kernel_size: int = 9) -> np.ndarray:
    """
    Apply morphological black-hat transform
    Extracts dark objects on bright background
    
    Args:
        image: Input grayscale image
        kernel_size: Size of structuring element
        
    Returns:
        Black-hat transformed image
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                       (kernel_size, kernel_size))
    blackhat = cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, kernel)
    return blackhat


def apply_morphological_operations(image: np.ndarray, 
                                  operations: List[Dict]) -> np.ndarray:
    """
    Apply a sequence of morphological operations
    
    Args:
        image: Input image
        operations: List of operation dicts with 'type', 'kernel_size', etc.
        
    Returns:
        Result after all operations
    """
    result = image.copy()
    
    for op in operations:
        op_type = op.get('type', 'opening')
        kernel_size = op.get('kernel_size', 5)
        iterations = op.get('iterations', 1)
        
        if op_type == 'dilate':
            result = morphology_dilate(result, kernel_size, iterations)
        elif op_type == 'erode':
            result = morphology_erode(result, kernel_size, iterations)
        elif op_type == 'opening':
            result = morphology_opening(result, kernel_size)
        elif op_type == 'closing':
            result = morphology_closing(result, kernel_size)
        elif op_type == 'gradient':
            result = morphology_gradient(result, kernel_size)
        elif op_type == 'tophat':
            result = morphology_tophat(result, kernel_size)
        elif op_type == 'blackhat':
            result = morphology_blackhat(result, kernel_size)
    
    return result
