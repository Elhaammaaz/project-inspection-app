"""
Seed database from Excel BCAR file
Loads all lookup tables, systems hierarchy, compliance areas from the actual Excel
"""

import pandas as pd
import os
from app import create_app, db
from models import (
    System, Subsystem, Component, Rate, Weight, Responsibility, Priority,
    ComplianceArea
)

def seed_from_excel():
    """Load all data from BCAR Excel file"""
    
    excel_path = 'Building Assessment Report (BCAR) – v12.xlsx'
    if not os.path.exists(excel_path):
        print(f"ERROR: Excel file not found: {excel_path}")
        return False
    
    xl = pd.ExcelFile(excel_path)
    df_lists = pd.read_excel(xl, sheet_name='Lists', header=0)
    
    # ==================== RATES (0-5) ====================
    print("Seeding Rates...")
    if Rate.query.first() is None:
        rates = [
            (0, 'Not Rated / Not Applicable'),
            (1, 'Critical – Immediate action required'),
            (2, 'Poor – Major deficiencies'),
            (3, 'Fair – Minor deficiencies'),
            (4, 'Good – Acceptable with observations'),
            (5, 'Excellent – Fully compliant')
        ]
        for val, desc in rates:
            db.session.add(Rate(rate_value=val, description=desc, active=True))
        db.session.commit()
        print(f"  Added {len(rates)} rates")
    
    # ==================== WEIGHTS (0-5) ====================
    print("Seeding Weights...")
    if Weight.query.first() is None:
        weight_vals = df_lists['Rate/Weight'].dropna().unique()
        for w in sorted(weight_vals):
            if w >= 0 and w <= 5:
                db.session.add(Weight(weight_value=float(w), description=f'Weight {w}', active=True))
        db.session.commit()
        print(f"  Added weights 0-5")
    
    # ==================== PRIORITIES ====================
    print("Seeding Priorities...")
    if Priority.query.first() is None:
        priorities = [
            ('P1', 1, 'Critical – Immediate'),
            ('P2', 2, 'High – Within 7 days'),
            ('P3', 3, 'Medium – Within 30 days'),
            ('P4', 4, 'Low – Scheduled maintenance')
        ]
        for name, order, desc in priorities:
            db.session.add(Priority(priority_name=name, order=order, active=True))
        db.session.commit()
        print(f"  Added {len(priorities)} priorities")
    
    # ==================== RESPONSIBILITIES ====================
    print("Seeding Responsibilities...")
    if Responsibility.query.first() is None:
        resp_list = ['MEP Contractor', 'Main Contractor', 'FM Contractor', 'Specialist Vendor', 'Client/Owner']
        for name in resp_list:
            db.session.add(Responsibility(name=name, active=True))
        db.session.commit()
        print(f"  Added {len(resp_list)} responsibilities")
    
    # ==================== SYSTEMS, SUBSYSTEMS, COMPONENTS ====================
    print("Seeding Systems Hierarchy...")
    if System.query.first() is None:
        # Parse the Lists sheet to get System -> Subsystem -> Component hierarchy
        # The data is structured in columns: Priority (has System), Status (has Subsystem), Responsibility (has Component)
        
        # Find where the actual hierarchy data starts
        priority_col = df_lists['Priority'].dropna().tolist()
        status_col = df_lists['Status'].dropna().tolist()
        resp_col = df_lists['Responsibility'].dropna().tolist()
        
        # Find the index where "System" appears in priority column
        sys_start_idx = None
        for i, val in enumerate(priority_col):
            if val == 'System':
                sys_start_idx = i
                break
        
        if sys_start_idx is None:
            print("  WARNING: Could not find system hierarchy in Excel")
            return False
        
        # Extract systems, subsystems, components
        systems_data = priority_col[sys_start_idx + 1:]
        subsystems_data = status_col[sys_start_idx + 1:]
        components_data = resp_col[sys_start_idx + 1:]
        
        # Build hierarchy
        current_system = None
        current_subsystem = None
        system_order = 0
        subsystem_order = 0
        component_order = 0
        
        # Track unique systems
        unique_systems = list(dict.fromkeys([s for s in systems_data if pd.notna(s)]))
        
        for sys_name in unique_systems:
            # Create system
            sys_code = sys_name.replace(' ', '_').replace('/', '_')
            system = System(
                system_code=sys_code,
                system_name=sys_name,
                order=system_order,
                active=True
            )
            db.session.add(system)
            db.session.flush()  # Get ID
            system_order += 1
            
            # Find all subsystems for this system
            subsystem_order = 0
            seen_subsystems = set()
            
            for i, (s, sub, comp) in enumerate(zip(systems_data, subsystems_data, components_data)):
                if s == sys_name and pd.notna(sub) and sub not in seen_subsystems:
                    seen_subsystems.add(sub)
                    sub_code = f"{sys_code[:3]}-{sub[:3].upper()}"
                    subsystem = Subsystem(
                        system_id=system.id,
                        subsystem_code=sub_code,
                        subsystem_name=sub,
                        order=subsystem_order,
                        active=True
                    )
                    db.session.add(subsystem)
                    db.session.flush()
                    subsystem_order += 1
                    
                    # Find all components for this subsystem
                    component_order = 0
                    seen_components = set()
                    
                    for j, (s2, sub2, comp2) in enumerate(zip(systems_data, subsystems_data, components_data)):
                        if s2 == sys_name and sub2 == sub and pd.notna(comp2) and comp2 not in seen_components:
                            seen_components.add(comp2)
                            comp_code = f"{sub_code}-{str(component_order + 1).zfill(3)}"
                            component = Component(
                                subsystem_id=subsystem.id,
                                component_code=comp_code,
                                component_name=comp2,
                                order=component_order,
                                active=True
                            )
                            db.session.add(component)
                            component_order += 1
        
        db.session.commit()
        print(f"  Added {System.query.count()} systems")
        print(f"  Added {Subsystem.query.count()} subsystems")
        print(f"  Added {Component.query.count()} components")
    
    # ==================== COMPLIANCE AREAS ====================
    print("Seeding Compliance Areas...")
    if ComplianceArea.query.first() is None:
        df_comp = pd.read_excel(xl, sheet_name='Government Compliance Checklist', header=None)
        
        # Parse compliance areas from Excel
        seen_areas = set()
        for i in range(2, len(df_comp)):
            row = df_comp.iloc[i]
            area = row[1] if pd.notna(row[1]) else None
            if area and area not in seen_areas and area != 'Area':
                seen_areas.add(area)
                db.session.add(ComplianceArea(
                    area_name=area,
                    description=area,
                    regulation_code=f"GC-{len(seen_areas):02d}",
                    active=True
                ))
        
        db.session.commit()
        print(f"  Added {len(seen_areas)} compliance areas")
    
    print("\n✓ Seeding complete!")
    return True


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # Clear existing data if needed
        import sys
        if '--reset' in sys.argv:
            print("Resetting lookup tables...")
            Component.query.delete()
            Subsystem.query.delete()
            System.query.delete()
            Rate.query.delete()
            Weight.query.delete()
            Priority.query.delete()
            Responsibility.query.delete()
            ComplianceArea.query.delete()
            db.session.commit()
        
        seed_from_excel()
