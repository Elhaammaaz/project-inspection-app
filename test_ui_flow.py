"""
UI/UX Flow Test - Check all buttons and pages
Tests the complete user workflow through the application
"""

import requests
from requests.sessions import Session
import json

BASE_URL = 'http://127.0.0.1:5000'
session = Session()

def test_page_loads(endpoint, name):
    """Test if a page loads without errors"""
    try:
        response = session.get(f'{BASE_URL}{endpoint}')
        status = '✅' if response.status_code == 200 else '❌'
        print(f'{status} {name:30} - Status: {response.status_code}')
        
        # Check for common error indicators
        if '500' in response.text or 'BuildError' in response.text or 'TemplateNotFound' in response.text:
            print(f'   ERROR: {response.text[:100]}')
            return False
        return True
    except Exception as e:
        print(f'❌ {name:30} - Error: {str(e)[:50]}')
        return False

def test_login():
    """Test login form submission"""
    print('\n=== TESTING LOGIN FORM ===')
    
    # Get login page to extract CSRF token
    response = session.get(f'{BASE_URL}/login')
    if 'csrf_token' in response.text:
        print('✅ CSRF token found on login page')
    
    # Try login with demo account
    login_data = {
        'username': 'demo',
        'password': 'demo123'
    }
    
    response = session.post(f'{BASE_URL}/login', data=login_data, allow_redirects=True)
    
    if response.status_code == 200 and 'dashboard' in response.url:
        print('✅ Login successful - redirected to dashboard')
        return True
    else:
        print(f'❌ Login failed - Status: {response.status_code}, URL: {response.url}')
        return False

print('=' * 60)
print('BCAR APPLICATION - UI/UX FLOW TEST')
print('=' * 60)

print('\n=== TESTING UNAUTHENTICATED PAGES ===')
test_page_loads('/', 'Home/Index')
test_page_loads('/login', 'Login')
test_page_loads('/register', 'Register')

print('\n=== TESTING AUTHENTICATED PAGES (BEFORE LOGIN) ===')
test_page_loads('/dashboard', 'Dashboard')
test_page_loads('/building/1', 'View Building')
test_page_loads('/building/new', 'New Building')

print('\n=== TESTING LOGIN FLOW ===')
if test_login():
    print('\n=== TESTING AUTHENTICATED PAGES (AFTER LOGIN) ===')
    test_page_loads('/dashboard', 'Dashboard')
    test_page_loads('/building/new', 'New Building Form')
    test_page_loads('/logout', 'Logout')

print('\n' + '=' * 60)
print('UI/UX FLOW TEST COMPLETE')
print('=' * 60)
