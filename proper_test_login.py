#!/usr/bin/env python
"""Proper login test"""

from app import create_app
from models import User, db

app = create_app()

with app.app_context():
    # Check user first
    user = User.query.filter_by(email='demo@example.com').first()
    print('✓ User in database:')
    print(f'  Email: {user.email}')
    print(f'  Full Name: {user.full_name}')
    print(f'  Active: {user.active}')
    print(f'  Password Check: {user.check_password("demo123")}')
    print()
    
    # Now test with proper test client
    with app.test_client() as client:
        # First get the login page to extract CSRF token (if needed)
        login_page = client.get('/login')
        
        # Post the login
        response = client.post('/login', data={
            'email': 'demo@example.com',
            'password': 'demo123'
        }, follow_redirects=True)
        
        print('✓ Login Response:')
        print(f'  Status: {response.status_code}')
        
        # Check if login was successful by checking for dashboard/inspections content
        response_text = response.data.decode('utf-8', errors='ignore')
        
        if 'Building Inspections' in response_text or 'Log Out' in response_text:
            print('  ✓ LOGIN SUCCESSFUL - User authenticated!')
        elif 'pending approval' in response_text:
            print('  ✗ Account pending approval')
        elif 'incorrect' in response_text.lower():
            print('  ✗ Incorrect credentials')
        else:
            print('  ? Unknown response')
            # Check what page we're on
            if '/login' in response.request.url:
                print('  Still on login page')
            elif '/dashboard' in response.request.url or '/inspections' in response.request.url:
                print('  Redirected to dashboard/inspections - LOGIN SUCCESSFUL!')
