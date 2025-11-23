"""
Test Script for Advanced Image Processing API
Tests all new endpoints to verify functionality
"""

import requests
import os
from PIL import Image
import io

API_BASE = "http://localhost:8000"

def test_api_status():
    """Test if API is online and check available features"""
    print("🔍 Testing API Status...")
    try:
        response = requests.get(f"{API_BASE}/api/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ API Status: {data['api_status']}")
            print(f"✓ Device: {data['device']}")
            print(f"✓ Models: {data['models']}")
            print(f"✓ Features Available: {len(data['features_available'])} features")
            return True
        else:
            print(f"✗ API returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error connecting to API: {e}")
        return False

def create_test_image():
    """Create a simple test image"""
    img = Image.new('RGB', (200, 200), color='white')
    # Add some patterns
    pixels = img.load()
    for i in range(50, 150):
        for j in range(50, 150):
            pixels[i, j] = (100, 100, 100)
    
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer

def test_histogram_equalization():
    """Test histogram equalization endpoint"""
    print("\n📊 Testing Histogram Equalization...")
    try:
        img_buffer = create_test_image()
        files = {'file': ('test.png', img_buffer, 'image/png')}
        data = {'method': 'clahe'}
        
        response = requests.post(f"{API_BASE}/api/histogram-equalization", 
                               files=files, data=data)
        
        if response.status_code == 200:
            print("✓ Histogram equalization successful")
            return True
        else:
            print(f"✗ Failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_brightness_contrast():
    """Test brightness/contrast adjustment"""
    print("\n💡 Testing Brightness/Contrast Adjustment...")
    try:
        img_buffer = create_test_image()
        files = {'file': ('test.png', img_buffer, 'image/png')}
        data = {
            'brightness': 20,
            'contrast': 1.5,
            'gamma': 1.0
        }
        
        response = requests.post(f"{API_BASE}/api/adjust-brightness-contrast",
                               files=files, data=data)
        
        if response.status_code == 200:
            print("✓ Brightness/contrast adjustment successful")
            return True
        else:
            print(f"✗ Failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_spatial_filter():
    """Test spatial filtering"""
    print("\n🔲 Testing Spatial Filter...")
    try:
        img_buffer = create_test_image()
        files = {'file': ('test.png', img_buffer, 'image/png')}
        data = {
            'filter_type': 'gaussian',
            'kernel_size': 5,
            'sigma': 1.0
        }
        
        response = requests.post(f"{API_BASE}/api/spatial-filter",
                               files=files, data=data)
        
        if response.status_code == 200:
            print("✓ Spatial filter successful")
            return True
        else:
            print(f"✗ Failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_frequency_filter():
    """Test frequency domain filtering"""
    print("\n🌊 Testing Frequency Domain Filter...")
    try:
        img_buffer = create_test_image()
        files = {'file': ('test.png', img_buffer, 'image/png')}
        data = {
            'filter_type': 'lowpass',
            'cutoff': 30,
            'order': 2,
            'low_cutoff': 20,
            'high_cutoff': 60
        }
        
        response = requests.post(f"{API_BASE}/api/frequency-filter",
                               files=files, data=data)
        
        if response.status_code == 200:
            print("✓ Frequency filter successful")
            return True
        else:
            print(f"✗ Failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_edge_detection():
    """Test edge detection"""
    print("\n🔍 Testing Edge Detection...")
    try:
        img_buffer = create_test_image()
        files = {'file': ('test.png', img_buffer, 'image/png')}
        data = {
            'method': 'canny',
            'threshold1': 50,
            'threshold2': 150,
            'kernel_size': 3
        }
        
        response = requests.post(f"{API_BASE}/api/edge-detection",
                               files=files, data=data)
        
        if response.status_code == 200:
            print("✓ Edge detection successful")
            return True
        else:
            print(f"✗ Failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_compare_edge_detectors():
    """Test edge detector comparison"""
    print("\n🔍 Testing Edge Detector Comparison...")
    try:
        img_buffer = create_test_image()
        files = {'file': ('test.png', img_buffer, 'image/png')}
        
        response = requests.post(f"{API_BASE}/api/compare-edge-detectors",
                               files=files)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Edge detector comparison successful")
            print(f"  Methods compared: {list(data['results'].keys())}")
            return True
        else:
            print(f"✗ Failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_segmentation():
    """Test image segmentation"""
    print("\n🎯 Testing Image Segmentation...")
    try:
        img_buffer = create_test_image()
        files = {'file': ('test.png', img_buffer, 'image/png')}
        data = {
            'method': 'otsu',
            'block_size': 11,
            'C': 2
        }
        
        response = requests.post(f"{API_BASE}/api/segment-threshold",
                               files=files, data=data)
        
        if response.status_code == 200:
            print("✓ Segmentation successful")
            return True
        else:
            print(f"✗ Failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_kmeans_segmentation():
    """Test K-means segmentation"""
    print("\n🎯 Testing K-Means Segmentation...")
    try:
        img_buffer = create_test_image()
        files = {'file': ('test.png', img_buffer, 'image/png')}
        data = {'k': 3}
        
        response = requests.post(f"{API_BASE}/api/segment-kmeans",
                               files=files, data=data)
        
        if response.status_code == 200:
            print("✓ K-means segmentation successful")
            return True
        else:
            print(f"✗ Failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_morphology():
    """Test morphological operations"""
    print("\n🔷 Testing Morphological Operations...")
    try:
        img_buffer = create_test_image()
        files = {'file': ('test.png', img_buffer, 'image/png')}
        data = {
            'operation': 'opening',
            'kernel_size': 5,
            'iterations': 1
        }
        
        response = requests.post(f"{API_BASE}/api/morphology",
                               files=files, data=data)
        
        if response.status_code == 200:
            print("✓ Morphological operation successful")
            return True
        else:
            print(f"✗ Failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def run_all_tests():
    """Run all API tests"""
    print("=" * 60)
    print("🧪 Advanced Image Processing API Test Suite")
    print("=" * 60)
    
    # Check API status first
    if not test_api_status():
        print("\n❌ API is not available. Please start the backend server first.")
        print("   Run: cd backend && python main.py")
        return
    
    # Run all tests
    tests = [
        test_histogram_equalization,
        test_brightness_contrast,
        test_spatial_filter,
        test_frequency_filter,
        test_edge_detection,
        test_compare_edge_detectors,
        test_segmentation,
        test_kmeans_segmentation,
        test_morphology
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    print(f"Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n✅ All tests passed! API is fully functional.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the output above for details.")
    
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()
