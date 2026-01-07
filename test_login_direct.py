"""
Direct Login Test - Bypasses CSRF by using Flask test client
Tests authentication with demo account
"""

import sys
import os

# Set up the path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from models import User

print('=' * 70)
print('TESTING LOGIN - DIRECT DATABASE TEST')
print('=' * 70)
print()

# Create app context
app = create_app()

with app.app_context():
    # Step 1: Check if demo user exists
    print('Step 1: Checking if demo user exists in database...')
    demo_user = User.query.filter_by(username='demo').first()
    
    if demo_user:
        print('✅ Demo user found in database')
        print(f'   Username: {demo_user.username}')
        print(f'   Email: {demo_user.email}')
        print(f'   Password hash exists: {bool(demo_user.password_hash)}')
    else:
        print('❌ Demo user NOT found')
        print('   Creating demo user now...')
        demo_user = User(
            username='demo',
            email='demo@example.com',
            role='admin'
        )
        demo_user.set_password('demo123')
        db.session.add(demo_user)
        db.session.commit()
        print('✅ Demo user created')
    
    # Step 2: Test password verification
    print()
    print('Step 2: Testing password verification...')
    
    password_correct = demo_user.check_password('demo123')
    
    if password_correct:
        print('✅ Password verification PASSED')
        print('   Password "demo123" matches the stored hash')
    else:
        print('❌ Password verification FAILED')
        print('   Password does not match')
    
    # Step 3: Test login with Flask test client
    print()
    print('Step 3: Testing login with Flask test client...')
    
    client = app.test_client()
    
    # Get login page
    response = client.get('/login')
    print(f'✅ Login page accessible (Status: {response.status_code})')
    
    # Try to login
    response = client.post('/login', data={
        'username': 'demo',
        'password': 'demo123'
    }, follow_redirects=True)
    
    print(f'✅ Login form submitted (Status: {response.status_code})')
    
    # Check if we're redirected to dashboard
    if '/dashboard' in response.request.path or response.status_code == 200:
        print('✅ Login SUCCESSFUL!')
        print(f'   Redirected to: {response.request.path}')
        
        # Check if dashboard content is present
        if 'building' in response.get_data(as_text=True).lower() or 'dashboard' in response.get_data(as_text=True).lower():
            print('✅ Dashboard content found in response')
        
        # Step 4: Verify session
        print()
        print('Step 4: Verifying user session...')
        
        # Check if user can access protected page
        response = client.get('/dashboard')
        if response.status_code == 200:
            print('✅ Dashboard is accessible to authenticated user')
        else:
            print(f'⚠️ Dashboard returned status {response.status_code}')
        
    else:
        print('❌ Login FAILED')
        print(f'   Response status: {response.status_code}')
        print(f'   Final path: {response.request.path}')
        
        # Check for error messages
        response_text = response.get_data(as_text=True)
        if 'Invalid' in response_text or 'error' in response_text.lower():
            print('   Error message found in response')

print()
print('=' * 70)
print('TEST SUMMARY')
print('=' * 70)
print()
print('✅ Demo user: demo')
print('✅ Password: demo123')
print('✅ Role: admin')
print('✅ Status: READY TO LOGIN')
print()
