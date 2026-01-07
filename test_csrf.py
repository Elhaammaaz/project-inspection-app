"""
Comprehensive CSRF and form test - tests all forms are working
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from models import User, Building, System, Assessment
from werkzeug.security import generate_password_hash
import re

def extract_csrf(html):
    """Extract CSRF token from HTML form"""
    match = re.search(r'name="csrf_token".*?value="([^"]+)"', html, re.DOTALL)
    if match:
        return match.group(1)
    # Try hidden_tag format
    match = re.search(r'type="hidden".*?name="csrf_token".*?value="([^"]+)"', html, re.DOTALL)
    if match:
        return match.group(1)
    return None

def test_csrf_tokens():
    """Test that all forms have CSRF tokens"""
    app = create_app()
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['TESTING'] = True
    
    results = []
    
    with app.test_client() as client:
        with app.app_context():
            # Get or create admin user
            user = User.query.filter_by(username='admin').first()
            if not user:
                user = User(
                    username='admin',
                    email='admin@test.com',
                    password_hash=generate_password_hash('admin123'),
                    role='Admin'
                )
                db.session.add(user)
                db.session.commit()
            
            # Get or create building
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
                
                # Create assessment for building
                assessment = Assessment(building_id=building.id)
                db.session.add(assessment)
                db.session.commit()
            
            building_id = building.id
            
            # Test login page
            resp = client.get('/login')
            csrf = extract_csrf(resp.data.decode())
            if csrf:
                results.append(('Login Page CSRF', 'PASS', 'Token found'))
            else:
                results.append(('Login Page CSRF', 'FAIL', 'No token'))
            
            # Login
            resp = client.post('/login', data={
                'email': 'admin@test.com',
                'password': 'admin123',
                'csrf_token': csrf
            }, follow_redirects=True)
            
            if resp.status_code == 200:
                results.append(('Login POST', 'PASS', 'Logged in'))
            else:
                results.append(('Login POST', 'FAIL', f'Status {resp.status_code}'))
            
            # Test Register page
            resp = client.get('/register')
            csrf = extract_csrf(resp.data.decode())
            if csrf:
                results.append(('Register Page CSRF', 'PASS', 'Token found'))
            else:
                results.append(('Register Page CSRF', 'FAIL', 'No token'))
            
            # Test Assessment Item New form
            resp = client.get(f'/building/{building_id}/assessment/item/new')
            if resp.status_code == 200:
                csrf = extract_csrf(resp.data.decode())
                if csrf:
                    results.append(('Assessment Item Form CSRF', 'PASS', 'Token found'))
                else:
                    results.append(('Assessment Item Form CSRF', 'FAIL', 'No token'))
            else:
                results.append(('Assessment Item Form', 'FAIL', f'Status {resp.status_code}'))
            
            # Test Compliance Item New form
            resp = client.get(f'/building/{building_id}/compliance/new')
            if resp.status_code == 200:
                csrf = extract_csrf(resp.data.decode())
                if csrf:
                    results.append(('Compliance Item Form CSRF', 'PASS', 'Token found'))
                else:
                    results.append(('Compliance Item Form CSRF', 'FAIL', 'No token'))
            else:
                results.append(('Compliance Item Form', 'FAIL', f'Status {resp.status_code}'))
            
            # Test System Scoring form (has weight inputs)
            resp = client.get(f'/building/{building_id}/system-scoring')
            if resp.status_code == 200:
                csrf = extract_csrf(resp.data.decode())
                if csrf:
                    results.append(('System Scoring Form CSRF', 'PASS', 'Token found'))
                else:
                    # May not have form if no system scores
                    if 'No System Scores' in resp.data.decode():
                        results.append(('System Scoring Form CSRF', 'OK', 'No form (no data)'))
                    else:
                        results.append(('System Scoring Form CSRF', 'FAIL', 'No token'))
            else:
                results.append(('System Scoring Form', 'FAIL', f'Status {resp.status_code}'))
            
            # Test Test Register New form
            resp = client.get(f'/building/{building_id}/tests/new')
            if resp.status_code == 200:
                csrf = extract_csrf(resp.data.decode())
                if csrf:
                    results.append(('Test Register Form CSRF', 'PASS', 'Token found'))
                else:
                    results.append(('Test Register Form CSRF', 'FAIL', 'No token'))
            else:
                results.append(('Test Register Form', 'FAIL', f'Status {resp.status_code}'))
            
            # Test CAPA Register New form
            resp = client.get(f'/building/{building_id}/capa/new')
            if resp.status_code == 200:
                csrf = extract_csrf(resp.data.decode())
                if csrf:
                    results.append(('CAPA Register Form CSRF', 'PASS', 'Token found'))
                else:
                    results.append(('CAPA Register Form CSRF', 'FAIL', 'No token'))
            else:
                results.append(('CAPA Register Form', 'FAIL', f'Status {resp.status_code}'))
            
            # Test Admin Requests
            resp = client.get('/admin/requests')
            if resp.status_code == 200:
                csrf = extract_csrf(resp.data.decode())
                if csrf:
                    results.append(('Admin Requests CSRF', 'PASS', 'Token found'))
                else:
                    # Check if there are even forms on the page
                    if '<form' in resp.data.decode():
                        results.append(('Admin Requests CSRF', 'FAIL', 'Forms found but no CSRF'))
                    else:
                        results.append(('Admin Requests CSRF', 'OK', 'No forms (no data)'))
            else:
                results.append(('Admin Requests', 'FAIL', f'Status {resp.status_code}'))
            
            # Test building creation form (on dashboard)
            resp = client.get('/dashboard')
            if resp.status_code == 200:
                csrf = extract_csrf(resp.data.decode())
                if csrf:
                    results.append(('Building Form CSRF', 'PASS', 'Token found'))
                else:
                    results.append(('Building Form CSRF', 'FAIL', 'No token'))
            else:
                results.append(('Building Form', 'FAIL', f'Status {resp.status_code}'))
            
            # Test an actual form submission with CSRF
            resp = client.get(f'/building/{building_id}/tests/new')
            csrf = extract_csrf(resp.data.decode())
            if csrf:
                # Get first system
                system = System.query.first()
                if system:
                    from datetime import date
                    post_resp = client.post(f'/building/{building_id}/tests/new', data={
                        'csrf_token': csrf,
                        'system': system.id,
                        'test_id': 'TEST-001',
                        'test_name': 'Test Record',
                        'test_date': date.today().isoformat(),
                        'result': 'Pass'
                    }, follow_redirects=True)
                    
                    if post_resp.status_code == 200 and 'CSRF' not in post_resp.data.decode():
                        results.append(('Test Form POST with CSRF', 'PASS', 'Submitted OK'))
                    else:
                        if 'CSRF' in post_resp.data.decode():
                            results.append(('Test Form POST with CSRF', 'FAIL', 'CSRF error'))
                        else:
                            results.append(('Test Form POST with CSRF', 'PARTIAL', 'Form errors but CSRF OK'))
    
    # Print results
    print("\n" + "="*70)
    print("CSRF TOKEN TEST RESULTS")
    print("="*70)
    
    passed = 0
    failed = 0
    ok = 0
    
    for test, status, detail in results:
        if status == 'PASS':
            passed += 1
            print(f"✓ {test}: {status} - {detail}")
        elif status == 'FAIL':
            failed += 1
            print(f"✗ {test}: {status} - {detail}")
        else:
            ok += 1
            print(f"○ {test}: {status} - {detail}")
    
    print("\n" + "="*70)
    print(f"SUMMARY: {passed} passed, {failed} failed, {ok} ok")
    print("="*70)
    
    return failed == 0


if __name__ == '__main__':
    success = test_csrf_tokens()
    sys.exit(0 if success else 1)
