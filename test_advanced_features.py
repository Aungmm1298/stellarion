"""
Test script for advanced image processing features
Demonstrates histogram processing, filtering, edge detection, and segmentation
"""

import requests
import base64
from pathlib import Path

# Backend URL
BASE_URL = "http://localhost:8000"

def test_api_status():
    """Check API status and available features"""
    print("=" * 60)
    print("Testing API Status")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/api/status")
    data = response.json()
    
    print(f"\nAPI Status: {data['api_status']}")
    print(f"Device: {data['device']}")
    print(f"\nModels Loaded:")
    for model, status in data['models'].items():
        print(f"  - {model}: {status}")
    
    print(f"\nFeatures Available:")
    for feature, available in data['features_available'].items():
        status = "✓" if available else "✗"
        print(f"  {status} {feature}")
    
    print(f"\nHistogram Methods: {', '.join(data['histogram_methods'])}")
    print(f"Spatial Filters: {', '.join(data['spatial_filters'])}")
    print(f"Frequency Filters: {', '.join(data['frequency_filters'])}")
    print(f"Edge Detectors: {', '.join(data['edge_detectors'])}")
    print(f"Segmentation Methods: {', '.join(data['segmentation_methods'])}")
    print(f"Morphology Operations: {', '.join(data['morphology_operations'])}")


def test_histogram_equalization(image_path):
    """Test histogram equalization"""
    print("\n" + "=" * 60)
    print("Testing Histogram Equalization (CLAHE)")
    print("=" * 60)
    
    with open(image_path, 'rb') as f:
        response = requests.post(
            f"{BASE_URL}/api/histogram-equalization",
            files={'file': f},
            data={'method': 'clahe'}
        )
    
    if response.status_code == 200:
        output_path = "output_histogram_equalized.png"
        with open(output_path, 'wb') as out:
            out.write(response.content)
        print(f"✓ Histogram equalization successful")
        print(f"  Output saved to: {output_path}")
    else:
        print(f"✗ Error: {response.status_code}")


def test_edge_detection(image_path):
    """Test edge detection with Canny"""
    print("\n" + "=" * 60)
    print("Testing Edge Detection (Canny)")
    print("=" * 60)
    
    with open(image_path, 'rb') as f:
        response = requests.post(
            f"{BASE_URL}/api/edge-detection",
            files={'file': f},
            data={
                'method': 'canny',
                'threshold1': 50,
                'threshold2': 150,
                'kernel_size': 3
            }
        )
    
    if response.status_code == 200:
        output_path = "output_canny_edges.png"
        with open(output_path, 'wb') as out:
            out.write(response.content)
        print(f"✓ Edge detection successful")
        print(f"  Output saved to: {output_path}")
    else:
        print(f"✗ Error: {response.status_code}")


def test_compare_edge_detectors(image_path):
    """Compare different edge detection methods"""
    print("\n" + "=" * 60)
    print("Testing Edge Detector Comparison")
    print("=" * 60)
    
    with open(image_path, 'rb') as f:
        response = requests.post(
            f"{BASE_URL}/api/compare-edge-detectors",
            files={'file': f}
        )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Comparison successful")
        print(f"  Methods compared: {', '.join(data['results'].keys())}")
        
        # Save each result
        for method, base64_data in data['results'].items():
            # Extract base64 part
            image_data = base64_data.split(',')[1]
            image_bytes = base64.b64decode(image_data)
            
            output_path = f"output_edge_{method}.png"
            with open(output_path, 'wb') as out:
                out.write(image_bytes)
            print(f"  - {method} saved to: {output_path}")
    else:
        print(f"✗ Error: {response.status_code}")


def test_spatial_filter(image_path):
    """Test spatial filtering (Gaussian blur)"""
    print("\n" + "=" * 60)
    print("Testing Spatial Filter (Gaussian Blur)")
    print("=" * 60)
    
    with open(image_path, 'rb') as f:
        response = requests.post(
            f"{BASE_URL}/api/spatial-filter",
            files={'file': f},
            data={
                'filter_type': 'gaussian',
                'kernel_size': 7,
                'sigma': 2.0
            }
        )
    
    if response.status_code == 200:
        output_path = "output_gaussian_blur.png"
        with open(output_path, 'wb') as out:
            out.write(response.content)
        print(f"✓ Gaussian filter successful")
        print(f"  Output saved to: {output_path}")
    else:
        print(f"✗ Error: {response.status_code}")


