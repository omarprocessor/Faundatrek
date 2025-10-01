#!/usr/bin/env python3
"""
Simple test script for FaundaTrek API without authentication
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000/api"

def test_endpoints():
    print("🚀 Testing FaundaTrek API (No Auth Required)")
    print("=" * 60)
    
    # Test 1: Get Stories List
    print("\n1. Testing Stories List (GET)...")
    try:
        response = requests.get(f"{BASE_URL}/stories/")
        if response.status_code == 200:
            print("✅ Stories list retrieved successfully!")
            data = response.json()
            print(f"   Total stories: {data.get('count', 0)}")
            print(f"   Page size: {data.get('page_size', 0)}")
        else:
            print(f"❌ Stories list failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Create a Story
    print("\n2. Testing Story Creation (POST)...")
    story_data = {
        "content": "This is a test story created without authentication!"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/stories/", json=story_data)
        if response.status_code == 201:
            print("✅ Story created successfully!")
            story_response = response.json()
            print(f"   Story ID: {story_response.get('id', 'N/A')}")
            print(f"   Content: {story_response.get('content', 'N/A')}")
        else:
            print(f"❌ Story creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Get Pitches List
    print("\n3. Testing Pitches List (GET)...")
    try:
        response = requests.get(f"{BASE_URL}/pitches/")
        if response.status_code == 200:
            print("✅ Pitches list retrieved successfully!")
            data = response.json()
            print(f"   Total pitches: {data.get('count', 0)}")
        else:
            print(f"❌ Pitches list failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Create a Pitch
    print("\n4. Testing Pitch Creation (POST)...")
    pitch_data = {
        "title": "Test Startup Pitch",
        "description": "This is a test pitch created without authentication!",
        "funding_goal": "10000.00"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/pitches/", json=pitch_data)
        if response.status_code == 201:
            print("✅ Pitch created successfully!")
            pitch_response = response.json()
            print(f"   Pitch ID: {pitch_response.get('id', 'N/A')}")
            print(f"   Title: {pitch_response.get('title', 'N/A')}")
            print(f"   Funding Goal: ${pitch_response.get('funding_goal', 'N/A')}")
        else:
            print(f"❌ Pitch creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: Get Donations List
    print("\n5. Testing Donations List (GET)...")
    try:
        response = requests.get(f"{BASE_URL}/donations/")
        if response.status_code == 200:
            print("✅ Donations list retrieved successfully!")
            data = response.json()
            print(f"   Total donations: {data.get('count', 0)}")
        else:
            print(f"❌ Donations list failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 6: Get Messages List
    print("\n6. Testing Messages List (GET)...")
    try:
        response = requests.get(f"{BASE_URL}/messages/")
        if response.status_code == 200:
            print("✅ Messages list retrieved successfully!")
            data = response.json()
            print(f"   Total messages: {data.get('count', 0)}")
        else:
            print(f"❌ Messages list failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 7: Test Search and Filtering
    print("\n7. Testing Search and Filtering...")
    try:
        response = requests.get(f"{BASE_URL}/stories/?search=test&ordering=-created_at")
        if response.status_code == 200:
            print("✅ Search and filtering working!")
            data = response.json()
            print(f"   Found {data.get('count', 0)} stories with 'test'")
        else:
            print(f"❌ Search failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 API testing completed (No Authentication Required)!")
    print(f"📱 API is running at: {BASE_URL}")
    print(f"🔐 Admin interface: http://localhost:8000/admin/")
    print("   Username: admin")
    print("   Password: admin123")

if __name__ == "__main__":
    test_endpoints()
