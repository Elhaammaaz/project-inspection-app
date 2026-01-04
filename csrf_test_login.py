#!/usr/bin/env python
"""Login test with CSRF token extraction"""

from app import create_app
from models import User
import re

app = create_app()

with app.test_client() as client:
    # Step 1: Get login page and extract CSRF token
    print('Step 1: Getting login page...')
    response = client.get('/login')
    
    # Extract CSRF token from the HTML
    html = response.data.decode('utf-8')
    csrf_match = re.search(r'<input[^>]*name="csrf_token"[^>]*value="([^"]*)"', html)
    
    if csrf_match:
        csrf_token = csrf_match.group(1)
        print(f'  ✓ Found CSRF token: {csrf_token[:20]}...')
    else:
        print('  ✗ CSRF token not found')
        csrf_token = None
    
    # Step 2: Try login with CSRF token
    print('\nStep 2: Posting login form...')
    login_data = {
        'email': 'demo@example.com',
        'password': 'demo123'
    }
    
    if csrf_token:
        login_data['csrf_token'] = csrf_token
    
    response = client.post('/login', data=login_data, follow_redirects=True)
    
    print(f'  Status: {response.status_code}')
    print(f'  Final URL: {response.request.url}')
    
    # Check result
    if 'dashboard' in response.request.url.lower() or 'inspections' in response.request.url.lower():
        print('\n✅ LOGIN SUCCESSFUL!')
        print('Demo user (demo@example.com) can now login with password: demo123')
    elif 'login' in response.request.url.lower():
        print('\n❌ Still on login page')
        # Look for error message
        html = response.data.decode('utf-8')
        if 'pending approval' in html.lower():
            print('Error: Account pending approval')
        elif 'incorrect' in html.lower():
            print('Error: Incorrect credentials')
        else:
            print('Error: Unknown')
    else:
        print('\n? Unknown redirect')
