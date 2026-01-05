#!/usr/bin/env python3
"""
Setup script - Make demo user an admin with all access permissions
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, User, UserProfile

def setup_demo():
    """Setup demo admin user with all permissions"""
    app = create_app()
    
    with app.app_context():
        print("🔧 Setting up demo admin user...")
        print("-" * 60)
        
        try:
            # Find demo user
            demo_user = User.query.filter_by(email='demo@example.com').first()
            
            if not demo_user:
                print("❌ Demo user not found!")
                sys.exit(1)
            
            # Ensure profile exists with admin role
            if not demo_user.profile:
                profile = UserProfile(
                    user_id=demo_user.id,
                    role='admin',
                    department='Administration',
                    phone='555-0000'
                )
                db.session.add(profile)
            else:
                demo_user.profile.role = 'admin'
            
            # Grant all access permissions
            demo_user.can_view_dashboard = 1
            demo_user.can_view_reports = 1
            demo_user.can_export_data = 1
            demo_user.can_manage_users = 1
            
            # Set active and approved
            demo_user.active = 1
            
            db.session.commit()
            
            print("✓ Demo user configured as admin:")
            print(f"  Email: {demo_user.email}")
            print(f"  Full Name: {demo_user.full_name}")
            print(f"  Dashboard Access: ✓")
            print(f"  Reports Access: ✓")
            print(f"  Export Access: ✓")
            print(f"  User Management: ✓")
            print("\n✓ Setup completed successfully!")
            print("-" * 60)
            print("\n🚀 You can now login with:")
            print("   Email: demo@example.com")
            print("   Password: demo123")
            
        except Exception as e:
            print(f"❌ Setup error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == '__main__':
    setup_demo()
