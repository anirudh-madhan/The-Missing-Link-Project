"""
Test script for authentication and registration functionality
Run this after starting the Flask server to verify all fixes
"""

import requests
import json
from datetime import datetime, timedelta

API_BASE_URL = 'http://localhost:5000/api'

def test_patient_registration():
    """Test patient registration with date of birth"""
    print("\n=== Testing Patient Registration ===")
    
    # Calculate a valid date of birth (25 years ago)
    dob = (datetime.now() - timedelta(days=25*365)).strftime('%Y-%m-%d')
    
    test_user = {
        'email': f'test_patient_{datetime.now().timestamp()}@test.com',
        'password': 'testpass123',
        'full_name': 'Test Patient',
        'phone': '+91-9999999999',
        'date_of_birth': dob,
        'language_preference': 'en',
        'accessibility_needs': 'Wheelchair access required'
    }
    
    try:
        response = requests.post(f'{API_BASE_URL}/auth/register', json=test_user)
        data = response.json()
        
        if response.status_code == 201:
            print("✓ Registration successful")
            print(f"  User ID: {data['user']['id']}")
            print(f"  Email: {data['user']['email']}")
            print(f"  Date of Birth: {data['user']['date_of_birth']}")
            print(f"  Token received: {data['access_token'][:20]}...")
            return data['access_token'], data['user']
        else:
            print(f"✗ Registration failed: {data.get('error')}")
            return None, None
    except Exception as e:
        print(f"✗ Registration error: {str(e)}")
        return None, None


def test_patient_login():
    """Test patient login with demo credentials"""
    print("\n=== Testing Patient Login ===")
    
    credentials = {
        'email': 'john.doe@email.com',
        'password': 'patient123'
    }
    
    try:
        response = requests.post(f'{API_BASE_URL}/auth/login', json=credentials)
        data = response.json()
        
        if response.status_code == 200:
            print("✓ Patient login successful")
            print(f"  User: {data['user']['full_name']}")
            print(f"  Email: {data['user']['email']}")
            print(f"  Is Admin: {data['user']['is_admin']}")
            print(f"  Token received: {data['access_token'][:20]}...")
            return data['access_token'], data['user']
        else:
            print(f"✗ Patient login failed: {data.get('error')}")
            return None, None
    except Exception as e:
        print(f"✗ Login error: {str(e)}")
        return None, None


def test_admin_login():
    """Test admin login with demo credentials"""
    print("\n=== Testing Admin Login ===")
    
    credentials = {
        'email': 'admin@hospital.com',
        'password': 'admin123'
    }
    
    try:
        response = requests.post(f'{API_BASE_URL}/auth/login', json=credentials)
        data = response.json()
        
        if response.status_code == 200:
            print("✓ Admin login successful")
            print(f"  User: {data['user']['full_name']}")
            print(f"  Email: {data['user']['email']}")
            print(f"  Is Admin: {data['user']['is_admin']}")
            print(f"  Token received: {data['access_token'][:20]}...")
            return data['access_token'], data['user']
        else:
            print(f"✗ Admin login failed: {data.get('error')}")
            return None, None
    except Exception as e:
        print(f"✗ Login error: {str(e)}")
        return None, None


def test_protected_route(token, route_name, endpoint):
    """Test accessing protected routes with JWT token"""
    print(f"\n=== Testing Protected Route: {route_name} ===")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get(f'{API_BASE_URL}{endpoint}', headers=headers)
        data = response.json()
        
        if response.status_code == 200:
            print(f"✓ {route_name} access successful")
            return True
        else:
            print(f"✗ {route_name} access failed: {data.get('error')}")
            return False
    except Exception as e:
        print(f"✗ {route_name} error: {str(e)}")
        return False


def test_date_validation():
    """Test date of birth validation (no future dates)"""
    print("\n=== Testing Date Validation ===")
    
    # Try to register with future date
    future_date = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
    
    test_user = {
        'email': f'future_test_{datetime.now().timestamp()}@test.com',
        'password': 'testpass123',
        'full_name': 'Future Test',
        'date_of_birth': future_date
    }
    
    try:
        response = requests.post(f'{API_BASE_URL}/auth/register', json=test_user)
        data = response.json()
        
        # This should succeed at backend level, but frontend should prevent it
        if response.status_code == 201:
            print("⚠ Future date was accepted (frontend should prevent this)")
            return False
        else:
            print(f"✓ Date validation working: {data.get('error')}")
            return True
    except Exception as e:
        print(f"✗ Validation test error: {str(e)}")
        return False


def main():
    print("=" * 60)
    print("THE MISSING LINK - AUTHENTICATION TEST SUITE")
    print("=" * 60)
    
    # Test 1: Patient Registration
    new_token, new_user = test_patient_registration()
    
    # Test 2: Patient Login
    patient_token, patient_user = test_patient_login()
    
    # Test 3: Admin Login
    admin_token, admin_user = test_admin_login()
    
    # Test 4: Protected Routes with Patient Token
    if patient_token:
        test_protected_route(patient_token, "Profile", "/auth/profile")
        test_protected_route(patient_token, "Hospitals", "/hospitals")
        test_protected_route(patient_token, "Appointments", "/appointments")
    
    # Test 5: Admin Protected Routes
    if admin_token:
        test_protected_route(admin_token, "Admin Stats", "/admin/stats")
    
    # Test 6: Date Validation
    test_date_validation()
    
    print("\n" + "=" * 60)
    print("TEST SUITE COMPLETE")
    print("=" * 60)


if __name__ == '__main__':
    main()
