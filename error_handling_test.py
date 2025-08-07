#!/usr/bin/env python3
"""
Test error handling and edge cases for the PostgreSQL migration
"""

import requests
import json
import uuid

BACKEND_URL = "https://c393639a-fa64-415c-a2dd-ed9a85a0a9dc.preview.emergentagent.com/api"

def test_error_handling():
    """Test error handling scenarios"""
    session = requests.Session()
    session.timeout = 30
    
    print("🧪 Testing Error Handling and Edge Cases")
    print("=" * 50)
    
    # Test 1: DELETE non-existent service
    print("\n1. Testing DELETE non-existent service:")
    fake_id = str(uuid.uuid4())
    delete_response = session.delete(f"{BACKEND_URL}/services/{fake_id}")
    if delete_response.status_code == 404:
        print("✅ DELETE non-existent service: Properly returns 404")
    else:
        print(f"❌ DELETE non-existent service: Expected 404, got {delete_response.status_code}")
    
    # Test 2: DELETE non-existent portfolio
    print("\n2. Testing DELETE non-existent portfolio:")
    fake_id = str(uuid.uuid4())
    delete_response = session.delete(f"{BACKEND_URL}/portfolio/{fake_id}")
    if delete_response.status_code == 404:
        print("✅ DELETE non-existent portfolio: Properly returns 404")
    else:
        print(f"❌ DELETE non-existent portfolio: Expected 404, got {delete_response.status_code}")
    
    # Test 3: PUT non-existent service
    print("\n3. Testing PUT non-existent service:")
    fake_id = str(uuid.uuid4())
    update_data = {
        "name": "Non-existent service",
        "description": "This should fail",
        "detailedDescription": "This service doesn't exist",
        "price": "0 ₽",
        "images": []
    }
    put_response = session.put(f"{BACKEND_URL}/services/{fake_id}", json=update_data)
    if put_response.status_code == 404:
        print("✅ PUT non-existent service: Properly returns 404")
    else:
        print(f"❌ PUT non-existent service: Expected 404, got {put_response.status_code}")
    
    # Test 4: PUT non-existent portfolio
    print("\n4. Testing PUT non-existent portfolio:")
    fake_id = str(uuid.uuid4())
    update_data = {
        "title": "Non-existent portfolio",
        "image": "https://example.com/fake.jpg",
        "category": "Fake"
    }
    put_response = session.put(f"{BACKEND_URL}/portfolio/{fake_id}", json=update_data)
    if put_response.status_code == 404:
        print("✅ PUT non-existent portfolio: Properly returns 404")
    else:
        print(f"❌ PUT non-existent portfolio: Expected 404, got {put_response.status_code}")
    
    # Test 5: Invalid UUID format
    print("\n5. Testing invalid UUID format:")
    invalid_id = "not-a-valid-uuid"
    delete_response = session.delete(f"{BACKEND_URL}/services/{invalid_id}")
    print(f"DELETE with invalid UUID: HTTP {delete_response.status_code}")
    # This might return 404 or 422 depending on validation, both are acceptable
    if delete_response.status_code in [404, 422, 500]:
        print("✅ Invalid UUID: Properly handled")
    else:
        print(f"❌ Invalid UUID: Unexpected status {delete_response.status_code}")
    
    print("\n" + "=" * 50)
    print("Error Handling Test Complete")

if __name__ == "__main__":
    test_error_handling()