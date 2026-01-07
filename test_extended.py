#!/usr/bin/env python
"""
Extended test for all pages, buttons, and forms in the BCAR application
This tests the building workflow including creation and all steps
"""
import requests
from bs4 import BeautifulSoup
import sys

BASE_URL = "http://127.0.0.1:5000"
session = requests.Session()

DEMO_USER = "demo"
DEMO_PASS = "demo123"

def login():
    """Login with demo account and return CSRF token"""
    login_page = session.get(f"{BASE_URL}/login")
    soup = BeautifulSoup(login_page.content, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})
    
    if csrf_token:
        login_data = {
            'username': DEMO_USER,
            'password': DEMO_PASS,
            'csrf_token': csrf_token.get('value')
        }
        resp = session.post(f"{BASE_URL}/login", data=login_data, allow_redirects=True)
        return resp.status_code == 200
    return False

def get_csrf_token(url):
    """Get CSRF token from a page"""
    resp = session.get(f"{BASE_URL}{url}")
    soup = BeautifulSoup(resp.content, 'html.parser')
    csrf_input = soup.find('input', {'name': 'csrf_token'})
    return csrf_input.get('value') if csrf_input else None

def test_all_links_on_page(url, page_name):
    """Test all links on a given page"""
    print(f"\n--- Testing links on {page_name} ({url}) ---")
    try:
        resp = session.get(f"{BASE_URL}{url}", timeout=5)
        if resp.status_code != 200:
            print(f"❌ Could not access {page_name}: Status {resp.status_code}")
            return []
            
        soup = BeautifulSoup(resp.content, 'html.parser')
        links = soup.find_all('a')
        results = []
        
        for link in links:
            href = link.get('href')
            text = link.get_text(strip=True)[:40]
            
            if href and href.startswith('/') and not href.startswith('/logout'):
                try:
                    test_resp = session.get(f"{BASE_URL}{href}", timeout=5)
                    status = "✅" if test_resp.status_code in [200, 302] else f"❌ ({test_resp.status_code})"
                    results.append((href, status))
                    print(f"  {status} {text:40s} → {href}")
                except Exception as e:
                    print(f"  ❌ {text:40s} → {href} (Error: {str(e)[:30]})")
                    results.append((href, "❌"))
            elif href and href.startswith('#'):
                # Skip anchor links
                pass
        
        return results
    except Exception as e:
        print(f"❌ Error testing {page_name}: {str(e)}")
        return []

def test_form_submission(url, form_data, expected_redirect=None):
    """Test form submission"""
    print(f"\n--- Testing form submission on {url} ---")
    try:
        # Get CSRF token
        csrf = get_csrf_token(url)
        if csrf:
            form_data['csrf_token'] = csrf
        
        resp = session.post(f"{BASE_URL}{url}", data=form_data, allow_redirects=True)
        if resp.status_code == 200:
            print(f"✅ Form submitted successfully")
            return True
        else:
            print(f"❌ Form submission failed: Status {resp.status_code}")
            return False
    except Exception as e:
        print(f"❌ Form submission error: {str(e)}")
        return False


print("=" * 80)
print("EXTENDED COMPREHENSIVE TESTING - ALL PAGES, BUTTONS, AND FORMS")
print("=" * 80)

# Step 1: Login
print("\n[1] LOGIN")
if login():
    print("✅ Login successful")
else:
    print("❌ Login failed")
    sys.exit(1)

# Step 2: Test Dashboard
print("\n[2] DASHBOARD")
test_all_links_on_page('/dashboard', 'Dashboard')

# Step 3: Test Profile pages
print("\n[3] PROFILE PAGES")
test_all_links_on_page('/profile', 'Profile')
test_all_links_on_page('/profile/edit', 'Edit Profile')

# Step 4: Test Admin pages
print("\n[4] ADMIN PAGES")
test_all_links_on_page('/admin', 'Admin Dashboard')
test_all_links_on_page('/admin/requests', 'Admin Requests')

