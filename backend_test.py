#!/usr/bin/env python3
"""
Comprehensive Backend API Tests for AI Website Builder
Tests all API endpoints including generation, download, and database operations
"""

import requests
import json
import time
import zipfile
import io
import os
import sys
from typing import Dict, Any, Optional

class AIWebsiteBuilderTester:
    def __init__(self, base_url: str = "http://localhost:3000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.test_results = []
        self.generated_code = None
        self.generation_id = None
        
    def log_test(self, test_name: str, success: bool, message: str, details: Optional[Dict] = None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "details": details or {}
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name} - {message}")
        if details:
            print(f"   Details: {details}")
        print()

    def test_api_status(self) -> bool:
        """Test GET /api/ endpoint to ensure API is running"""
        try:
            response = requests.get(f"{self.api_url}/", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "AI Website Builder API" in data["message"]:
                    self.log_test("API Status Check", True, "API is running and responding correctly", 
                                {"status_code": response.status_code, "response": data})
                    return True
                else:
                    self.log_test("API Status Check", False, "API response format unexpected", 
                                {"status_code": response.status_code, "response": data})
                    return False
            else:
                self.log_test("API Status Check", False, f"API returned status {response.status_code}", 
                            {"status_code": response.status_code, "response": response.text})
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test("API Status Check", False, f"Failed to connect to API: {str(e)}")
            return False

    def test_website_generation_simple(self) -> bool:
        """Test POST /api/generate with simple prompt"""
        prompt = "Create a basic portfolio website"
        
        try:
            response = requests.post(
                f"{self.api_url}/generate",
                json={"prompt": prompt},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("code") and data.get("id"):
                    # Store for later tests
                    self.generated_code = data["code"]
                    self.generation_id = data["id"]
                    
                    # Basic validation of generated HTML
                    code = data["code"]
                    has_html = "<html" in code.lower()
                    has_head = "<head" in code.lower()
                    has_body = "<body" in code.lower()
                    has_title = "<title" in code.lower()
                    
                    if has_html and has_head and has_body and has_title:
                        self.log_test("Simple Website Generation", True, 
                                    "Generated valid HTML structure", 
                                    {"prompt": prompt, "code_length": len(code), 
                                     "generation_id": data["id"]})
                        return True
                    else:
                        self.log_test("Simple Website Generation", False, 
                                    "Generated code missing essential HTML elements",
                                    {"has_html": has_html, "has_head": has_head, 
                                     "has_body": has_body, "has_title": has_title})
                        return False
                else:
                    self.log_test("Simple Website Generation", False, 
                                "Response missing required fields",
                                {"response": data})
                    return False
            else:
                self.log_test("Simple Website Generation", False, 
                            f"API returned status {response.status_code}",
                            {"status_code": response.status_code, "response": response.text})
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test("Simple Website Generation", False, f"Request failed: {str(e)}")
            return False

    def test_website_generation_complex(self) -> bool:
        """Test POST /api/generate with complex prompt"""
        prompt = "Create a modern restaurant website with menu, location, and contact form using dark theme"
        
        try:
            response = requests.post(
                f"{self.api_url}/generate",
                json={"prompt": prompt},
                headers={"Content-Type": "application/json"},
                timeout=45
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("code"):
                    code = data["code"]
                    
                    # Check for restaurant-specific elements
                    has_menu = "menu" in code.lower()
                    has_contact = "contact" in code.lower()
                    has_location = "location" in code.lower() or "address" in code.lower()
                    has_dark_theme = "dark" in code.lower() or "black" in code.lower() or "#000" in code or "bg-gray-900" in code or "bg-black" in code
                    
                    if has_menu and has_contact and (has_location or has_dark_theme):
                        self.log_test("Complex Website Generation", True, 
                                    "Generated restaurant website with requested features",
                                    {"prompt": prompt, "has_menu": has_menu, 
                                     "has_contact": has_contact, "has_location": has_location,
                                     "has_dark_theme": has_dark_theme})
                        return True
                    else:
                        self.log_test("Complex Website Generation", False, 
                                    "Generated website missing some requested features",
                                    {"has_menu": has_menu, "has_contact": has_contact, 
                                     "has_location": has_location, "has_dark_theme": has_dark_theme})
                        return False
                else:
                    self.log_test("Complex Website Generation", False, 
                                "Response missing required fields",
                                {"response": data})
                    return False
            else:
                self.log_test("Complex Website Generation", False, 
                            f"API returned status {response.status_code}",
                            {"status_code": response.status_code, "response": response.text})
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test("Complex Website Generation", False, f"Request failed: {str(e)}")
            return False

    def test_website_generation_edge_cases(self) -> bool:
        """Test POST /api/generate with edge cases"""
        test_cases = [
            {"prompt": "", "expected_status": 400, "description": "Empty prompt"},
            {"prompt": None, "expected_status": 400, "description": "Null prompt"},
            {"prompt": "a" * 10000, "expected_status": 200, "description": "Very long prompt"}
        ]
        
        all_passed = True
        
        for case in test_cases:
            try:
                response = requests.post(
                    f"{self.api_url}/generate",
                    json={"prompt": case["prompt"]},
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                
                if response.status_code == case["expected_status"]:
                    if case["expected_status"] == 400:
                        data = response.json()
                        if "error" in data:
                            self.log_test(f"Edge Case - {case['description']}", True, 
                                        "Correctly rejected invalid input",
                                        {"expected_status": case["expected_status"], 
                                         "actual_status": response.status_code})
                        else:
                            self.log_test(f"Edge Case - {case['description']}", False, 
                                        "Missing error message in response")
                            all_passed = False
                    else:
                        self.log_test(f"Edge Case - {case['description']}", True, 
                                    "Handled edge case correctly",
                                    {"expected_status": case["expected_status"], 
                                     "actual_status": response.status_code})
                else:
                    self.log_test(f"Edge Case - {case['description']}", False, 
                                f"Expected status {case['expected_status']}, got {response.status_code}")
                    all_passed = False
                    
            except requests.exceptions.RequestException as e:
                self.log_test(f"Edge Case - {case['description']}", False, f"Request failed: {str(e)}")
                all_passed = False
        
        return all_passed

    def test_download_functionality(self) -> bool:
        """Test POST /api/download with generated HTML code"""
        if not self.generated_code:
            self.log_test("Download Functionality", False, "No generated code available for download test")
            return False
        
        try:
            response = requests.post(
                f"{self.api_url}/download",
                json={"code": self.generated_code},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                # Check if response is a ZIP file
                content_type = response.headers.get('content-type', '')
                content_disposition = response.headers.get('content-disposition', '')
                
                if 'application/zip' in content_type and 'attachment' in content_disposition:
                    # Try to read the ZIP file
                    try:
                        zip_data = io.BytesIO(response.content)
                        with zipfile.ZipFile(zip_data, 'r') as zip_file:
                            file_list = zip_file.namelist()
                            
                            # Check for expected files
                            has_index_html = 'index.html' in file_list
                            has_readme = 'README.md' in file_list
                            
                            if has_index_html and has_readme:
                                # Verify index.html content
                                index_content = zip_file.read('index.html').decode('utf-8')
                                if len(index_content) > 100:  # Basic content check
                                    self.log_test("Download Functionality", True, 
                                                "Successfully created valid ZIP file",
                                                {"files": file_list, "zip_size": len(response.content)})
                                    return True
                                else:
                                    self.log_test("Download Functionality", False, 
                                                "index.html content too short")
                                    return False
                            else:
                                self.log_test("Download Functionality", False, 
                                            "ZIP missing required files",
                                            {"files": file_list, "has_index": has_index_html, 
                                             "has_readme": has_readme})
                                return False
                                
                    except zipfile.BadZipFile:
                        self.log_test("Download Functionality", False, "Response is not a valid ZIP file")
                        return False
                else:
                    self.log_test("Download Functionality", False, 
                                "Response headers indicate non-ZIP content",
                                {"content_type": content_type, "content_disposition": content_disposition})
                    return False
            else:
                self.log_test("Download Functionality", False, 
                            f"API returned status {response.status_code}",
                            {"status_code": response.status_code, "response": response.text})
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test("Download Functionality", False, f"Request failed: {str(e)}")
            return False

    def test_download_edge_cases(self) -> bool:
        """Test POST /api/download with edge cases"""
        test_cases = [
            {"code": "", "expected_status": 400, "description": "Empty code"},
            {"code": None, "expected_status": 400, "description": "Null code"},
        ]
        
        all_passed = True
        
        for case in test_cases:
            try:
                response = requests.post(
                    f"{self.api_url}/download",
                    json={"code": case["code"]},
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                
                if response.status_code == case["expected_status"]:
                    data = response.json()
                    if "error" in data:
                        self.log_test(f"Download Edge Case - {case['description']}", True, 
                                    "Correctly rejected invalid input",
                                    {"expected_status": case["expected_status"], 
                                     "actual_status": response.status_code})
                    else:
                        self.log_test(f"Download Edge Case - {case['description']}", False, 
                                    "Missing error message in response")
                        all_passed = False
                else:
                    self.log_test(f"Download Edge Case - {case['description']}", False, 
                                f"Expected status {case['expected_status']}, got {response.status_code}")
                    all_passed = False
                    
            except requests.exceptions.RequestException as e:
                self.log_test(f"Download Edge Case - {case['description']}", False, f"Request failed: {str(e)}")
                all_passed = False
        
        return all_passed

    def test_database_operations(self) -> bool:
        """Test database operations by checking generations endpoint"""
        try:
            response = requests.get(f"{self.api_url}/generations", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    # Check if our generation is stored
                    if self.generation_id:
                        found_generation = any(gen.get("id") == self.generation_id for gen in data)
                        if found_generation:
                            self.log_test("Database Operations", True, 
                                        "Generation successfully stored and retrieved from database",
                                        {"total_generations": len(data), "found_our_generation": True})
                            return True
                        else:
                            self.log_test("Database Operations", False, 
                                        "Our generation not found in database",
                                        {"total_generations": len(data), "generation_id": self.generation_id})
                            return False
                    else:
                        # If we don't have a generation ID, just check if endpoint works
                        self.log_test("Database Operations", True, 
                                    "Database endpoint accessible",
                                    {"total_generations": len(data)})
                        return True
                else:
                    self.log_test("Database Operations", False, 
                                "Generations endpoint returned non-array response",
                                {"response_type": type(data)})
                    return False
            else:
                self.log_test("Database Operations", False, 
                            f"Generations endpoint returned status {response.status_code}",
                            {"status_code": response.status_code})
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test("Database Operations", False, f"Request failed: {str(e)}")
            return False

    def test_status_endpoints(self) -> bool:
        """Test status check endpoints"""
        try:
            # Test POST /api/status
            client_name = "backend_test_client"
            response = requests.post(
                f"{self.api_url}/status",
                json={"client_name": client_name},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("client_name") == client_name and data.get("id"):
                    # Test GET /api/status
                    get_response = requests.get(f"{self.api_url}/status", timeout=10)
                    
                    if get_response.status_code == 200:
                        status_data = get_response.json()
                        if isinstance(status_data, list):
                            self.log_test("Status Endpoints", True, 
                                        "Status endpoints working correctly",
                                        {"post_response": data, "total_status_checks": len(status_data)})
                            return True
                        else:
                            self.log_test("Status Endpoints", False, 
                                        "GET status returned non-array response")
                            return False
                    else:
                        self.log_test("Status Endpoints", False, 
                                    f"GET status returned status {get_response.status_code}")
                        return False
                else:
                    self.log_test("Status Endpoints", False, 
                                "POST status response missing required fields",
                                {"response": data})
                    return False
            else:
                self.log_test("Status Endpoints", False, 
                            f"POST status returned status {response.status_code}",
                            {"status_code": response.status_code})
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test("Status Endpoints", False, f"Request failed: {str(e)}")
            return False

    def test_error_handling(self) -> bool:
        """Test various error scenarios"""
        test_cases = [
            {
                "endpoint": "/nonexistent",
                "method": "GET",
                "expected_status": 404,
                "description": "Non-existent endpoint"
            },
            {
                "endpoint": "/generate",
                "method": "POST",
                "data": {"invalid": "data"},
                "expected_status": 400,
                "description": "Invalid request data for generate"
            },
            {
                "endpoint": "/status",
                "method": "POST",
                "data": {},
                "expected_status": 400,
                "description": "Missing client_name in status"
            }
        ]
        
        all_passed = True
        
        for case in test_cases:
            try:
                if case["method"] == "GET":
                    response = requests.get(f"{self.api_url}{case['endpoint']}", timeout=10)
                else:
                    response = requests.post(
                        f"{self.api_url}{case['endpoint']}",
                        json=case.get("data", {}),
                        headers={"Content-Type": "application/json"},
                        timeout=10
                    )
                
                if response.status_code == case["expected_status"]:
                    self.log_test(f"Error Handling - {case['description']}", True, 
                                "Correctly handled error scenario",
                                {"expected_status": case["expected_status"], 
                                 "actual_status": response.status_code})
                else:
                    self.log_test(f"Error Handling - {case['description']}", False, 
                                f"Expected status {case['expected_status']}, got {response.status_code}")
                    all_passed = False
                    
            except requests.exceptions.RequestException as e:
                self.log_test(f"Error Handling - {case['description']}", False, f"Request failed: {str(e)}")
                all_passed = False
        
        return all_passed

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and return summary"""
        print("🚀 Starting AI Website Builder Backend API Tests")
        print("=" * 60)
        print()
        
        # Run tests in order
        tests = [
            ("API Status Check", self.test_api_status),
            ("Simple Website Generation", self.test_website_generation_simple),
            ("Complex Website Generation", self.test_website_generation_complex),
            ("Website Generation Edge Cases", self.test_website_generation_edge_cases),
            ("Download Functionality", self.test_download_functionality),
            ("Download Edge Cases", self.test_download_edge_cases),
            ("Database Operations", self.test_database_operations),
            ("Status Endpoints", self.test_status_endpoints),
            ("Error Handling", self.test_error_handling),
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                if result:
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                self.log_test(test_name, False, f"Test threw exception: {str(e)}")
                failed += 1
        
        # Summary
        print("=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {passed + failed}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"Success Rate: {(passed / (passed + failed) * 100):.1f}%")
        print()
        
        if failed > 0:
            print("❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['message']}")
            print()
        
        return {
            "total": passed + failed,
            "passed": passed,
            "failed": failed,
            "success_rate": passed / (passed + failed) * 100 if (passed + failed) > 0 else 0,
            "results": self.test_results
        }

def main():
    """Main test execution"""
    # Check if Next.js is running
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        print("✅ Next.js application is running")
    except requests.exceptions.RequestException:
        print("❌ Next.js application is not accessible at http://localhost:3000")
        print("Please ensure the application is running with: yarn dev")
        sys.exit(1)
    
    # Run tests
    tester = AIWebsiteBuilderTester()
    summary = tester.run_all_tests()
    
    # Exit with appropriate code
    if summary["failed"] > 0:
        sys.exit(1)
    else:
        print("🎉 All tests passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()