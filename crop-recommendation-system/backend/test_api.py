"""
Crop Recommendation System - API Testing Script
Run this script to test all API endpoints
"""

import requests
import json
from pprint import pprint
import time

# Configuration
API_BASE_URL = "http://localhost:5000/api"

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")

# Test Cases
test_cases = {
    "Rice Growing Conditions": {
        "N": 90,
        "P": 40,
        "K": 40,
        "temperature": 21.5,
        "humidity": 82,
        "ph": 6.5,
        "rainfall": 202,
        "expected_crop": "Rice"
    },
    "Wheat Growing Conditions": {
        "N": 50,
        "P": 25,
        "K": 25,
        "temperature": 20,
        "humidity": 60,
        "ph": 6.8,
        "rainfall": 75,
        "expected_crop": "Wheat"
    },
    "Cotton Growing Conditions": {
        "N": 70,
        "P": 45,
        "K": 85,
        "temperature": 25,
        "humidity": 50,
        "ph": 6.5,
        "rainfall": 120,
        "expected_crop": "Cotton"
    },
    "Corn Growing Conditions": {
        "N": 80,
        "P": 60,
        "K": 100,
        "temperature": 24,
        "humidity": 70,
        "ph": 6.5,
        "rainfall": 150,
        "expected_crop": "Corn"
    },
    "Sugarcane Growing Conditions": {
        "N": 100,
        "P": 50,
        "K": 150,
        "temperature": 24,
        "humidity": 80,
        "ph": 6.5,
        "rainfall": 200,
        "expected_crop": "Sugarcane"
    }
}

invalid_test_cases = {
    "Missing Fields": {
        "N": 90,
        "P": 40,
        # Missing other fields
    },
    "Out of Range - High Nitrogen": {
        "N": 200,  # Should be 0-140
        "P": 40,
        "K": 40,
        "temperature": 21.5,
        "humidity": 82,
        "ph": 6.5,
        "rainfall": 202
    },
    "Out of Range - Low Temperature": {
        "N": 90,
        "P": 40,
        "K": 40,
        "temperature": 0,  # Should be 8-43
        "humidity": 82,
        "ph": 6.5,
        "rainfall": 202
    },
    "Invalid Data Type": {
        "N": "not_a_number",
        "P": 40,
        "K": 40,
        "temperature": 21.5,
        "humidity": 82,
        "ph": 6.5,
        "rainfall": 202
    }
}

def test_health():
    """Test health check endpoint"""
    print_header("Testing Health Check Endpoint")
    
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Health check endpoint is working")
            print_info(f"Model Status: {data.get('model_status', 'Unknown')}")
            return True
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error connecting to API: {e}")
        return False