# Step 5: Test Building Creation Form
print("\n[5] BUILDING CREATION FORM")
resp = session.get(f"{BASE_URL}/building/new")
if resp.status_code == 200:
    print("✅ Building creation form loads")
    soup = BeautifulSoup(resp.content, 'html.parser')
    form = soup.find('form')
    if form:
        inputs = form.find_all(['input', 'select', 'textarea'])
        print(f"   Found {len(inputs)} form fields")
        buttons = form.find_all('button') + form.find_all('input', {'type': 'submit'})
        print(f"   Found {len(buttons)} buttons")
else:
    print(f"❌ Building creation form failed: {resp.status_code}")

# Step 6: Create a test building
print("\n[6] CREATE TEST BUILDING")
from datetime import date
building_data = {
    'project_name': 'Test Building ' + str(date.today()),
    'city': 'Riyadh',
    'address': '123 Test Street',
    'building_type': 'Commercial',
    'primary_use': 'Office',
    'gross_built_area_m2': '5000',
    'number_of_floors': '5',
    'construction_year': '2020',
    'estimated_life_time_years': '50',
    'inspection_date': str(date.today()),
    'current_year': '2026',
    'system_threshold_percent': '75',
}

csrf = get_csrf_token('/building/new')
if csrf:
    building_data['csrf_token'] = csrf
    resp = session.post(f"{BASE_URL}/building/new", data=building_data, allow_redirects=True)
    
    if resp.status_code == 200:
        # Check if we're redirected to building view
        if '/building/' in resp.url:
            print(f"✅ Building created successfully! Redirected to: {resp.url}")
            
            # Test the building view page
            building_view_soup = BeautifulSoup(resp.content, 'html.parser')
            links = building_view_soup.find_all('a')
            print(f"   Found {len(links)} links on building view page")
            
            # Extract building ID for further testing
            building_id = resp.url.split('/')[-1] if '/building/' in resp.url else None
            
            if building_id and building_id.isdigit():
                # Test workflow links
                print(f"\n[7] TESTING BUILDING WORKFLOW (Building ID: {building_id})")
                
                workflow_pages = [
                    (f'/building/{building_id}', 'Building View'),
                    (f'/building/{building_id}/assessment/items', 'Assessment Items'),
                    (f'/building/{building_id}/dashboard', 'Executive Dashboard'),
                ]
                
                for url, name in workflow_pages:
                    try:
                        test_resp = session.get(f"{BASE_URL}{url}", timeout=5)
                        status = "✅" if test_resp.status_code == 200 else f"❌ ({test_resp.status_code})"
                        print(f"  {status} {name}: {url}")
                    except Exception as e:
                        print(f"  ❌ {name}: {url} (Error)")
        else:
            print(f"⚠️ Building creation may have issues - current URL: {resp.url}")
    else:
        print(f"❌ Building creation failed: Status {resp.status_code}")
else:
    print("❌ Could not get CSRF token for building creation")

# Step 8: Test navigation menu
print("\n[8] NAVIGATION MENU LINKS")
resp = session.get(f"{BASE_URL}/dashboard")
soup = BeautifulSoup(resp.content, 'html.parser')
nav = soup.find('nav')
if nav:
    nav_links = nav.find_all('a')
    print(f"Found {len(nav_links)} navigation links")
    for link in nav_links:
        href = link.get('href')
        text = link.get_text(strip=True)[:30]
        if href and href.startswith('/') and not href.startswith('/logout'):
            try:
                test_resp = session.get(f"{BASE_URL}{href}", timeout=5)
                status = "✅" if test_resp.status_code in [200, 302] else f"❌ ({test_resp.status_code})"
                print(f"  {status} {text:30s} → {href}")
            except:
                print(f"  ❌ {text:30s} → {href} (Error)")

print("\n" + "=" * 80)
print("EXTENDED TESTING COMPLETE")
print("=" * 80)
