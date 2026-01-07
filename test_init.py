#!/usr/bin/env python
"""Quick test of app initialization"""
import sys
sys.path.insert(0, '.')

try:
    from app import create_app
    print("✓ Importing create_app...")
    app = create_app()
    print("✓ App created successfully")
    
    with app.app_context():
        from models import db
        print("✓ Database context works")
        print("✓ All systems ready!")
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
