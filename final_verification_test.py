#!/usr/bin/env python3
"""
Final comprehensive test focusing on the specific operations mentioned in the review request
"""

import requests
import json

BACKEND_URL = "https://c393639a-fa64-415c-a2dd-ed9a85a0a9dc.preview.emergentagent.com/api"

def test_key_operations():
    """Test the key operations mentioned in the review request"""
    session = requests.Session()
    session.timeout = 30
    
    print("🎯 Final Verification Test - Key Operations from Review Request")
    print("=" * 70)
    
    results = {
        'total_tests': 0,
        'passed_tests': 0,
        'failed_tests': []
    }
    
    def log_test(name, success, message):
        results['total_tests'] += 1
        if success:
            results['passed_tests'] += 1
            print(f"✅ {name}: {message}")
        else:
            results['failed_tests'].append(f"{name}: {message}")
            print(f"❌ {name}: {message}")
    
    # Test 1: PUT /api/services/{id} - Update existing service
    print("\n1. Testing PUT /api/services/{id} (Previously Failing Operation)")
    try:
        # Get existing services
        get_response = session.get(f"{BACKEND_URL}/services")
        if get_response.status_code == 200:
            services = get_response.json()
            if services:
                service_id = services[0]['id']
                original_name = services[0]['name']
                
                # Update the service
                update_data = {
                    "name": f"UPDATED: {original_name}",
                    "description": services[0]['description'],
                    "detailedDescription": services[0]['detailedDescription'],
                    "price": "UPDATED PRICE: от 999 999 ₽",
                    "images": services[0]['images']
                }
                
                put_response = session.put(f"{BACKEND_URL}/services/{service_id}", json=update_data)
                if put_response.status_code == 200:
                    updated_service = put_response.json()
                    if updated_service['name'] == update_data['name'] and updated_service['price'] == update_data['price']:
                        log_test("PUT /api/services/{id}", True, "Service updated successfully with correct data")
                        
                        # Restore original data
                        restore_data = {
                            "name": original_name,
                            "description": services[0]['description'],
                            "detailedDescription": services[0]['detailedDescription'],
                            "price": services[0]['price'],
                            "images": services[0]['images']
                        }
                        session.put(f"{BACKEND_URL}/services/{service_id}", json=restore_data)
                    else:
                        log_test("PUT /api/services/{id}", False, "Service updated but data doesn't match")
                else:
                    log_test("PUT /api/services/{id}", False, f"HTTP {put_response.status_code}: {put_response.text[:100]}")
            else:
                log_test("PUT /api/services/{id}", False, "No services available to test")
        else:
            log_test("PUT /api/services/{id}", False, f"Failed to get services: HTTP {get_response.status_code}")
    except Exception as e:
        log_test("PUT /api/services/{id}", False, f"Exception: {str(e)}")
    
    # Test 2: DELETE /api/services/{id} - Delete service
    print("\n2. Testing DELETE /api/services/{id} (Previously Failing Operation)")
    try:
        # Create a service to delete
        test_service = {
            "name": "Услуга для тестирования DELETE",
            "description": "Эта услуга будет удалена в рамках теста",
            "detailedDescription": "Подробное описание услуги для тестирования DELETE операции",
            "price": "от 1 ₽",
            "images": []
        }
        
        create_response = session.post(f"{BACKEND_URL}/services", json=test_service)
        if create_response.status_code == 200:
            service_data = create_response.json()
            service_id = service_data['id']
            
            # Delete the service
            delete_response = session.delete(f"{BACKEND_URL}/services/{service_id}")
            if delete_response.status_code == 200:
                # Verify deletion
                get_response = session.get(f"{BACKEND_URL}/services")
                if get_response.status_code == 200:
                    services = get_response.json()
                    deleted_service = next((s for s in services if s['id'] == service_id), None)
                    if deleted_service is None:
                        log_test("DELETE /api/services/{id}", True, "Service deleted and verified removed from database")
                    else:
                        log_test("DELETE /api/services/{id}", False, "Service not actually deleted from database")
                else:
                    log_test("DELETE /api/services/{id}", False, "Could not verify deletion")
            else:
                log_test("DELETE /api/services/{id}", False, f"HTTP {delete_response.status_code}: {delete_response.text[:100]}")
        else:
            log_test("DELETE /api/services/{id}", False, f"Failed to create test service: HTTP {create_response.status_code}")
    except Exception as e:
        log_test("DELETE /api/services/{id}", False, f"Exception: {str(e)}")
    
    # Test 3: PUT /api/portfolio/{id} - Update existing portfolio item
    print("\n3. Testing PUT /api/portfolio/{id} (Previously Failing Operation)")
    try:
        # Get existing portfolio
        get_response = session.get(f"{BACKEND_URL}/portfolio")
        if get_response.status_code == 200:
            portfolio = get_response.json()
            if portfolio:
                item_id = portfolio[0]['id']
                original_title = portfolio[0]['title']
                
                # Update the portfolio item
                update_data = {
                    "title": f"UPDATED: {original_title}",
                    "image": portfolio[0]['image'],
                    "category": "UPDATED CATEGORY"
                }
                
                put_response = session.put(f"{BACKEND_URL}/portfolio/{item_id}", json=update_data)
                if put_response.status_code == 200:
                    updated_item = put_response.json()
                    if updated_item['title'] == update_data['title'] and updated_item['category'] == update_data['category']:
                        log_test("PUT /api/portfolio/{id}", True, "Portfolio item updated successfully with correct data")
                        
                        # Restore original data
                        restore_data = {
                            "title": original_title,
                            "image": portfolio[0]['image'],
                            "category": portfolio[0]['category']
                        }
                        session.put(f"{BACKEND_URL}/portfolio/{item_id}", json=restore_data)
                    else:
                        log_test("PUT /api/portfolio/{id}", False, "Portfolio item updated but data doesn't match")
                else:
                    log_test("PUT /api/portfolio/{id}", False, f"HTTP {put_response.status_code}: {put_response.text[:100]}")
            else:
                log_test("PUT /api/portfolio/{id}", False, "No portfolio items available to test")
        else:
            log_test("PUT /api/portfolio/{id}", False, f"Failed to get portfolio: HTTP {get_response.status_code}")
    except Exception as e:
        log_test("PUT /api/portfolio/{id}", False, f"Exception: {str(e)}")
    
    # Test 4: DELETE /api/portfolio/{id} - Delete portfolio item
    print("\n4. Testing DELETE /api/portfolio/{id} (Previously Failing Operation)")
    try:
        # Create a portfolio item to delete
        test_portfolio = {
            "title": "Проект для тестирования DELETE",
            "image": "https://example.com/test-delete-portfolio.jpg",
            "category": "Тестирование DELETE"
        }
        
        create_response = session.post(f"{BACKEND_URL}/portfolio", json=test_portfolio)
        if create_response.status_code == 200:
            item_data = create_response.json()
            item_id = item_data['id']
            
            # Delete the portfolio item
            delete_response = session.delete(f"{BACKEND_URL}/portfolio/{item_id}")
            if delete_response.status_code == 200:
                # Verify deletion
                get_response = session.get(f"{BACKEND_URL}/portfolio")
                if get_response.status_code == 200:
                    portfolio = get_response.json()
                    deleted_item = next((p for p in portfolio if p['id'] == item_id), None)
                    if deleted_item is None:
                        log_test("DELETE /api/portfolio/{id}", True, "Portfolio item deleted and verified removed from database")
                    else:
                        log_test("DELETE /api/portfolio/{id}", False, "Portfolio item not actually deleted from database")
                else:
                    log_test("DELETE /api/portfolio/{id}", False, "Could not verify deletion")
            else:
                log_test("DELETE /api/portfolio/{id}", False, f"HTTP {delete_response.status_code}: {delete_response.text[:100]}")
        else:
            log_test("DELETE /api/portfolio/{id}", False, f"Failed to create test portfolio item: HTTP {create_response.status_code}")
    except Exception as e:
        log_test("DELETE /api/portfolio/{id}", False, f"Exception: {str(e)}")
    
    # Test 5: Overall CRUD functionality verification
    print("\n5. Testing Complete CRUD Cycle")
    try:
        # Create -> Read -> Update -> Delete cycle for services
        test_service = {
            "name": "Полный CRUD тест",
            "description": "Тестирование полного цикла CRUD операций",
            "detailedDescription": "Создание, чтение, обновление и удаление для проверки целостности системы",
            "price": "от 100 ₽",
            "images": ["https://example.com/crud-test.jpg"]
        }
        
        # CREATE
        create_response = session.post(f"{BACKEND_URL}/services", json=test_service)
        if create_response.status_code == 200:
            service_data = create_response.json()
            service_id = service_data['id']
            
            # READ
            get_response = session.get(f"{BACKEND_URL}/services")
            if get_response.status_code == 200:
                services = get_response.json()
                created_service = next((s for s in services if s['id'] == service_id), None)
                
                if created_service and created_service['name'] == test_service['name']:
                    # UPDATE
                    update_data = test_service.copy()
                    update_data['name'] = "ОБНОВЛЕННЫЙ CRUD тест"
                    update_data['price'] = "от 200 ₽"
                    
                    update_response = session.put(f"{BACKEND_URL}/services/{service_id}", json=update_data)
                    if update_response.status_code == 200:
                        updated_service = update_response.json()
                        
                        if updated_service['name'] == update_data['name']:
                            # DELETE
                            delete_response = session.delete(f"{BACKEND_URL}/services/{service_id}")
                            if delete_response.status_code == 200:
                                log_test("Complete CRUD Cycle", True, "CREATE -> READ -> UPDATE -> DELETE all successful")
                            else:
                                log_test("Complete CRUD Cycle", False, f"DELETE failed: HTTP {delete_response.status_code}")
                        else:
                            log_test("Complete CRUD Cycle", False, "UPDATE failed - data not updated correctly")
                    else:
                        log_test("Complete CRUD Cycle", False, f"UPDATE failed: HTTP {update_response.status_code}")
                else:
                    log_test("Complete CRUD Cycle", False, "READ failed - created service not found")
            else:
                log_test("Complete CRUD Cycle", False, f"READ failed: HTTP {get_response.status_code}")
        else:
            log_test("Complete CRUD Cycle", False, f"CREATE failed: HTTP {create_response.status_code}")
    except Exception as e:
        log_test("Complete CRUD Cycle", False, f"Exception: {str(e)}")
    
    # Final Summary
    print("\n" + "=" * 70)
    print("🎯 FINAL VERIFICATION SUMMARY")
    print("=" * 70)
    
    success_rate = (results['passed_tests'] / results['total_tests']) * 100 if results['total_tests'] > 0 else 0
    
    print(f"✅ Passed: {results['passed_tests']}")
    print(f"❌ Failed: {len(results['failed_tests'])}")
    print(f"📈 Success Rate: {results['passed_tests']}/{results['total_tests']} ({success_rate:.1f}%)")
    
    if results['failed_tests']:
        print("\n❌ FAILED OPERATIONS:")
        for failure in results['failed_tests']:
            print(f"  • {failure}")
    
    if success_rate >= 100:
        print("\n🎉 MIGRATION VERIFICATION: COMPLETE SUCCESS!")
        print("All previously failing PUT/DELETE operations are now working correctly.")
        print("The PostgreSQL migration is fully functional and ready for production.")
    elif success_rate >= 80:
        print("\n✅ MIGRATION VERIFICATION: MOSTLY SUCCESSFUL")
        print("Core functionality is working, minor issues may exist.")
    else:
        print("\n⚠️ MIGRATION VERIFICATION: ISSUES DETECTED")
        print("Significant problems found that need attention.")
    
    return success_rate >= 80

if __name__ == "__main__":
    test_key_operations()