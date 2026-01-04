#!/usr/bin/env python
"""
Force Initialize Database with Inspection Table + Sample Data
This script GUARANTEES the inspection table is created and populated
"""

import os
import sys
from datetime import datetime, date
from sqlalchemy import inspect, text

# Setup path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, User, ProjectInspection

def force_init_database():
    """Force initialize database with tables and sample data"""
    
    app = create_app()
    
    with app.app_context():
        print("\n" + "=" * 80)
        print("🔨 FORCE DATABASE INITIALIZATION")
        print("=" * 80)
        
        # Get database URL
        db_url = app.config.get('SQLALCHEMY_DATABASE_URI', 'unknown')
        print(f"\n📊 Database: {db_url[:60]}...")
        
        # Step 1: Drop existing tables (clean slate)
        print("\n[1/5] 🗑️  Checking for existing tables...")
        try:
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            print(f"     Found tables: {existing_tables}")
        except Exception as e:
            print(f"     ⚠️  Could not inspect: {e}")
            existing_tables = []
        
        # Step 2: Create all tables
        print("\n[2/5] 🔨 Creating database tables...")
        try:
            db.create_all()
            print("     ✅ Tables created successfully!")
        except Exception as e:
            print(f"     ❌ Error creating tables: {e}")
            return False
        
        # Step 3: Verify tables exist
        print("\n[3/5] 📋 Verifying tables...")
        try:
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            required_tables = ['users', 'project_inspections']
            for table in required_tables:
                if table in tables:
                    columns = inspector.get_columns(table)
                    print(f"     ✅ {table} ({len(columns)} columns)")
                else:
                    print(f"     ❌ {table} NOT FOUND!")
                    return False
        except Exception as e:
            print(f"     ❌ Error verifying: {e}")
            return False
        
        # Step 4: Create/verify demo user
        print("\n[4/5] 👤 Creating demo user...")
        try:
            demo_user = User.query.filter_by(email='demo@example.com').first()
            if not demo_user:
                demo_user = User(email='demo@example.com')
                demo_user.set_password('demo123')
                db.session.add(demo_user)
                db.session.commit()
                print("     ✅ Demo user created: demo@example.com / demo123")
            else:
                print("     ℹ️  Demo user already exists")
        except Exception as e:
            print(f"     ❌ Error with demo user: {e}")
            db.session.rollback()
            return False
        
        # Step 5: Add 3 sample inspections
        print("\n[5/5] 📝 Adding 3 sample inspections...")
        
        # First, delete any existing inspections to start fresh
        try:
            ProjectInspection.query.delete()
            db.session.commit()
            print("     🗑️  Cleared existing inspections")
        except:
            db.session.rollback()
        
        # Sample data - exactly 3 rows
        samples = [
            {
                'project_name': 'Downtown Office Tower',
                'city': 'Riyadh',
                'address': 'King Fahd Road, Riyadh',
                'gps_latitude': 24.7136,
                'gps_longitude': 46.6753,
                'building_type': 'Commercial',
                'primary_use': 'Office',
                'gross_built_area': 45000.0,
                'number_of_floors': 20,
                'construction_year': 2010,
                'current_year': 2025,
                'estimated_life_time': 50,
                'planned_retirement_year': 2060,
                'last_renovation_date': date(2020, 6, 15),
                'inspection_date': date(2025, 12, 15),
                'fm_contractor': 'FM Solutions Saudi',
                'system_threshold': 85.0,
                'inspection_result': 'Passed',
                'building_score': 85.5,
                'fm_performance': 92.0,
                'government_compliance': 'Complied',
                'high_priority_classified': 0,
                'fire_life_safety': 88.0,
                'total_economic_life': 50,
                'chronological_age': 15,
                'estimated_effective_age': 12,
                'estimated_remaining_life': 38,
                'notes': 'Well-maintained building. All systems operational.',
            },
            {
                'project_name': 'Business Park Complex',
                'city': 'Jeddah',
                'address': 'Red Sea Street, Jeddah',
                'gps_latitude': 21.5433,
                'gps_longitude': 39.1728,
                'building_type': 'Mixed Use',
                'primary_use': 'Retail & Office',
                'gross_built_area': 62000.0,
                'number_of_floors': 15,
                'construction_year': 2015,
                'current_year': 2025,
                'estimated_life_time': 50,
                'planned_retirement_year': 2065,
                'last_renovation_date': date(2022, 3, 20),
                'inspection_date': date(2025, 12, 10),
                'fm_contractor': 'Global Property Management',
                'system_threshold': 80.0,
                'inspection_result': 'Passed but Need Attention',
                'building_score': 78.0,
                'fm_performance': 85.0,
                'government_compliance': 'Partial Compliance',
                'high_priority_classified': 2,
                'fire_life_safety': 82.0,
                'total_economic_life': 50,
                'chronological_age': 10,
                'estimated_effective_age': 8,
                'estimated_remaining_life': 42,
                'notes': 'Requires attention to HVAC systems and emergency exits.',
            },
            {
                'project_name': 'Industrial Warehouse',
                'city': 'Dammam',
                'address': 'Industrial Zone 5, Dammam',
                'gps_latitude': 26.4167,
                'gps_longitude': 50.2,
                'building_type': 'Industrial',
                'primary_use': 'Warehouse',
                'gross_built_area': 120000.0,
                'number_of_floors': 3,
                'construction_year': 2008,
                'current_year': 2025,
                'estimated_life_time': 50,
                'planned_retirement_year': 2058,
                'last_renovation_date': date(2018, 9, 10),
                'inspection_date': date(2025, 12, 20),
                'fm_contractor': 'Industrial Services Ltd',
                'system_threshold': 75.0,
                'inspection_result': 'Passed but Need Attention',
                'building_score': 72.0,
                'fm_performance': 78.0,
                'government_compliance': 'Not Complied',
                'high_priority_classified': 5,
                'fire_life_safety': 75.0,
                'total_economic_life': 50,
                'chronological_age': 17,
                'estimated_effective_age': 19,
                'estimated_remaining_life': 31,
                'notes': 'Aging infrastructure. Requires immediate attention to electrical systems.',
            },
        ]
        
        # Add all 3 samples
        added_count = 0
        for idx, data in enumerate(samples, 1):
            try:
                inspection = ProjectInspection(user_id=demo_user.id, **data)
                db.session.add(inspection)
                print(f"     ✅ Row {idx}: {data['project_name']} ({data['city']})")
                added_count += 1
            except Exception as e:
                print(f"     ❌ Row {idx} Error: {e}")
                db.session.rollback()
                return False
        
        # Commit all
        try:
            db.session.commit()
            print(f"\n     ✅ Successfully added all {added_count} inspections!")
        except Exception as e:
            print(f"     ❌ Commit error: {e}")
            db.session.rollback()
            return False
        
        # Step 6: Verify final data
        print("\n" + "-" * 80)
        print("📊 FINAL VERIFICATION")
        print("-" * 80)
        
        try:
            user_count = User.query.count()
            inspection_count = ProjectInspection.query.count()
            
            print(f"\n✅ Users in database: {user_count}")
            print(f"✅ Inspections in database: {inspection_count}")
            
            # List all inspections
            inspections = ProjectInspection.query.all()
            print(f"\n📋 All Inspections:")
            for insp in inspections:
                print(f"   ID: {insp.id} | {insp.project_name} | {insp.city} | Score: {insp.building_score}")
            
        except Exception as e:
            print(f"❌ Error verifying: {e}")
            return False
        
        print("\n" + "=" * 80)
        print("✅ DATABASE INITIALIZATION COMPLETE!")
        print("=" * 80)
        print("\n🔗 Next Steps:")
        print("   1. Visit: https://web-production-c26d2.up.railway.app")
        print("   2. Login: demo@example.com / demo123")
        print("   3. Check: /api/inspections endpoint")
        print("   4. Update Power BI query")
        print("\n")
        
        return True

if __name__ == '__main__':
    try:
        success = force_init_database()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
