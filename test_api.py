#!/usr/bin/env python3
"""
Test script for FaundaTrek API
This script demonstrates the basic functionality of the API endpoints
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000/api"

def test_api():
    print("🚀 Testing FaundaTrek API")
    print("=" * 50)
    
    # Test 1: User Registration
    print("\n1. Testing User Registration...")
    register_data = {
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "testpass123",
        "confirm_password": "testpass123",
        "first_name": "Test",
        "last_name": "User2",
        "role": "entrepreneur"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register/", json=register_data)
        if response.status_code == 201:
            print("✅ User registration successful!")
            user_data = response.json()
            access_token = user_data['access']
            user_id = user_data['user']['id']
            print(f"   User ID: {user_id}")
            print(f"   Access Token: {access_token[:50]}...")
        else:
            print(f"❌ User registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return
    
    # Test 2: User Login
    print("\n2. Testing User Login...")
    login_data = {
        "username": "testuser2",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        if response.status_code == 200:
            print("✅ User login successful!")
            login_response = response.json()
            access_token = login_response['access']
            print(f"   Access Token: {access_token[:50]}...")
        else:
            print(f"❌ User login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return
    
    # Test 3: Create a Story
    print("\n3. Testing Story Creation...")
    headers = {"Authorization": f"Bearer {access_token}"}
    story_data = {
        "content": "This is a test story about entrepreneurship and innovation!"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/stories/", json=story_data, headers=headers)
        if response.status_code == 201:
            print("✅ Story creation successful!")
            story_response = response.json()
            story_id = story_response['id']
            print(f"   Story ID: {story_id}")
            print(f"   Content: {story_response['content'][:50]}...")
        else:
            print(f"❌ Story creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return
    
    # Test 4: Get Stories List
    print("\n4. Testing Stories List...")
    try:
        response = requests.get(f"{BASE_URL}/stories/", headers=headers)
        if response.status_code == 200:
            print("✅ Stories list retrieved successfully!")
            stories_response = response.json()
            print(f"   Total stories: {stories_response['count']}")
            print(f"   Page size: {stories_response['page_size']}")
            if stories_response['results']:
                first_story = stories_response['results'][0]
                print(f"   First story: {first_story['content'][:50]}...")
        else:
            print(f"❌ Stories list failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
    
    # Test 5: Create a Pitch
    print("\n5. Testing Pitch Creation...")
    pitch_data = {
        "title": "Innovative Tech Startup",
        "description": "A revolutionary technology platform that will change the world!",
        "funding_goal": "50000.00"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/pitches/", json=pitch_data, headers=headers)
        if response.status_code == 201:
            print("✅ Pitch creation successful!")
            pitch_response = response.json()
            pitch_id = pitch_response['id']
            print(f"   Pitch ID: {pitch_id}")
            print(f"   Title: {pitch_response['title']}")
            print(f"   Funding Goal: ${pitch_response['funding_goal']}")
        else:
            print(f"❌ Pitch creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
    
    # Test 6: Get User Profile
    print("\n6. Testing User Profile...")
    try:
        response = requests.get(f"{BASE_URL}/profile/{user_id}/", headers=headers)
        if response.status_code == 200:
            print("✅ User profile retrieved successfully!")
            profile_response = response.json()
            print(f"   Username: {profile_response['username']}")
            print(f"   Role: {profile_response['role']}")
            print(f"   Email: {profile_response['email']}")
        else:
            print(f"❌ User profile failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API testing completed!")
    print(f"📱 API is running at: {BASE_URL}")
    print(f"🔐 Admin interface: http://localhost:8000/admin/")
    print("   Username: admin")
    print("   Password: admin123")

if __name__ == "__main__":
    test_api()
