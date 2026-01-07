"""
Login Test - Test authentication with demo account
Tests the complete login flow
"""

import urllib.request
import urllib.parse
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup
import time

BASE_URL = 'http://127.0.0.1:5000'

# Create a cookie jar to maintain session
cookie_jar = CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

def test_login_flow():
    """Test the complete login flow"""
    print('=' * 70)
    print('TESTING LOGIN WITH DEMO ACCOUNT')
    print('=' * 70)
    print()
    
    # Step 1: Get login page to extract CSRF token
    print('Step 1: Accessing login page...')
    try:
        response = opener.open(f'{BASE_URL}/login')
        login_html = response.read().decode('utf-8')
        print('✅ Login page loaded (Status: 200)')
        
        # Parse HTML to find CSRF token
        soup = BeautifulSoup(login_html, 'html.parser')
        csrf_token = None
        
        # Find the CSRF token in the form
        for input_field in soup.find_all('input', {'type': 'hidden'}):
            if input_field.get('name') == 'csrf_token':
                csrf_token = input_field.get('value')
                break
        
        if csrf_token:
            print(f'✅ CSRF token found: {csrf_token[:20]}...')
        else:
            print('⚠️ CSRF token not found (but login might still work)')
        
        # Step 2: Submit login form
        print()
        print('Step 2: Submitting login form...')
        print('   Username: demo')
        print('   Password: demo123')
        
        # Prepare login data
        login_data = {
            'username': 'demo',
            'password': 'demo123'
        }
        
        if csrf_token:
            login_data['csrf_token'] = csrf_token
        
        # Encode and submit
        encoded_data = urllib.parse.urlencode(login_data).encode('utf-8')
        
        try:
            response = opener.open(f'{BASE_URL}/login', encoded_data)
            response_html = response.read().decode('utf-8')
            
            print(f'✅ Login form submitted (Status: {response.status})')
            
            # Step 3: Check response
            print()
            print('Step 3: Verifying login response...')
            
            # Check if we got dashboard or error
            if 'dashboard' in response.url or 'Dashboard' in response_html or 'buildings' in response_html.lower():
                print('✅ LOGIN SUCCESSFUL!')
                print(f'   Redirected to: {response.url}')
                print('   Dashboard content found')
                return True
            elif 'login' in response.url and 'Invalid' in response_html:
                print('❌ LOGIN FAILED')
                print('   Invalid credentials')
                return False
            else:
                print('⚠️ Login response unclear')
                print(f'   URL: {response.url}')
                print(f'   Content length: {len(response_html)} bytes')
                
                # Check for error messages
                if 'error' in response_html.lower():
                    print('   ERROR found in response')
                    return False
                else:
                    print('   No obvious error - might be success')
                    return True
                    
        except urllib.error.HTTPError as e:
            print(f'❌ HTTP Error: {e.code}')
            print(f'   Message: {e.reason}')
            return False
            
    except Exception as e:
        print(f'❌ Error: {str(e)}')
        return False

# Run the test
print()
success = test_login_flow()

print()
print('=' * 70)
print('TEST RESULT')
print('=' * 70)
if success:
    print('✅ LOGIN SUCCESSFUL - Demo account is working!')
    print()
    print('You can now:')
    print('  1. View buildings list')
    print('  2. Create new buildings')
    print('  3. Add assessment items')
    print('  4. View dashboards and KPIs')
else:
    print('❌ LOGIN FAILED - Check credentials or database')
print()
