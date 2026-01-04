#!/usr/bin/env python
"""Quick test of login"""

from app import create_app
from models import User

app = create_app()

# Test login
with app.test_client() as client:
    # Try to login with demo credentials
    response = client.post('/login', data={
        'email': 'demo@example.com',
        'password': 'demo123'
    }, follow_redirects=True)
    
    print('✓ Login Test:')
    print(f'  Status Code: {response.status_code}')
    
    if response.status_code == 200:
        # Check if we got to the inspections page (contains specific text)
        if b'Building Inspections' in response.data or b'dashboard' in response.data.lower():
            print('  ✓ Login SUCCESSFUL - Redirected to dashboard')
        else:
            print('  ✗ Login failed - Still on login page')
            # Print error message if any
            if b'pending approval' in response.data:
                print('  Error: "Your account is pending approval"')
    else:
        print(f'  ✗ Unexpected status: {response.status_code}')
