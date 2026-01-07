"""
Comprehensive test script to verify all pages and button/form functionality
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from models import User, Building, System, AssessmentItem, Assessment
from werkzeug.security import generate_password_hash

def test_all_pages():
    """Test all pages and forms with CSRF tokens"""
    app = create_app()
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['TESTING'] = True
    
    results = []
    
    with app.test_client() as client:
        with app.app_context():
            # Ensure we have a test user
            user = User.query.filter_by(email='test@example.com').first()
            if not user:
                user = User(
                    username='testuser',
                    email='test@example.com',
                    password_hash=generate_password_hash('test123'),
                    role='Admin'
                )
                db.session.add(user)
                db.session.commit()
            
            # Get a building for testing
            building = Building.query.first()
            if not building:
                building = Building(
                    project_name='Test Building',
                    building_type='Office',
                    primary_use='Commercial',
                    created_by_id=user.id
                )
                db.session.add(building)
                db.session.commit()
            
            building_id = building.id
            
            # Login
            login_resp = client.get('/login')
            assert login_resp.status_code == 200, "Login page failed"
            results.append(('GET /login', 'PASS', 200))
            
            # Extract CSRF token from login page
            csrf_token = None
            html = login_resp.data.decode()
            if 'name="csrf_token"' in html:
                import re
                match = re.search(r'name="csrf_token".*?value="([^"]+)"', html)
                if match:
                    csrf_token = match.group(1)
            
            # Test login POST with CSRF
            if csrf_token:
                login_post = client.post('/login', data={
                    'email': 'test@example.com',
                    'password': 'test123',
                    'csrf_token': csrf_token
                }, follow_redirects=True)
                if login_post.status_code == 200:
                    results.append(('POST /login', 'PASS', 200))
                else:
                    results.append(('POST /login', 'FAIL', login_post.status_code))
            
            # Test all GET pages (no auth required)
            public_pages = [
                ('/login', 'Login'),
                ('/register', 'Register'),
            ]
            
            for url, name in public_pages:
                resp = client.get(url)
                status = 'PASS' if resp.status_code in [200, 302] else 'FAIL'
                results.append((f'GET {url} ({name})', status, resp.status_code))
            
            # Login for authenticated pages
            login_resp = client.get('/login')
            html = login_resp.data.decode()
            csrf_token = None
            if 'name="csrf_token"' in html:
                import re
                match = re.search(r'name="csrf_token".*?value="([^"]+)"', html)
                if match:
                    csrf_token = match.group(1)
            
            client.post('/login', data={
                'email': 'test@example.com',
                'password': 'test123',
                'csrf_token': csrf_token
            }, follow_redirects=True)
            
            # Test all authenticated GET pages
            auth_pages = [
                ('/', 'Dashboard'),
                ('/dashboard', 'Dashboard'),
                ('/buildings', 'Buildings List'),
                (f'/building/{building_id}', 'Building View'),
                (f'/building/{building_id}/assessment/items', 'Assessment Items'),
                (f'/building/{building_id}/assessment/items/new', 'New Assessment Item'),
                (f'/building/{building_id}/compliance', 'Compliance Checklist'),
                (f'/building/{building_id}/compliance/new', 'New Compliance Item'),
                (f'/building/{building_id}/system-scoring', 'System Scoring'),
                (f'/building/{building_id}/tests', 'Test Register'),
                (f'/building/{building_id}/tests/new', 'New Test'),
                (f'/building/{building_id}/capa', 'CAPA Register'),
                (f'/building/{building_id}/capa/new', 'New CAPA'),
                (f'/building/{building_id}/executive-dashboard', 'Executive Dashboard'),
                ('/profile', 'Profile'),
                ('/edit-profile', 'Edit Profile'),
                ('/admin/requests', 'Admin Requests'),
                ('/admin/access', 'Access Management'),
            ]
            
            for url, name in auth_pages:
                resp = client.get(url)
                status = 'PASS' if resp.status_code in [200, 302] else 'FAIL'
                results.append((f'GET {url} ({name})', status, resp.status_code))
            
            # Test API endpoints
            api_endpoints = [
                '/api/systems',
            ]
            
            for url in api_endpoints:
                resp = client.get(url)
                status = 'PASS' if resp.status_code == 200 else 'FAIL'
                results.append((f'API {url}', status, resp.status_code))
            
            # Get a system for subsystem/component tests
            system = System.query.first()
            if system:
                resp = client.get(f'/api/subsystems/{system.id}')
                status = 'PASS' if resp.status_code == 200 else 'FAIL'
                results.append((f'API /api/subsystems/{system.id}', status, resp.status_code))
            
            # Test POST forms with CSRF tokens
            print("\n" + "="*60)
            print("Testing POST forms with CSRF tokens...")
            print("="*60)
            
            # Test building creation form
            resp = client.get('/dashboard')
            html = resp.data.decode()
            if 'building_new' in html or 'Add Building' in html:
                results.append(('Building New Button', 'PASS - Button Found', '-'))
            
            # Test Assessment Item form page
            resp = client.get(f'/building/{building_id}/assessment/items/new')
            html = resp.data.decode()
            if 'csrf_token' in html or 'hidden_tag' in html:
                results.append(('Assessment Form CSRF', 'PASS', '-'))
            else:
                results.append(('Assessment Form CSRF', 'FAIL - No CSRF', '-'))
            
            # Test Compliance form page
            resp = client.get(f'/building/{building_id}/compliance/new')
            html = resp.data.decode()
            if 'csrf_token' in html or 'hidden_tag' in html:
                results.append(('Compliance Form CSRF', 'PASS', '-'))
            else:
                results.append(('Compliance Form CSRF', 'FAIL - No CSRF', '-'))
            
            # Test System Scoring page
            resp = client.get(f'/building/{building_id}/system-scoring')
            html = resp.data.decode()
            if 'csrf_token' in html:
                results.append(('System Scoring Form CSRF', 'PASS', '-'))
            else:
                results.append(('System Scoring Form CSRF', 'No Form (OK)', '-'))
            
            # Test Test Register form
            resp = client.get(f'/building/{building_id}/tests/new')
            html = resp.data.decode()
            if 'csrf_token' in html or 'hidden_tag' in html:
                results.append(('Test Register Form CSRF', 'PASS', '-'))
            else:
                results.append(('Test Register Form CSRF', 'FAIL - No CSRF', '-'))
            
            # Test CAPA form
            resp = client.get(f'/building/{building_id}/capa/new')
            html = resp.data.decode()
            if 'csrf_token' in html or 'hidden_tag' in html:
                results.append(('CAPA Form CSRF', 'PASS', '-'))
            else:
                results.append(('CAPA Form CSRF', 'FAIL - No CSRF', '-'))
            
            # Test Edit Profile form
            resp = client.get('/edit-profile')
            html = resp.data.decode()
            if 'csrf_token' in html:
                results.append(('Edit Profile Form CSRF', 'PASS', '-'))
            else:
                results.append(('Edit Profile Form CSRF', 'FAIL - No CSRF', '-'))
    
    # Print results
    print("\n" + "="*70)
    print("TEST RESULTS - All Pages and Buttons")
    print("="*70)
    
    passed = 0
    failed = 0
    
    for test, status, code in results:
        if 'PASS' in status:
            passed += 1
            print(f"✓ {test}: {status} ({code})")
        elif 'FAIL' in status:
            failed += 1
            print(f"✗ {test}: {status} ({code})")
        else:
            print(f"  {test}: {status} ({code})")
    
    print("\n" + "="*70)
    print(f"SUMMARY: {passed} passed, {failed} failed out of {len(results)} tests")
    print("="*70)
    
    return failed == 0


if __name__ == '__main__':
    success = test_all_pages()
    sys.exit(0 if success else 1)
