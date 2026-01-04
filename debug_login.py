#!/usr/bin/env python
"""Debug login"""

from app import create_app
from models import User

app = create_app()

with app.test_client() as client:
    response = client.post('/login', data={
        'email': 'demo@example.com',
        'password': 'demo123'
    }, follow_redirects=True)
    
    print('Response status:', response.status_code)
    print('Response URL:', response.request.url if hasattr(response, 'request') else 'N/A')
    
    # Check for keywords
    if b'pending approval' in response.data:
        print('✗ Found: "pending approval" message - User is not active')
    elif b'dashboard' in response.data.lower() or b'inspections' in response.data.lower():
        print('✓ Found: dashboard/inspections - Login successful')
    elif b'Sign In' in response.data or b'login' in response.data.lower():
        print('? Still on login page - Check for errors:')
        if b'incorrect' in response.data.lower():
            print('  - Incorrect credentials message found')
        elif b'error' in response.data.lower():
            print('  - Error message found')
        else:
            print('  - No specific error message')
    
    # Print part of the response
    print('\nResponse snippet:')
    resp_text = response.data.decode('utf-8', errors='ignore')
    if 'pending approval' in resp_text:
        start = resp_text.find('pending approval') - 50
        end = resp_text.find('pending approval') + 80
        print(resp_text[max(0, start):end])
