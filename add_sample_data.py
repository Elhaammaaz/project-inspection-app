"""
Add Sample Inspection Data
Run this to populate the database with sample inspection data for Power BI
"""

import os
import sys
from datetime import datetime, date

# Setup path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, ProjectInspection, User

def add_sample_data():
    """Add sample inspection data"""
    
    app = create_app()
    
    with app.app_context():
        print("=" * 70)
        print("📊 ADDING SAMPLE INSPECTION DATA")
        print("=" * 70)
        
        # Get demo user
        demo_user = User.query.filter_by(email='demo@example.com').first()
        
        if not demo_user:
            print("❌ Demo user not found! Creating demo user first...")
            demo_user = User(email='demo@example.com')
            demo_user.set_password('demo123')
            db.session.add(demo_user)
            db.session.commit()
            print("✅ Demo user created: demo@example.com / demo123")
        
        # Check if data already exists
        existing_count = ProjectInspection.query.count()
        if existing_count > 0:
            print(f"\n⚠️  Database already has {existing_count} inspections")
            print("   Adding more sample data...")
        
        # Sample inspection data
        samples = [
            {
                'project_name': 'Downtown Tower A',
                'city': 'Riyadh',
                'address': 'King Fahd Road, Riyadh 12345',
                'gps_latitude': 24.7136,
                'gps_longitude': 46.6753,
                'building_type': 'Commercial',
                'primary_use': 'Office',
                'gross_built_area': 45000,
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
                'notes': 'Well-maintained building with excellent FM practices',
            },
            {
                'project_name': 'Business Park Complex',
                'city': 'Jeddah',
                'address': 'Red Sea Street, Jeddah 23456',
                'gps_latitude': 21.5433,
                'gps_longitude': 39.1728,
                'building_type': 'Mixed Use',
                'primary_use': 'Retail & Office',
                'gross_built_area': 62000,
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
                'notes': 'Needs attention to HVAC systems and emergency exits',
            },
            {
                'project_name': 'Industrial Hub Warehouse',
                'city': 'Dammam',
                'address': 'Industrial Zone 5, Dammam 34567',
                'gps_latitude': 26.4167,
                'gps_longitude': 50.2,
                'building_type': 'Industrial',
                'primary_use': 'Warehouse',
                'gross_built_area': 120000,
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
                'notes': 'Aging infrastructure. Requires immediate attention to electrical systems and fire safety compliance',
            },
            {
                'project_name': 'Royal Hotel Resort',
                'city': 'Riyadh',
                'address': 'Diplomatic Quarter, Riyadh 11567',
                'gps_latitude': 24.7204,
                'gps_longitude': 46.7048,
                'building_type': 'Hospitality',
                'primary_use': 'Hotel',
                'gross_built_area': 85000,
                'number_of_floors': 25,
                'construction_year': 2012,
                'current_year': 2025,
                'estimated_life_time': 50,
                'planned_retirement_year': 2062,
                'last_renovation_date': date(2021, 5, 12),
                'inspection_date': date(2025, 11, 25),
                'fm_contractor': 'Luxury FM Solutions',
                'system_threshold': 90.0,
                'inspection_result': 'Passed',
                'building_score': 88.0,
                'fm_performance': 94.5,
                'government_compliance': 'Complied',
                'high_priority_classified': 0,
                'fire_life_safety': 91.0,
                'total_economic_life': 50,
                'chronological_age': 13,
                'estimated_effective_age': 10,
                'estimated_remaining_life': 40,
                'notes': 'Premium maintenance standards. All systems functioning optimally',
            },
            {
                'project_name': 'Medical Center Building',
                'city': 'Mecca',
                'address': 'Al-Haram District, Mecca 24231',
                'gps_latitude': 21.4225,
                'gps_longitude': 39.8262,
                'building_type': 'Healthcare',
                'primary_use': 'Medical Facility',
                'gross_built_area': 35000,
                'number_of_floors': 8,
                'construction_year': 2014,
                'current_year': 2025,
                'estimated_life_time': 50,
                'planned_retirement_year': 2064,
                'last_renovation_date': date(2023, 1, 8),
                'inspection_date': date(2025, 12, 5),
                'fm_contractor': 'Healthcare Facilities Inc',
                'system_threshold': 88.0,
                'inspection_result': 'Passed',
                'building_score': 86.5,
                'fm_performance': 90.0,
                'government_compliance': 'Complied',
                'high_priority_classified': 0,
                'fire_life_safety': 92.0,
                'total_economic_life': 50,
                'chronological_age': 11,
                'estimated_effective_age': 9,
                'estimated_remaining_life': 41,
                'notes': 'Strict compliance with healthcare standards. Recent renovations maintained',
            },
        ]
        
        # Add all samples
        added_count = 0
        for data in samples:
            # Check if project already exists
            existing = ProjectInspection.query.filter_by(
                project_name=data['project_name'],
                city=data['city']
            ).first()
            
            if not existing:
                inspection = ProjectInspection(user_id=demo_user.id, **data)
                db.session.add(inspection)
                added_count += 1
                print(f"✅ Added: {data['project_name']} ({data['city']})")
            else:
                print(f"⏭️  Skipped: {data['project_name']} (already exists)")
        
        # Commit all changes
        if added_count > 0:
            db.session.commit()
            print(f"\n✅ Successfully added {added_count} new inspections!")
        else:
            print("\nℹ️  No new inspections were added (all exist)")
        
        # Show total count
        total = ProjectInspection.query.count()
        print(f"\n📊 Total inspections in database: {total}")
        
        print("=" * 70)
        print("✅ SAMPLE DATA LOADED SUCCESSFULLY!")
        print("=" * 70)
        print("\n🔗 Access your data:")
        print("   • App: https://web-production-c26d2.up.railway.app")
        print("   • API: https://web-production-c26d2.up.railway.app/api/inspections")
        print("   • Power BI: Refresh your query")

if __name__ == '__main__':
    try:
        add_sample_data()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
