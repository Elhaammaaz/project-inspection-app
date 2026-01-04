#!/usr/bin/env python
"""
Database Migration Script
This script initializes the database with all required tables.
Run this on Railway to ensure tables are created.
"""

import os
import sys
from sqlalchemy import inspect, text

# Setup path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, User, ProjectInspection

def init_database():
    """Initialize database with all tables"""
    
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("🔨 DATABASE INITIALIZATION")
        print("=" * 60)
        
        # Check current database URL
        db_url = app.config.get('SQLALCHEMY_DATABASE_URI', 'unknown')
        print(f"\n📊 Database: {db_url[:60]}...")
        
        # Create all tables
        print("\n📋 Creating tables...")
        try:
            db.create_all()
            print("✅ Tables created successfully!")
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            return False
        
        # List all tables
        try:
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"\n📊 Tables in database ({len(tables)}):")
            for table in tables:
                columns = inspector.get_columns(table)
                print(f"  • {table} ({len(columns)} columns)")
                for col in columns[:3]:  # Show first 3 columns
                    print(f"    - {col['name']}: {col['type']}")
                if len(columns) > 3:
                    print(f"    - ... and {len(columns) - 3} more columns")
            
        except Exception as e:
            print(f"⚠️  Could not list tables: {e}")
        
        # Create demo user
        print("\n👤 Creating demo account...")
        try:
            demo_user = User.query.filter_by(email='demo@example.com').first()
            if not demo_user:
                demo_user = User(email='demo@example.com')
                demo_user.set_password('demo123')
                db.session.add(demo_user)
                db.session.commit()
                print("✅ Demo user created: demo@example.com / demo123")
            else:
                print("ℹ️  Demo user already exists")
        except Exception as e:
            print(f"⚠️  Demo user error: {e}")
            db.session.rollback()
        
        print("\n" + "=" * 60)
        print("✅ DATABASE INITIALIZATION COMPLETE!")
        print("=" * 60)
        
        return True

if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 1)
