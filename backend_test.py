#!/usr/bin/env python3
"""
Backend Test Suite for PostgreSQL Migration
Tests all API endpoints and database functionality after MongoDB to PostgreSQL migration
"""

import asyncio
import requests
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List
import uuid
from datetime import datetime

# Add backend to path for imports
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

# Test configuration
BACKEND_URL = "https://c393639a-fa64-415c-a2dd-ed9a85a0a9dc.preview.emergentagent.com/api"
TEST_TIMEOUT = 30

class BackendTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.session = requests.Session()
        self.session.timeout = TEST_TIMEOUT
        self.test_results = []
        self.created_resources = {
            'services': [],
            'portfolio': [],
            'images': []
        }
    
    def log_test(self, test_name: str, success: bool, message: str, details: str = ""):
        """Log test result"""
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if details and not success:
            print(f"   Details: {details}")
    
    def test_basic_connectivity(self) -> bool:
        """Test basic API connectivity"""
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                if "Княжий Терем API" in data.get("message", ""):
                    self.log_test("Basic Connectivity", True, "API is accessible and responding")
                    return True
                else:
                    self.log_test("Basic Connectivity", False, "API responding but wrong message", str(data))
                    return False
            else:
                self.log_test("Basic Connectivity", False, f"HTTP {response.status_code}", response.text[:200])
                return False
        except Exception as e:
            self.log_test("Basic Connectivity", False, "Connection failed", str(e))
            return False
    
    def test_services_endpoints(self) -> bool:
        """Test all services CRUD operations"""
        all_passed = True
        
        # Test GET services
        try:
            response = self.session.get(f"{self.base_url}/services")
            if response.status_code == 200:
                services = response.json()
                if isinstance(services, list):
                    self.log_test("GET Services", True, f"Retrieved {len(services)} services")
                    # Verify service structure
                    if services:
                        service = services[0]
                        required_fields = ['id', 'name', 'description', 'detailedDescription', 'price', 'images', 'createdAt', 'updatedAt']
                        missing_fields = [field for field in required_fields if field not in service]
                        if missing_fields:
                            self.log_test("Service Structure", False, f"Missing fields: {missing_fields}")
                            all_passed = False
                        else:
                            self.log_test("Service Structure", True, "All required fields present")
                else:
                    self.log_test("GET Services", False, "Response is not a list", str(services))
                    all_passed = False
            else:
                self.log_test("GET Services", False, f"HTTP {response.status_code}", response.text[:200])
                all_passed = False
        except Exception as e:
            self.log_test("GET Services", False, "Request failed", str(e))
            all_passed = False
        
        # Test POST service (create)
        try:
            test_service = {
                "name": "Тестовая услуга",
                "description": "Описание тестовой услуги",
                "detailedDescription": "Подробное описание тестовой услуги для проверки API",
                "price": "от 100 000 ₽",
                "images": ["https://example.com/test1.jpg", "https://example.com/test2.jpg"]
            }
            
            response = self.session.post(f"{self.base_url}/services", json=test_service)
            if response.status_code == 200:
                created_service = response.json()
                if 'id' in created_service and created_service['name'] == test_service['name']:
                    self.created_resources['services'].append(created_service['id'])
                    self.log_test("POST Service", True, f"Created service with ID: {created_service['id']}")
                    
                    # Test PUT service (update)
                    updated_service = test_service.copy()
                    updated_service['name'] = "Обновленная тестовая услуга"
                    updated_service['price'] = "от 150 000 ₽"
                    
                    update_response = self.session.put(f"{self.base_url}/services/{created_service['id']}", json=updated_service)
                    if update_response.status_code == 200:
                        updated_data = update_response.json()
                        if updated_data['name'] == updated_service['name']:
                            self.log_test("PUT Service", True, "Service updated successfully")
                        else:
                            self.log_test("PUT Service", False, "Service not updated properly", str(updated_data))
                            all_passed = False
                    else:
                        self.log_test("PUT Service", False, f"HTTP {update_response.status_code}", update_response.text[:200])
                        all_passed = False
                else:
                    self.log_test("POST Service", False, "Invalid response structure", str(created_service))
                    all_passed = False
            else:
                self.log_test("POST Service", False, f"HTTP {response.status_code}", response.text[:200])
                all_passed = False
        except Exception as e:
            self.log_test("POST Service", False, "Request failed", str(e))
            all_passed = False
        
        return all_passed
    
    def test_portfolio_endpoints(self) -> bool:
        """Test all portfolio CRUD operations"""
        all_passed = True
        
        # Test GET portfolio
        try:
            response = self.session.get(f"{self.base_url}/portfolio")
            if response.status_code == 200:
                portfolio = response.json()
                if isinstance(portfolio, list):
                    self.log_test("GET Portfolio", True, f"Retrieved {len(portfolio)} portfolio items")
                    # Verify portfolio structure
                    if portfolio:
                        item = portfolio[0]
                        required_fields = ['id', 'title', 'image', 'category', 'createdAt', 'updatedAt']
                        missing_fields = [field for field in required_fields if field not in item]
                        if missing_fields:
                            self.log_test("Portfolio Structure", False, f"Missing fields: {missing_fields}")
                            all_passed = False
                        else:
                            self.log_test("Portfolio Structure", True, "All required fields present")
                else:
                    self.log_test("GET Portfolio", False, "Response is not a list", str(portfolio))
                    all_passed = False
            else:
                self.log_test("GET Portfolio", False, f"HTTP {response.status_code}", response.text[:200])
                all_passed = False
        except Exception as e:
            self.log_test("GET Portfolio", False, "Request failed", str(e))
            all_passed = False
        
        # Test POST portfolio (create)
        try:
            test_portfolio = {
                "title": "Тестовый проект",
                "image": "https://example.com/test-portfolio.jpg",
                "category": "Тестирование"
            }
            
            response = self.session.post(f"{self.base_url}/portfolio", json=test_portfolio)
            if response.status_code == 200:
                created_item = response.json()
                if 'id' in created_item and created_item['title'] == test_portfolio['title']:
                    self.created_resources['portfolio'].append(created_item['id'])
                    self.log_test("POST Portfolio", True, f"Created portfolio item with ID: {created_item['id']}")
                    
                    # Test PUT portfolio (update)
                    updated_portfolio = test_portfolio.copy()
                    updated_portfolio['title'] = "Обновленный тестовый проект"
                    updated_portfolio['category'] = "Обновленное тестирование"
                    
                    update_response = self.session.put(f"{self.base_url}/portfolio/{created_item['id']}", json=updated_portfolio)
                    if update_response.status_code == 200:
                        updated_data = update_response.json()
                        if updated_data['title'] == updated_portfolio['title']:
                            self.log_test("PUT Portfolio", True, "Portfolio item updated successfully")
                        else:
                            self.log_test("PUT Portfolio", False, "Portfolio item not updated properly", str(updated_data))
                            all_passed = False
                    else:
                        self.log_test("PUT Portfolio", False, f"HTTP {update_response.status_code}", update_response.text[:200])
                        all_passed = False
                else:
                    self.log_test("POST Portfolio", False, "Invalid response structure", str(created_item))
                    all_passed = False
            else:
                self.log_test("POST Portfolio", False, f"HTTP {response.status_code}", response.text[:200])
                all_passed = False
        except Exception as e:
            self.log_test("POST Portfolio", False, "Request failed", str(e))
            all_passed = False
        
        return all_passed
    
    def test_contacts_endpoints(self) -> bool:
        """Test contacts endpoints"""
        all_passed = True
        
        # Test GET contacts
        try:
            response = self.session.get(f"{self.base_url}/contacts")
            if response.status_code == 200:
                contacts = response.json()
                required_fields = ['id', 'name', 'tagline', 'phone', 'whatsapp', 'email', 'updatedAt']
                missing_fields = [field for field in required_fields if field not in contacts]
                if missing_fields:
                    self.log_test("GET Contacts", False, f"Missing fields: {missing_fields}")
                    all_passed = False
                else:
                    self.log_test("GET Contacts", True, "Retrieved contacts successfully")
                    
                    # Test PUT contacts (update)
                    updated_contacts = {
                        "name": contacts['name'],
                        "tagline": "Обновленный слоган для тестирования",
                        "phone": contacts['phone'],
                        "whatsapp": contacts['whatsapp'],
                        "email": contacts['email']
                    }
                    
                    update_response = self.session.put(f"{self.base_url}/contacts", json=updated_contacts)
                    if update_response.status_code == 200:
                        updated_data = update_response.json()
                        if updated_data['tagline'] == updated_contacts['tagline']:
                            self.log_test("PUT Contacts", True, "Contacts updated successfully")
                        else:
                            self.log_test("PUT Contacts", False, "Contacts not updated properly", str(updated_data))
                            all_passed = False
                    else:
                        self.log_test("PUT Contacts", False, f"HTTP {update_response.status_code}", update_response.text[:200])
                        all_passed = False
            else:
                self.log_test("GET Contacts", False, f"HTTP {response.status_code}", response.text[:200])
                all_passed = False
        except Exception as e:
            self.log_test("GET Contacts", False, "Request failed", str(e))
            all_passed = False
        
        return all_passed
    
    def test_admin_endpoints(self) -> bool:
        """Test admin login endpoint"""
        all_passed = True
        
        # Test valid login
        try:
            valid_login = {"login": "admin", "password": "admin123"}
            response = self.session.post(f"{self.base_url}/admin/login", json=valid_login)
            if response.status_code == 200:
                result = response.json()
                if result.get('success') == True:
                    self.log_test("Admin Login (Valid)", True, "Valid credentials accepted")
                else:
                    self.log_test("Admin Login (Valid)", False, "Valid credentials rejected", str(result))
                    all_passed = False
            else:
                self.log_test("Admin Login (Valid)", False, f"HTTP {response.status_code}", response.text[:200])
                all_passed = False
        except Exception as e:
            self.log_test("Admin Login (Valid)", False, "Request failed", str(e))
            all_passed = False
        
        # Test invalid login
        try:
            invalid_login = {"login": "wrong", "password": "wrong"}
            response = self.session.post(f"{self.base_url}/admin/login", json=invalid_login)
            if response.status_code == 200:
                result = response.json()
                if result.get('success') == False:
                    self.log_test("Admin Login (Invalid)", True, "Invalid credentials properly rejected")
                else:
                    self.log_test("Admin Login (Invalid)", False, "Invalid credentials accepted", str(result))
                    all_passed = False
            else:
                self.log_test("Admin Login (Invalid)", False, f"HTTP {response.status_code}", response.text[:200])
                all_passed = False
        except Exception as e:
            self.log_test("Admin Login (Invalid)", False, "Request failed", str(e))
            all_passed = False
        
        return all_passed
    
    def test_image_endpoints(self) -> bool:
        """Test image upload endpoints and static file serving"""
        all_passed = True
        
        # Test GET uploaded images
        try:
            response = self.session.get(f"{self.base_url}/uploaded-images")
            if response.status_code == 200:
                images = response.json()
                if isinstance(images, list):
                    self.log_test("GET Uploaded Images", True, f"Retrieved {len(images)} uploaded images")
                    
                    # Test static file serving for existing images
                    if images:
                        # Verify image structure
                        image = images[0]
                        required_fields = ['id', 'filename', 'original_filename', 'url', 'size', 'createdAt']
                        missing_fields = [field for field in required_fields if field not in image]
                        if missing_fields:
                            self.log_test("Image Structure", False, f"Missing fields: {missing_fields}")
                            all_passed = False
                        else:
                            self.log_test("Image Structure", True, "All required fields present")
                            
                            # Test direct image URL access
                            self.test_image_url_access(images)
                    else:
                        self.log_test("Image URL Access", True, "No images to test URL access")
                else:
                    self.log_test("GET Uploaded Images", False, "Response is not a list", str(images))
                    all_passed = False
            else:
                self.log_test("GET Uploaded Images", False, f"HTTP {response.status_code}", response.text[:200])
                all_passed = False
        except Exception as e:
            self.log_test("GET Uploaded Images", False, "Request failed", str(e))
            all_passed = False
        
        # Test image upload with a small test image
        upload_success = self.test_image_upload()
        if not upload_success:
            all_passed = False
        
        return all_passed
    
    def test_image_url_access(self, images: List[Dict[str, Any]]):
        """Test direct access to uploaded image URLs"""
        for i, image in enumerate(images[:3]):  # Test first 3 images only
            try:
                image_url = image['url']
                self.log_test("Image URL Format", True, f"Image {i+1} URL: {image_url}")
                
                # Test direct HTTP access to the image
                response = self.session.get(image_url, timeout=10)
                if response.status_code == 200:
                    # Check if it's actually an image by content type
                    content_type = response.headers.get('content-type', '')
                    if content_type.startswith('image/'):
                        self.log_test(f"Image Access {i+1}", True, f"Image accessible at {image_url}")
                    else:
                        self.log_test(f"Image Access {i+1}", False, f"URL returns non-image content: {content_type}")
                elif response.status_code == 404:
                    self.log_test(f"Image Access {i+1}", False, f"Image not found at {image_url}")
                else:
                    self.log_test(f"Image Access {i+1}", False, f"HTTP {response.status_code} for {image_url}")
            except Exception as e:
                self.log_test(f"Image Access {i+1}", False, f"Failed to access {image_url}", str(e))
    
    def test_image_upload(self) -> bool:
        """Test actual image upload functionality"""
        try:
            # Create a small test image (1x1 pixel PNG)
            import io
            from PIL import Image
            
            # Create a small test image
            test_image = Image.new('RGB', (1, 1), color='red')
            img_buffer = io.BytesIO()
            test_image.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            # Prepare multipart form data
            files = {
                'file': ('test_image.png', img_buffer, 'image/png')
            }
            
            # Upload the image
            response = self.session.post(f"{self.base_url}/upload-image", files=files)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    uploaded_image = result.get('image')
                    if uploaded_image and 'url' in uploaded_image:
                        self.created_resources['images'].append(uploaded_image['id'])
                        self.log_test("Image Upload", True, f"Successfully uploaded test image")
                        
                        # Test immediate access to uploaded image
                        image_url = uploaded_image['url']
                        access_response = self.session.get(image_url, timeout=10)
                        if access_response.status_code == 200:
                            self.log_test("Uploaded Image Access", True, f"Uploaded image immediately accessible")
                        else:
                            self.log_test("Uploaded Image Access", False, f"Uploaded image not accessible: HTTP {access_response.status_code}")
                        
                        return True
                    else:
                        self.log_test("Image Upload", False, "Upload successful but no image URL returned", str(result))
                        return False
                else:
                    self.log_test("Image Upload", False, f"Upload failed: {result.get('message', 'Unknown error')}")
                    return False
            else:
                self.log_test("Image Upload", False, f"HTTP {response.status_code}", response.text[:200])
                return False
                
        except ImportError:
            self.log_test("Image Upload", False, "PIL not available for test image creation")
            return False
        except Exception as e:
            self.log_test("Image Upload", False, "Upload test failed", str(e))
            return False
    
    def cleanup_test_data(self):
        """Clean up created test data"""
        print("\n🧹 Cleaning up test data...")
        
        # Delete created services
        for service_id in self.created_resources['services']:
            try:
                response = self.session.delete(f"{self.base_url}/services/{service_id}")
                if response.status_code == 200:
                    print(f"✅ Deleted test service: {service_id}")
                else:
                    print(f"⚠️ Failed to delete service {service_id}: HTTP {response.status_code}")
            except Exception as e:
                print(f"⚠️ Error deleting service {service_id}: {e}")
        
        # Delete created portfolio items
        for portfolio_id in self.created_resources['portfolio']:
            try:
                response = self.session.delete(f"{self.base_url}/portfolio/{portfolio_id}")
                if response.status_code == 200:
                    print(f"✅ Deleted test portfolio item: {portfolio_id}")
                else:
                    print(f"⚠️ Failed to delete portfolio item {portfolio_id}: HTTP {response.status_code}")
            except Exception as e:
                print(f"⚠️ Error deleting portfolio item {portfolio_id}: {e}")
        
        # Delete created images
        for image_id in self.created_resources['images']:
            try:
                response = self.session.delete(f"{self.base_url}/uploaded-images/{image_id}")
                if response.status_code == 200:
                    print(f"✅ Deleted test image: {image_id}")
                else:
                    print(f"⚠️ Failed to delete image {image_id}: HTTP {response.status_code}")
            except Exception as e:
                print(f"⚠️ Error deleting image {image_id}: {e}")
    
    def run_all_tests(self) -> bool:
        """Run all backend tests"""
        print("🚀 Starting Backend API Tests for PostgreSQL Migration")
        print(f"🔗 Testing against: {self.base_url}")
        print("=" * 60)
        
        all_passed = True
        
        # Test basic connectivity first
        if not self.test_basic_connectivity():
            print("❌ Basic connectivity failed - aborting further tests")
            return False
        
        # Run all endpoint tests
        test_methods = [
            self.test_services_endpoints,
            self.test_portfolio_endpoints,
            self.test_contacts_endpoints,
            self.test_admin_endpoints,
            self.test_image_endpoints
        ]
        
        for test_method in test_methods:
            try:
                if not test_method():
                    all_passed = False
            except Exception as e:
                print(f"❌ Test method {test_method.__name__} failed with exception: {e}")
                all_passed = False
        
        # Cleanup
        self.cleanup_test_data()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed_tests = [r for r in self.test_results if r['success']]
        failed_tests = [r for r in self.test_results if not r['success']]
        
        print(f"✅ Passed: {len(passed_tests)}")
        print(f"❌ Failed: {len(failed_tests)}")
        print(f"📈 Success Rate: {len(passed_tests)}/{len(self.test_results)} ({len(passed_tests)/len(self.test_results)*100:.1f}%)")
        
        if failed_tests:
            print("\n❌ FAILED TESTS:")
            for test in failed_tests:
                print(f"  • {test['test']}: {test['message']}")
                if test['details']:
                    print(f"    Details: {test['details']}")
        
        return all_passed

def main():
    """Main test execution"""
    tester = BackendTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed! PostgreSQL migration is working correctly.")
        return 0
    else:
        print("\n⚠️ Some tests failed. Check the details above.")
        return 1

if __name__ == "__main__":
    exit(main())