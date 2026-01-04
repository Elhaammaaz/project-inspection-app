#!/usr/bin/env python
"""Debug login issue"""

from app import create_app
from models import User
import re

app = create_app()

# First verify user in DB
with app.app_context():
    user = User.query.filter_by(email='demo@example.com').first()
    print('Database check:')
    print(f'  User exists: {user is not None}')
    if user:
        print(f'  Email: {user.email}')
        print(f'  Active: {user.active}')
        print(f'  Password check (demo123): {user.check_password("demo123")}')
    print()

# Now test login
with app.test_client() as client:
    # Step 1: Get CSRF token
    login_page = client.get('/login')
    html = login_page.data.decode('utf-8')
    csrf_match = re.search(r'name="csrf_token"\s*value="([^"]*)"', html)
    csrf_token = csrf_match.group(1) if csrf_match else None
    
    print('Login form:')
    print(f'  CSRF token found: {csrf_token is not None}')
    if csrf_token:
        print(f'  Token: {csrf_token[:30]}...')
    print()
    
    # Step 2: Post login
    print('Login attempt:')
    login_data = {'email': 'demo@example.com', 'password': 'demo123'}
    if csrf_token:
        login_data['csrf_token'] = csrf_token
    
    response = client.post('/login', data=login_data, follow_redirects=False)
    print(f'  Response status: {response.status_code}')
    print(f'  Redirect location: {response.location}')
    
    # If redirected, check where
    if response.status_code in [301, 302, 303, 307, 308]:
        if 'dashboard' in response.location:
            print('  ✅ Redirected to dashboard - LOGIN SUCCESS')
        else:
            print(f'  Redirected to: {response.location}')