def test_frequency_filter(image_path):
    """Test frequency domain filtering"""
    print("\n" + "=" * 60)
    print("Testing Frequency Filter (High-Pass)")
    print("=" * 60)
    
    with open(image_path, 'rb') as f:
        response = requests.post(
            f"{BASE_URL}/api/frequency-filter",
            files={'file': f},
            data={
                'filter_type': 'highpass',
                'cutoff': 30.0
            }
        )
    
    if response.status_code == 200:
        output_path = "output_highpass_filter.png"
        with open(output_path, 'wb') as out:
            out.write(response.content)
        print(f"✓ High-pass filter successful")
        print(f"  Output saved to: {output_path}")
    else:
        print(f"✗ Error: {response.status_code}")


def test_segmentation_otsu(image_path):
    """Test Otsu thresholding segmentation"""
    print("\n" + "=" * 60)
    print("Testing Segmentation (Otsu's Method)")
    print("=" * 60)
    
    with open(image_path, 'rb') as f:
        response = requests.post(
            f"{BASE_URL}/api/segment-threshold",
            files={'file': f},
            data={'method': 'otsu'}
        )
    
    if response.status_code == 200:
        output_path = "output_otsu_segmentation.png"
        with open(output_path, 'wb') as out:
            out.write(response.content)
        print(f"✓ Otsu segmentation successful")
        print(f"  Output saved to: {output_path}")
    else:
        print(f"✗ Error: {response.status_code}")


def test_segmentation_kmeans(image_path):
    """Test K-means clustering segmentation"""
    print("\n" + "=" * 60)
    print("Testing Segmentation (K-means, k=4)")
    print("=" * 60)
    
    with open(image_path, 'rb') as f:
        response = requests.post(
            f"{BASE_URL}/api/segment-kmeans",
            files={'file': f},
            data={'k': 4}
        )
    
    if response.status_code == 200:
        output_path = "output_kmeans_segmentation.png"
        with open(output_path, 'wb') as out:
            out.write(response.content)
        print(f"✓ K-means segmentation successful")
        print(f"  Output saved to: {output_path}")
    else:
        print(f"✗ Error: {response.status_code}")


def test_morphology(image_path):
    """Test morphological operations"""
    print("\n" + "=" * 60)
    print("Testing Morphological Operations (Opening)")
    print("=" * 60)
    
    with open(image_path, 'rb') as f:
        response = requests.post(
            f"{BASE_URL}/api/morphology",
            files={'file': f},
            data={
                'operation': 'opening',
                'kernel_size': 5
            }
        )
    
    if response.status_code == 200:
        output_path = "output_morphology_opening.png"
        with open(output_path, 'wb') as out:
            out.write(response.content)
        print(f"✓ Morphological opening successful")
        print(f"  Output saved to: {output_path}")
    else:
        print(f"✗ Error: {response.status_code}")


def test_brightness_contrast(image_path):
    """Test brightness and contrast adjustment"""
    print("\n" + "=" * 60)
    print("Testing Brightness/Contrast Adjustment")
    print("=" * 60)
    
    with open(image_path, 'rb') as f:
        response = requests.post(
            f"{BASE_URL}/api/adjust-brightness-contrast",
            files={'file': f},
            data={
                'brightness': 20,
                'contrast': 1.3,
                'gamma': 1.2
            }
        )
    
    if response.status_code == 200:
        output_path = "output_brightness_contrast.png"
        with open(output_path, 'wb') as out:
            out.write(response.content)
        print(f"✓ Brightness/contrast adjustment successful")
        print(f"  Output saved to: {output_path}")
    else:
        print(f"✗ Error: {response.status_code}")


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("ADVANCED IMAGE PROCESSING FEATURE TESTS")
    print("=" * 60)
    
    # Check API status first
    test_api_status()
    
    # Check if test image exists
    test_image = "test_image.jpg"
    if not Path(test_image).exists():
        print(f"\n\n⚠ Test image '{test_image}' not found!")
        print("Please place a test image named 'test_image.jpg' in the current directory.")
        print("\nAlternatively, you can test the API using:")
        print("  - The frontend interface at http://127.0.0.1:5500")
        print("  - API documentation at http://localhost:8000/docs")
        print("  - cURL commands (see ADVANCED_IMAGE_PROCESSING.md)")
        return
    
    # Run all feature tests
    test_histogram_equalization(test_image)
    test_brightness_contrast(test_image)
    test_spatial_filter(test_image)
    test_frequency_filter(test_image)
    test_edge_detection(test_image)
    test_compare_edge_detectors(test_image)
    test_segmentation_otsu(test_image)
    test_segmentation_kmeans(test_image)
    test_morphology(test_image)
    
    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)
    print("\nCheck the output files in the current directory.")
    print("For more information, see ADVANCED_IMAGE_PROCESSING.md")


if __name__ == "__main__":
    main()
