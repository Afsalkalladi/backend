#!/usr/bin/env python3
"""
EESA Backend API Test Script
Test the main API endpoints to ensure everything is working correctly.
"""

import json
import requests
import sys

BASE_URL = "http://127.0.0.1:8000/api"

def test_api():
    print("🚀 Testing EESA Backend API...")
    
    # Test 1: User Registration
    print("\n1. Testing User Registration...")
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "role": "student",
        "first_name": "Test",
        "last_name": "User",
        "full_name": "Test User",
        "scheme": 2023,
        "year_of_joining": 2023,
        "expected_year_of_passout": 2027,
        "ongoing_semester": 2
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register/", json=register_data)
        if response.status_code == 201:
            print("✅ Registration successful!")
            data = response.json()
            access_token = data['tokens']['access']
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(response.text)
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the server is running on port 8000.")
        return False
    
    # Test 2: User Login
    print("\n2. Testing User Login...")
    login_data = {
        "username_or_email": "testuser",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
    if response.status_code == 200:
        print("✅ Login successful!")
        data = response.json()
        access_token = data['tokens']['access']
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(response.text)
        return False
    
    # Headers for authenticated requests
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Test 3: Get Profile
    print("\n3. Testing Profile Retrieval...")
    response = requests.get(f"{BASE_URL}/auth/profile/", headers=headers)
    if response.status_code == 200:
        print("✅ Profile retrieval successful!")
        profile = response.json()
        print(f"   User: {profile['username']} ({profile['role']})")
    else:
        print(f"❌ Profile retrieval failed: {response.status_code}")
        return False
    
    # Test 4: Get Subjects
    print("\n4. Testing Subjects API...")
    response = requests.get(f"{BASE_URL}/academics/subjects/?scheme=2023&semester=1", headers=headers)
    if response.status_code == 200:
        print("✅ Subjects API working!")
        data = response.json()
        print(f"   Found {len(data['subjects'])} subjects for Scheme 2023, Semester 1")
    else:
        print(f"❌ Subjects API failed: {response.status_code}")
        return False
    
    # Test 5: Get Projects
    print("\n5. Testing Projects API...")
    response = requests.get(f"{BASE_URL}/projects/", headers=headers)
    if response.status_code == 200:
        print("✅ Projects API working!")
        data = response.json()
        print(f"   Found {len(data['projects'])} projects")
    else:
        print(f"❌ Projects API failed: {response.status_code}")
        return False
    
    # Test 6: Get Events
    print("\n6. Testing Events API...")
    response = requests.get(f"{BASE_URL}/events/upcoming/")  # Public endpoint
    if response.status_code == 200:
        print("✅ Events API working!")
        data = response.json()
        print(f"   Found {len(data['upcoming_events'])} upcoming events")
    else:
        print(f"❌ Events API failed: {response.status_code}")
        return False
    
    print("\n🎉 All API tests passed successfully!")
    print("\n📋 API Endpoints Summary:")
    print("   • Authentication: /api/auth/")
    print("   • Students: /api/students/")
    print("   • Academics: /api/academics/")
    print("   • Projects: /api/projects/")
    print("   • Events: /api/events/")
    print("\n🌐 Admin Panel: http://127.0.0.1:8000/admin/")
    print("🔍 API Browser: http://127.0.0.1:8000/api/")
    
    return True

if __name__ == "__main__":
    success = test_api()
    if not success:
        print("\n❌ Some tests failed. Check the server logs for details.")
        sys.exit(1)
    else:
        print("\n✅ All tests passed! EESA Backend is ready for development.")
        sys.exit(0)
