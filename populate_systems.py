#!/usr/bin/env python
"""
Populate Sample Inspection with 21 Systems
Run this after migration to add demo data
"""

import os
import sys
from app import create_app
from models import db, User, ProjectInspection, InspectionSystem
from datetime import datetime, timedelta

# The 21 building systems with their data
SYSTEMS_DATA = [
    {"name": "Fire_LifeSafety", "item_count": 35, "score": 54, "weight": 17.00, "weighted_score": 9},
    {"name": "Electrical", "item_count": 30, "score": 73, "weight": 10.00, "weighted_score": 7},
    {"name": "Emergency_Power", "item_count": 5, "score": 78, "weight": 2.00, "weighted_score": 2},
    {"name": "Mechanical_HVAC", "item_count": 35, "score": 60, "weight": 9.00, "weighted_score": 5},
    {"name": "Plumbing_Water", "item_count": 35, "score": 69, "weight": 8.00, "weighted_score": 6},
    {"name": "Gas_Systems", "item_count": 35, "score": 69, "weight": 2.00, "weighted_score": 1},
    {"name": "Vertical_Transportation", "item_count": 35, "score": 79, "weight": 5.00, "weighted_score": 4},
    {"name": "BMS_Controls", "item_count": 35, "score": 63, "weight": 6.00, "weighted_score": 4},
    {"name": "ELV_Systems", "item_count": 28, "score": 63, "weight": 3.00, "weighted_score": 2},
    {"name": "Security_Safety", "item_count": 35, "score": 67, "weight": 3.00, "weighted_score": 2},
    {"name": "Digital_ICT", "item_count": 35, "score": 64, "weight": 2.00, "weighted_score": 1},
    {"name": "Structural", "item_count": 35, "score": 69, "weight": 4.00, "weighted_score": 3},
    {"name": "Architectural_Fabric", "item_count": 35, "score": 64, "weight": 2.00, "weighted_score": 1},
    {"name": "External_Parking", "item_count": 35, "score": 66, "weight": 1.00, "weighted_score": 1},
    {"name": "Landscape", "item_count": 35, "score": 64, "weight": 1.00, "weighted_score": 1},
    {"name": "Pools_WaterFeatures", "item_count": 35, "score": 61, "weight": 1.00, "weighted_score": 1},
    {"name": "Waste_Management", "item_count": 35, "score": 65, "weight": 2.00, "weighted_score": 1},
    {"name": "Sustainability", "item_count": 35, "score": 61, "weight": 1.00, "weighted_score": 1},
    {"name": "Compliance_Documentation", "item_count": 35, "score": 61, "weight": 12.00, "weighted_score": 7},
    {"name": "FM_Performance", "item_count": 35, "score": 61, "weight": 2.00, "weighted_score": 1},
    {"name": "Governance_Readiness", "item_count": 36, "score": 68, "weight": 7.00, "weighted_score": 5},
]


def populate_sample_data():
    """Create sample inspection with 21 systems"""
    
    app = create_app()
    with app.app_context():
        print("=" * 60)
        print("POPULATING SAMPLE DATA")
        print("=" * 60)
        
        try:
            # Step 1: Get or create demo user
            print("\n[1] Getting demo user...")
            demo_user = User.query.filter_by(email='demo@example.com').first()
            
            if not demo_user:
                print("   [!] Demo user not found. Creating...")
                demo_user = User(email='demo@example.com', full_name='Demo Admin', active=1)
                demo_user.set_password('demo123')
                demo_user.approved_at = datetime.utcnow()
                db.session.add(demo_user)
                db.session.commit()
                print("   ✓ Demo user created: demo@example.com / demo123 (ACTIVE)")
            else:
                print(f"   ✓ Demo user found: {demo_user.email}")
            
            # Step 2: Create sample inspection
            print("\n[2] Creating sample inspection...")
            
            inspection = ProjectInspection(
                user_id=demo_user.id,
                
                # Project Information
                project_name="Royal Hotel Resort",
                city="Riyadh",
                address="Diplomatic Quarter, P.O. Box 12345",
                gps_latitude=24.7204,
                gps_longitude=46.7048,
                
                # Building Details
                building_type="Hospitality",
                primary_use="Hotel",
                gross_built_area=85000,
                number_of_floors=25,
                
                # Dates & Timeline
                last_renovation_date=datetime(2021, 5, 12).date(),
                fm_contractor="Luxury FM Solutions LLC",
                current_year=2025,
                construction_year=2012,
                estimated_life_time=50,
                planned_retirement_year=2062,
                system_threshold=90,
                inspection_date=datetime(2025, 11, 25).date(),
                
                # Life & Aging Metrics
                total_economic_life=50,
                chronological_age=13,
                estimated_effective_age=10,
                estimated_remaining_life=40,
                
                # Assessment Results
                inspection_result="Fail",
                building_score=64,
                high_priority_classified=183,
                fm_performance=61,
                government_compliance="Not Complied",
                fire_life_safety=54,
                
                # Additional Info
                notes="Inspection completed. 183 high priority items identified. Major work required in Fire Safety and Electrical systems.",
                inspection_status="completed",
                inspection_by="Ahmed Al-Dosari",
                reviewed_by="Mohammed Al-Saud",
            )
            
            db.session.add(inspection)
            db.session.flush()  # Get the ID without committing
            
            print(f"   ✓ Inspection created with ID: {inspection.id}")
            
            # Step 3: Add 21 systems
            print("\n[3] Adding 21 building systems...")
            
            for idx, sys_data in enumerate(SYSTEMS_DATA, 1):
                # Determine status based on score
                if sys_data['score'] >= 70:
                    status = "Good"
                elif sys_data['score'] >= 50:
                    status = "Warning"
                else:
                    status = "Critical"
                
                system = InspectionSystem(
                    project_inspection_id=inspection.id,
                    system_name=sys_data['name'],
                    item_count=sys_data['item_count'],
                    score_percentage=sys_data['score'],
                    weight=sys_data['weight'],
                    weighted_score=sys_data['weighted_score'],
                    status=status
                )
                db.session.add(system)
                print(f"   {idx:2d}. {sys_data['name']:30s} - Score: {sys_data['score']:3.0f}% - Weight: {sys_data['weight']:6.2f} - Status: {status}")
            
            # Step 4: Commit all changes
            print("\n[4] Saving to database...")
            db.session.commit()
            print("   ✓ All data saved successfully")
            
            # Step 5: Verify data
            print("\n[5] Verifying data...")
            inspection = ProjectInspection.query.get(inspection.id)
            systems_count = len(inspection.systems)
            total_weighted = sum(s.weighted_score for s in inspection.systems)
            
            print(f"   ✓ Inspection ID: {inspection.id}")
            print(f"   ✓ Project: {inspection.project_name}")
            print(f"   ✓ Building Score: {inspection.building_score}")
            print(f"   ✓ Systems Count: {systems_count}/21")
            print(f"   ✓ Total Weighted Score: {total_weighted}%")
            
            print("\n" + "=" * 60)
            print("✅ SAMPLE DATA POPULATED SUCCESSFULLY!")
            print("=" * 60)
            print("\nYou can now:")
            print("1. Login with: demo@example.com / demo123")
            print("2. View the inspection with 21 systems")
            print("3. Access Power BI dashboard with /api/inspections\n")
            
            return True
            
        except Exception as e:
            print(f"\n   [ERROR] Failed to populate data: {str(e)}")
            db.session.rollback()
            import traceback
            traceback.print_exc()
            return False


if __name__ == '__main__':
    populate_sample_data()
