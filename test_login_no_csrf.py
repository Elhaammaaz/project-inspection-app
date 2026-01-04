#!/usr/bin/env python
"""Login test with CSRF disabled"""

from app import create_app

app = create_app()
app.config['WTF_CSRF_ENABLED'] = False

with app.test_client() as client:
    # Post login
    response = client.post('/login', data={
        'email': 'demo@example.com',
        'password': 'demo123'
    }, follow_redirects=False)
    
    print('Login without CSRF:')
    print(f'  Status: {response.status_code}')
    print(f'  Location: {response.location}')
    
    if response.status_code in [301, 302, 303, 307, 308]:
        if 'dashboard' in response.location:
            print('\n✅ LOGIN SUCCESSFUL!')
            print('Demo user demo@example.com can now login with password: demo123')
        else:
            print(f'\nRedirect to: {response.location}')
