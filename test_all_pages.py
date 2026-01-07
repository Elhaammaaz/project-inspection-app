#!/usr/bin/env python
"""
Comprehensive test of all pages and buttons in the BCAR application
"""
import requests
from bs4 import BeautifulSoup
import time
import sys

BASE_URL = "http://127.0.0.1:5000"
session = requests.Session()

# Demo credentials
DEMO_USER = "demo"
DEMO_PASS = "demo123"

print("=" * 80)
print("COMPREHENSIVE PAGE AND BUTTON TESTING")
print("=" * 80)

# Step 1: Test public pages (no login required)
print("\n[STEP 1] Testing Public Pages (No Login Required)")
print("-" * 80)

pages_to_test = [
    ("/", "Home Page"),
    ("/login", "Login Page"),
    ("/register", "Register Page"),
]

for url, name in pages_to_test:
    try:
        resp = session.get(f"{BASE_URL}{url}", timeout=5)
        status = "✅ OK" if resp.status_code == 200 else f"❌ Error {resp.status_code}"
        print(f"{status} - {name}: {url}")
    except Exception as e:
        print(f"❌ FAILED - {name}: {str(e)}")

# Step 2: Login with demo account
print("\n[STEP 2] Logging In with Demo Account")
print("-" * 80)

try:
    # Get CSRF token from login page
    login_page = session.get(f"{BASE_URL}/login")
    soup = BeautifulSoup(login_page.content, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})
    
    if csrf_token:
        csrf_value = csrf_token.get('value')
        
        # Login
        login_data = {
            'username': DEMO_USER,
            'password': DEMO_PASS,
            'csrf_token': csrf_value
        }
        resp = session.post(f"{BASE_URL}/login", data=login_data, allow_redirects=True)
        
        if resp.status_code == 200:
            print(f"✅ Login successful for user: {DEMO_USER}")
        else:
            print(f"❌ Login failed with status {resp.status_code}")
    else:
        print("❌ Could not find CSRF token")
except Exception as e:
    print(f"❌ Login error: {str(e)}")

# Step 3: Test protected/authenticated pages
print("\n[STEP 3] Testing Protected Pages (After Login)")
print("-" * 80)

protected_pages = [
    ("/dashboard", "Dashboard"),
    ("/profile", "Profile Page"),
    ("/admin", "Admin Dashboard"),
]

for url, name in protected_pages:
    try:
        resp = session.get(f"{BASE_URL}{url}", timeout=5)
        if resp.status_code == 200:
            print(f"✅ OK - {name}: {url}")
        elif resp.status_code == 403:
            print(f"⚠️ FORBIDDEN (Access denied) - {name}: {url}")
        elif resp.status_code == 302:
            print(f"⚠️ REDIRECT - {name}: {url} (might redirect to login)")
        else:
            print(f"❌ Error {resp.status_code} - {name}: {url}")
    except Exception as e:
        print(f"❌ FAILED - {name}: {str(e)}")

# Step 4: Extract and test all buttons/links from Dashboard
print("\n[STEP 4] Testing All Buttons/Links on Dashboard")
print("-" * 80)

try:
    dashboard_resp = session.get(f"{BASE_URL}/dashboard", timeout=5)
    dashboard_soup = BeautifulSoup(dashboard_resp.content, 'html.parser')
    
    # Find all links
    links = dashboard_soup.find_all('a')
    if links:
        print(f"Found {len(links)} links on dashboard:")
        for i, link in enumerate(links[:20], 1):  # Test first 20 links
            href = link.get('href')
            text = link.get_text(strip=True)[:50]  # Truncate text
            
            if href and (href.startswith('/') or href.startswith('http')):
                try:
                    test_resp = session.get(f"{BASE_URL}{href}" if href.startswith('/') else href, timeout=5)
                    status = "✅" if test_resp.status_code in [200, 302] else f"❌ ({test_resp.status_code})"
                    print(f"  {i:2d}. {status} {text[:40]:40s} → {href}")
                except Exception as e:
                    print(f"  {i:2d}. ❌ {text[:40]:40s} → {href} (Error: {str(e)[:30]})")
    else:
        print("No links found on dashboard")
except Exception as e:
    print(f"❌ Could not test dashboard links: {str(e)}")

# Step 5: Test navigation buttons in base template
print("\n[STEP 5] Testing Navigation Menu Buttons")
print("-" * 80)

try:
    resp = session.get(f"{BASE_URL}/dashboard", timeout=5)
    soup = BeautifulSoup(resp.content, 'html.parser')
    
    # Find navbar
    nav = soup.find('nav')
    if nav:
        nav_links = nav.find_all('a')
        print(f"Found {len(nav_links)} navigation menu items:")
        for i, link in enumerate(nav_links[:15], 1):
            href = link.get('href')
            text = link.get_text(strip=True)
            
            if href and (href.startswith('/') or href.startswith('#')):
                if not href.startswith('#'):
                    try:
                        test_resp = session.get(f"{BASE_URL}{href}", timeout=5)
                        status = "✅" if test_resp.status_code in [200, 302] else f"❌ ({test_resp.status_code})"
                        print(f"  {i:2d}. {status} {text[:35]:35s} → {href}")
                    except:
                        print(f"  {i:2d}. ❌ {text[:35]:35s} → {href}")
    else:
        print("No navigation menu found")
except Exception as e:
    print(f"Error testing navigation: {str(e)}")

# Step 6: Test form pages
print("\n[STEP 6] Testing Form Pages")
print("-" * 80)

form_pages = [
    ("/building/new", "New Building Form"),
    ("/profile", "Profile/Edit Profile"),
]

for url, name in form_pages:
    try:
        resp = session.get(f"{BASE_URL}{url}", timeout=5)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            forms = soup.find_all('form')
            button_count = len(soup.find_all(['button', 'input[type="submit"]']))
            print(f"✅ {name}: {url} (Found {len(forms)} form(s), {button_count} button(s))")
        else:
            print(f"❌ {name}: {url} (Status: {resp.status_code})")
    except Exception as e:
        print(f"❌ {name}: {str(e)}")

# Step 7: Test logout
print("\n[STEP 7] Testing Logout")
print("-" * 80)

try:
    logout_resp = session.get(f"{BASE_URL}/logout", allow_redirects=True, timeout=5)
    if logout_resp.status_code == 200:
        print(f"✅ Logout successful - redirected back to login/home")
    else:
        print(f"⚠️ Logout returned status {logout_resp.status_code}")
except Exception as e:
    print(f"❌ Logout failed: {str(e)}")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