def test_valid_recommendations():
    """Test valid crop recommendations"""
    print_header("Testing Valid Crop Recommendations")
    
    passed = 0
    failed = 0
    
    for test_name, test_data in test_cases.items():
        expected_crop = test_data.pop("expected_crop")
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/recommend",
                json=test_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    recommendation = data['data']['recommendation']
                    confidence = data['data']['confidence']
                    
                    # Check if recommendation matches expected crop
                    is_correct = recommendation == expected_crop
                    
                    if is_correct:
                        print_success(
                            f"{test_name}: Got '{recommendation}' "
                            f"(confidence: {confidence:.2%})"
                        )
                        passed += 1
                    else:
                        print_error(
                            f"{test_name}: Got '{recommendation}' "
                            f"but expected '{expected_crop}'"
                        )
                        failed += 1
                else:
                    print_error(f"{test_name}: API returned error")
                    failed += 1
            else:
                print_error(
                    f"{test_name}: HTTP {response.status_code} - "
                    f"{response.text[:100]}"
                )
                failed += 1
                
        except Exception as e:
            print_error(f"{test_name}: Exception - {e}")
            failed += 1
        
        time.sleep(0.5)  # Rate limiting
    
    print_info(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0

def test_invalid_inputs():
    """Test invalid input handling"""
    print_header("Testing Invalid Input Handling")
    
    passed = 0
    failed = 0
    
    for test_name, test_data in invalid_test_cases.items():
        try:
            response = requests.post(
                f"{API_BASE_URL}/recommend",
                json=test_data,
                timeout=10
            )
            
            # Should return error status (400 or 500)
            if response.status_code in [400, 422, 500]:
                data = response.json()
                if not data.get('success'):
                    print_success(f"{test_name}: Correctly rejected")
                    passed += 1
                else:
                    print_error(f"{test_name}: Should have been rejected")
                    failed += 1
            else:
                print_error(
                    f"{test_name}: Got unexpected status {response.status_code}"
                )
                failed += 1
                
        except Exception as e:
            print_error(f"{test_name}: Exception - {e}")
            failed += 1
        
        time.sleep(0.5)
    
    print_info(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0

def test_crops_endpoint():
    """Test crops information endpoint"""
    print_header("Testing Crops Endpoint")
    
    try:
        response = requests.get(f"{API_BASE_URL}/crops", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            crops = data['data']['crops']
            
            print_success(f"Retrieved {len(crops)} crops")
            print_info(f"Crops: {', '.join(crops)}")
            return True
        else:
            print_error(f"Failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Exception: {e}")
        return False

def test_stats_endpoint():
    """Test statistics endpoint"""
    print_header("Testing Statistics Endpoint")
    
    try:
        response = requests.get(f"{API_BASE_URL}/stats", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            stats = data['data']
            
            print_success("Retrieved API statistics")
            print_info(f"Total Crops: {stats['total_crops']}")
            print_info(f"Model Type: {stats['model_type']}")
            print_info(f"Features: {', '.join(stats['features'])}")
            return True
        else:
            print_error(f"Failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Exception: {e}")
        return False

def test_performance():
    """Test API response time"""
    print_header("Testing API Performance")
    
    test_data = test_cases["Rice Growing Conditions"].copy()
    test_data.pop("expected_crop")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{API_BASE_URL}/recommend",
            json=test_data,
            timeout=10
        )
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            print_success(f"API responded in {elapsed_time:.3f} seconds")
            
            if elapsed_time < 1:
                print_success("Response time is excellent (< 1s)")
            elif elapsed_time < 2:
                print_info("Response time is good (< 2s)")
            else:
                print_error("Response time is slow (> 2s)")
            
            return True
        else:
            print_error(f"Request failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Exception: {e}")
        return False

def test_concurrent_requests():
    """Test API with multiple concurrent requests"""
    print_header("Testing Concurrent Requests")
    
    import concurrent.futures
    
    test_data = test_cases["Rice Growing Conditions"].copy()
    test_data.pop("expected_crop")
    
    def make_request():
        try:
            response = requests.post(
                f"{API_BASE_URL}/recommend",
                json=test_data,
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
    
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(5)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        success_count = sum(results)
        print_success(f"Successfully handled {success_count}/5 concurrent requests")
        return success_count == 5
    except Exception as e:
        print_error(f"Concurrent test failed: {e}")
        return False

def main():
    """Run all tests"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║   Crop Recommendation System - API Test Suite              ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")
    
    print_info(f"API Base URL: {API_BASE_URL}")
    print_info("Starting tests...\n")
    
    results = {
        "Health Check": test_health(),
        "Valid Recommendations": test_valid_recommendations(),
        "Invalid Input Handling": test_invalid_inputs(),
        "Crops Endpoint": test_crops_endpoint(),
        "Stats Endpoint": test_stats_endpoint(),
        "Performance": test_performance(),
        "Concurrent Requests": test_concurrent_requests()
    }
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = f"{Colors.OKGREEN}PASS{Colors.ENDC}" if result else f"{Colors.FAIL}FAIL{Colors.ENDC}"
        print(f"{test_name}: {status}")
    
    print_info(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print_success("All tests passed! ✨")
    else:
        print_error(f"{total - passed} test(s) failed")
    
    print(f"\n{Colors.ENDC}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_error("\n\nTests interrupted by user")
    except Exception as e:
        print_error(f"\n\nUnexpected error: {e}")
