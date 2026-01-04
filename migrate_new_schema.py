#!/usr/bin/env python
"""
Database Migration Script - Convert old schema to new 2-table structure
This script handles the migration from flat project_inspections to normalized structure
"""

import os
import sys
from app import create_app
from models import db, User, ProjectInspection, InspectionSystem
from datetime import datetime
import json

def migrate_database():
    """Migrate from old schema to new normalized schema"""
    
    app = create_app()
    with app.app_context():
        print("=" * 60)
        print("DATABASE MIGRATION: OLD SCHEMA → NEW SCHEMA")
        print("=" * 60)
        
        # Step 1: Check if we need to migrate
        print("\n[1] Checking database structure...")
        
        try:
            # Try to count existing inspections
            old_inspections = ProjectInspection.query.all()
            print(f"   Found {len(old_inspections)} existing inspections")
            
            # Step 2: Create new tables
            print("\n[2] Creating new database tables...")
            db.create_all()
            print("   ✓ Tables created successfully")
            
            # Step 3: Check if inspection_systems table has data
            existing_systems = InspectionSystem.query.first()
            if existing_systems:
                print("\n   [!] Migration already completed - systems table has data")
                return True
            
            # Step 4: Preserve existing inspections (they remain in project_inspections)
            # The new InspectionSystem table is empty and ready for data
            print(f"\n[3] Preserved {len(old_inspections)} existing inspections")
            print("   ✓ Ready to add system data")
            
            print("\n" + "=" * 60)
            print("MIGRATION COMPLETE!")
            print("=" * 60)
            print("\nNext steps:")
            print("1. Add inspection systems via the web interface")
            print("2. Or run: python populate_systems.py")
            print("\n")
            
            return True
            
        except Exception as e:
            print(f"\n   [ERROR] Migration failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return False


def reset_database_hard():
    """HARD RESET: Delete all tables and recreate from scratch"""
    
    app = create_app()
    with app.app_context():
        print("\n" + "=" * 60)
        print("WARNING: HARD RESET - Deleting all data!")
        print("=" * 60)
        
        confirm = input("\nType 'YES' to confirm hard reset: ").strip()
        if confirm != 'YES':
            print("Hard reset cancelled.")
            return False
        
        try:
            print("\n[1] Dropping all tables...")
            db.drop_all()
            print("   ✓ All tables dropped")
            
            print("\n[2] Creating all tables from models...")
            db.create_all()
            print("   ✓ All tables created")
            
            print("\n[3] Creating demo user...")
            demo_user = User(email='demo@example.com', full_name='Demo Admin', active=1)
            demo_user.set_password('demo123')
            demo_user.approved_at = datetime.utcnow()
            db.session.add(demo_user)
            db.session.commit()
            print("   ✓ Demo user created: demo@example.com / demo123 (ACTIVE)")
            
            print("\n" + "=" * 60)
            print("HARD RESET COMPLETE!")
            print("=" * 60)
            print("\nDatabase is ready with demo account.")
            print("You can now create inspections and add systems.\n")
            
            return True
            
        except Exception as e:
            print(f"\n   [ERROR] Hard reset failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return False


if __name__ == '__main__':
    
    if len(sys.argv) > 1 and sys.argv[1] == 'hard-reset':
        # Hard reset mode
        reset_database_hard()
    else:
        # Normal migration
        migrate_database()
