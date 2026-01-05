#!/usr/bin/env python3
"""
Database migration script - Add access control columns to User model
"""

import os
import sys
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, User

def migrate_database():
    """Migrate database to add new access control columns"""
    app = create_app()
    
    with app.app_context():
        print("🔄 Starting database migration...")
        print("-" * 60)
        
        try:
            # Create all tables (including new columns)
            db.create_all()
            print("✓ Database schema updated successfully")
            
            # Get all users
            users = User.query.all()
            print(f"✓ Found {len(users)} existing users")
            
            # Check and update columns for existing users
            updated_count = 0
            for user in users:
                # Ensure all new columns have default values
                if user.can_view_dashboard is None:
                    user.can_view_dashboard = 0
                    updated_count += 1
                if user.can_view_reports is None:
                    user.can_view_reports = 0
                    updated_count += 1
                if user.can_export_data is None:
                    user.can_export_data = 0
                    updated_count += 1
                if user.can_manage_users is None:
                    user.can_manage_users = 0
                    updated_count += 1
            
            if updated_count > 0:
                db.session.commit()
                print(f"✓ Updated {updated_count} user records with default access values")
            
            # Print database statistics
            print("\n📊 Database Statistics:")
            print(f"   Total users: {len(users)}")
            
            dashboard_users = User.query.filter(User.can_view_dashboard == 1).count()
            reports_users = User.query.filter(User.can_view_reports == 1).count()
            export_users = User.query.filter(User.can_export_data == 1).count()
            manage_users = User.query.filter(User.can_manage_users == 1).count()
            
            print(f"   Dashboard access: {dashboard_users}")
            print(f"   Reports access: {reports_users}")
            print(f"   Export access: {export_users}")
            print(f"   User management: {manage_users}")
            
            print("\n✓ Migration completed successfully!")
            print("-" * 60)
            
        except Exception as e:
            print(f"❌ Migration error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == '__main__':
    migrate_database()
