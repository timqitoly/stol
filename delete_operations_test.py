#!/usr/bin/env python3
"""
Specific test for DELETE operations that were previously failing
"""

import requests
import json

BACKEND_URL = "https://c393639a-fa64-415c-a2dd-ed9a85a0a9dc.preview.emergentagent.com/api"

def test_delete_operations():
    """Test DELETE operations specifically"""
    session = requests.Session()
    session.timeout = 30
    
    print("🧪 Testing DELETE Operations Specifically")
    print("=" * 50)
    
    # Test DELETE service
    print("\n1. Testing DELETE Service Operation:")
    
    # First create a service to delete
    test_service = {
        "name": "Услуга для удаления",
        "description": "Тестовая услуга для проверки DELETE операции",
        "detailedDescription": "Подробное описание услуги которая будет удалена",
        "price": "от 50 000 ₽",
        "images": ["https://example.com/delete-test.jpg"]
    }
    
    create_response = session.post(f"{BACKEND_URL}/services", json=test_service)
    if create_response.status_code == 200:
        service_data = create_response.json()
        service_id = service_data['id']
        print(f"✅ Created service for deletion: {service_id}")
        
        # Now delete it
        delete_response = session.delete(f"{BACKEND_URL}/services/{service_id}")
        if delete_response.status_code == 200:
            print("✅ DELETE Service: Successfully deleted")
            
            # Verify it's actually deleted by trying to get it
            get_response = session.get(f"{BACKEND_URL}/services")
            if get_response.status_code == 200:
                services = get_response.json()
                deleted_service = next((s for s in services if s['id'] == service_id), None)
                if deleted_service is None:
                    print("✅ Verification: Service properly removed from database")
                else:
                    print("❌ Verification: Service still exists in database")
        else:
            print(f"❌ DELETE Service failed: HTTP {delete_response.status_code}")
            print(f"Response: {delete_response.text}")
    else:
        print(f"❌ Failed to create test service: HTTP {create_response.status_code}")
    
    # Test DELETE portfolio
    print("\n2. Testing DELETE Portfolio Operation:")
    
    # First create a portfolio item to delete
    test_portfolio = {
        "title": "Проект для удаления",
        "image": "https://example.com/delete-portfolio.jpg",
        "category": "Тестирование удаления"
    }
    
    create_response = session.post(f"{BACKEND_URL}/portfolio", json=test_portfolio)
    if create_response.status_code == 200:
        portfolio_data = create_response.json()
        portfolio_id = portfolio_data['id']
        print(f"✅ Created portfolio item for deletion: {portfolio_id}")
        
        # Now delete it
        delete_response = session.delete(f"{BACKEND_URL}/portfolio/{portfolio_id}")
        if delete_response.status_code == 200:
            print("✅ DELETE Portfolio: Successfully deleted")
            
            # Verify it's actually deleted
            get_response = session.get(f"{BACKEND_URL}/portfolio")
            if get_response.status_code == 200:
                portfolio_items = get_response.json()
                deleted_item = next((p for p in portfolio_items if p['id'] == portfolio_id), None)
                if deleted_item is None:
                    print("✅ Verification: Portfolio item properly removed from database")
                else:
                    print("❌ Verification: Portfolio item still exists in database")
        else:
            print(f"❌ DELETE Portfolio failed: HTTP {delete_response.status_code}")
            print(f"Response: {delete_response.text}")
    else:
        print(f"❌ Failed to create test portfolio item: HTTP {create_response.status_code}")
    
    print("\n" + "=" * 50)
    print("DELETE Operations Test Complete")

if __name__ == "__main__":
    test_delete_operations()