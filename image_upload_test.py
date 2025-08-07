#!/usr/bin/env python3
"""
Comprehensive Image Upload and Static File Serving Test
Tests the specific issue reported by the user about images not displaying
"""

import requests
import json
from datetime import datetime

def test_image_upload_functionality():
    """Test image upload functionality and static file serving"""
    base_url = "https://c393639a-fa64-415c-a2dd-ed9a85a0a9dc.preview.emergentagent.com"
    api_url = f"{base_url}/api"
    
    print("🔍 COMPREHENSIVE IMAGE UPLOAD TEST")
    print("=" * 60)
    print(f"Testing against: {base_url}")
    print(f"API endpoint: {api_url}")
    print()
    
    # Test 1: Get uploaded images from database
    print("1️⃣ Testing GET /api/uploaded-images endpoint")
    try:
        response = requests.get(f"{api_url}/uploaded-images")
        if response.status_code == 200:
            images = response.json()
            print(f"✅ SUCCESS: Retrieved {len(images)} images from database")
            
            if images:
                print("\n📋 Image URLs stored in database:")
                for i, img in enumerate(images, 1):
                    print(f"   {i}. {img['url']}")
                    print(f"      Filename: {img['filename']}")
                    print(f"      Original: {img['original_filename']}")
                    print(f"      Size: {img['size']} bytes")
                    print()
            else:
                print("ℹ️  No images found in database")
        else:
            print(f"❌ FAILED: HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"❌ FAILED: {e}")
    
    print("\n" + "=" * 60)
    
    # Test 2: Test direct image URL access
    print("2️⃣ Testing direct image URL access")
    try:
        response = requests.get(f"{api_url}/uploaded-images")
        if response.status_code == 200:
            images = response.json()
            
            if images:
                for i, img in enumerate(images[:3], 1):  # Test first 3 images
                    print(f"\n🖼️  Testing image {i}: {img['filename']}")
                    image_url = img['url']
                    
                    try:
                        img_response = requests.get(image_url, timeout=10)
                        print(f"   Status: {img_response.status_code}")
                        print(f"   Content-Type: {img_response.headers.get('content-type', 'N/A')}")
                        print(f"   Content-Length: {img_response.headers.get('content-length', 'N/A')}")
                        
                        if img_response.status_code == 200:
                            content_type = img_response.headers.get('content-type', '')
                            if content_type.startswith('image/'):
                                print("   ✅ SUCCESS: Image accessible and correct content type")
                            else:
                                print(f"   ❌ ISSUE: Wrong content type - expected image/*, got {content_type}")
                                # Show first 100 chars of response
                                content_preview = img_response.text[:100] if hasattr(img_response, 'text') else str(img_response.content[:100])
                                print(f"   Content preview: {content_preview}")
                        else:
                            print(f"   ❌ FAILED: HTTP {img_response.status_code}")
                    except Exception as e:
                        print(f"   ❌ ERROR: {e}")
            else:
                print("ℹ️  No images to test")
    except Exception as e:
        print(f"❌ FAILED: {e}")
    
    print("\n" + "=" * 60)
    
    # Test 3: Test static file serving at /uploads
    print("3️⃣ Testing static file serving at /uploads")
    
    # Test the uploads directory directly
    uploads_url = f"{base_url}/uploads/"
    try:
        response = requests.get(uploads_url)
        print(f"Testing {uploads_url}")
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type', 'N/A')}")
        
        if response.status_code == 200:
            content_preview = response.text[:200] if hasattr(response, 'text') else str(response.content[:200])
            print(f"Content preview: {content_preview}")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print("\n" + "=" * 60)
    
    # Test 4: Test specific image file access
    print("4️⃣ Testing specific image file access")
    
    # Test a known image file
    test_image_url = f"{base_url}/uploads/370fb168-5397-4092-b453-61306530f7ef.png"
    try:
        print(f"Testing: {test_image_url}")
        response = requests.get(test_image_url)
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type', 'N/A')}")
        print(f"Content-Length: {response.headers.get('content-length', 'N/A')}")
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            if content_type.startswith('image/'):
                print("✅ SUCCESS: Image file accessible with correct content type")
            else:
                print(f"❌ ISSUE: Wrong content type - expected image/*, got {content_type}")
                content_preview = response.text[:100] if hasattr(response, 'text') else str(response.content[:100])
                print(f"Content preview: {content_preview}")
        else:
            print(f"❌ FAILED: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY AND DIAGNOSIS")
    print("=" * 60)
    
    # Get current images for final analysis
    try:
        response = requests.get(f"{api_url}/uploaded-images")
        if response.status_code == 200:
            images = response.json()
            
            print(f"✅ Database contains {len(images)} images")
            
            if images:
                # Check URL patterns
                localhost_urls = [img for img in images if 'localhost' in img['url']]
                external_urls = [img for img in images if 'localhost' not in img['url']]
                
                print(f"📊 URL Analysis:")
                print(f"   - Images with localhost URLs: {len(localhost_urls)}")
                print(f"   - Images with external URLs: {len(external_urls)}")
                
                if localhost_urls:
                    print("❌ ISSUE FOUND: Some images have localhost URLs that frontend cannot access")
                    print("   These images will appear as gray boxes in the frontend")
                
                if external_urls:
                    print("✅ Some images have correct external URLs")
                    
                    # Test if external URLs work
                    working_external = 0
                    for img in external_urls[:3]:
                        try:
                            test_response = requests.get(img['url'], timeout=5)
                            if test_response.status_code == 200 and test_response.headers.get('content-type', '').startswith('image/'):
                                working_external += 1
                        except:
                            pass
                    
                    if working_external == 0:
                        print("❌ CRITICAL ISSUE: External URLs are not serving images correctly")
                        print("   This suggests a problem with static file serving configuration")
                    else:
                        print(f"✅ {working_external} external URLs are working correctly")
            
            print("\n🔧 RECOMMENDED FIXES:")
            if localhost_urls:
                print("1. Fix backend environment variable REACT_APP_BACKEND_URL")
                print("   Current issue: Some images stored with localhost URLs")
            
            # Test static serving
            try:
                test_response = requests.get(f"{base_url}/uploads/370fb168-5397-4092-b453-61306530f7ef.png")
                if test_response.status_code == 200:
                    if not test_response.headers.get('content-type', '').startswith('image/'):
                        print("2. Fix Kubernetes ingress routing for /uploads path")
                        print("   Current issue: /uploads routes to frontend instead of backend static files")
                else:
                    print("2. Check if static file serving is properly configured")
            except:
                print("2. Check network connectivity to static files")
                
    except Exception as e:
        print(f"❌ Could not complete analysis: {e}")

if __name__ == "__main__":
    test_image_upload_functionality()