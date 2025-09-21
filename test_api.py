#!/usr/bin/env python3
"""
Test script for the pre-computed Smart Factory Energy Optimizer API
"""

import json
import urllib.request
import sys

def test_api(base_url="http://localhost:8000"):
    """Test the API endpoints"""
    
    print(f"Testing API at: {base_url}")
    
    # Test 1: Health check
    try:
        response = urllib.request.urlopen(f"{base_url}/health")
        health_data = json.loads(response.read().decode())
        print("✅ Health check:", health_data)
    except Exception as e:
        print("❌ Health check failed:", e)
        return False
    
    # Test 2: Root endpoint
    try:
        response = urllib.request.urlopen(f"{base_url}/")
        root_data = json.loads(response.read().decode())
        print("✅ Root endpoint:", root_data)
    except Exception as e:
        print("❌ Root endpoint failed:", e)
    
    # Test 3: Prediction endpoint
    try:
        # Test data
        test_data = {
            "machine": "Machine_A",
            "hour": 14,
            "day": 3,
            "temperature": 25.0,
            "humidity": 60.0
        }
        
        # Create request
        data = json.dumps(test_data).encode('utf-8')
        req = urllib.request.Request(
            f"{base_url}/predict",
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        response = urllib.request.urlopen(req)
        prediction_data = json.loads(response.read().decode())
        print("✅ Prediction test:", prediction_data)
        
        # Validate response structure
        required_fields = ["predicted_energy", "machine", "timestamp"]
        for field in required_fields:
            if field not in prediction_data:
                print(f"❌ Missing field in response: {field}")
                return False
        
        print(f"🎯 Predicted energy consumption: {prediction_data['predicted_energy']} kWh")
        return True
        
    except Exception as e:
        print("❌ Prediction test failed:", e)
        return False

if __name__ == "__main__":
    # Test with local URL by default, accept URL as command line argument
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    print("=" * 60)
    print("Smart Factory Energy Optimizer API Test")
    print("=" * 60)
    
    success = test_api(url)
    
    if success:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("💥 Some tests failed. Check the API implementation.")
        sys.exit(1)