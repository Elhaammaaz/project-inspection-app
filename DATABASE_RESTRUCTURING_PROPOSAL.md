# 🔍 DATABASE SCHEMA RESTRUCTURING PROPOSAL

## **Current Data vs Required Data Analysis**

Based on your inspection report, I've identified what needs to be added/replaced:

---

## **📊 NEW TABLES REQUIRED:**

### **1. Assessment Categories Table**
```
assessment_categories:
  - id (PK)
  - project_inspection_id (FK)
  - category_name (e.g., "Inspection Result", "Building Score", "FM Performance")
  - category_value
  - status (Pass/Fail/Warning)
  - created_at
```

### **2. Inspection Systems Table** 
```
inspection_systems:
  - id (PK)
  - project_inspection_id (FK)
  - system_name (Fire_LifeSafety, Electrical, Emergency_Power, etc.)
  - item_count (35, 30, 5, etc.)
  - score_percentage (54%, 73%, 78%, etc.)
  - weight (17.00, 10.00, 2.00, etc.)
  - weighted_score (9%, 7%, 2%, etc.)
  - status (Critical/Warning/Good)
  - created_at
```

### **3. Priority Items Table**
```
priority_items:
  - id (PK)
  - project_inspection_id (FK)
  - system_id (FK to inspection_systems)
  - priority_level (1-5, where 1 is critical)
  - description
  - corrective_action_required
  - status (Open/In Progress/Resolved)
  - due_date
  - created_at
  - updated_at
```

### **4. Compliance Assessment Table**
```
compliance_assessment:
  - id (PK)
  - project_inspection_id (FK)
  - assessment_category (Inspection Result, Government Compliance, etc.)
  - finding (Pass, Fail, Partial, etc.)
  - details
  - evidence_notes
  - reviewed_date
  - created_at
```

---

## **📝 ENHANCED ProjectInspection Fields (Current → New):**

| Current Field | Type | Action | New Changes |
|---|---|---|---|
| project_name | String | KEEP | ✓ |
| city | String | KEEP | ✓ |
| address | String | KEEP | ✓ |
| gps_latitude | Float | KEEP | ✓ |
| gps_longitude | Float | KEEP | ✓ |
| building_type | String | KEEP | ✓ |
| primary_use | String | KEEP | ✓ |
| gross_built_area | Float | KEEP | ✓ |
| number_of_floors | Integer | KEEP | ✓ |
| construction_year | Integer | KEEP | ✓ |
| current_year | Integer | KEEP | ✓ |
| last_renovation_date | Date | KEEP | ✓ |
| inspection_date | Date | KEEP | ✓ |
| fm_contractor | String | KEEP | ✓ |
| system_threshold | Float | KEEP | ✓ |
| inspection_result | String | REPLACE | → Now stored in assessment_categories |
| building_score | Float | REPLACE | → Now stored in assessment_categories |
| fm_performance | Float | REPLACE | → Now stored in assessment_categories |
| government_compliance | String | REPLACE | → Now stored in compliance_assessment |
| fire_life_safety | Float | REPLACE | → Now stored in inspection_systems |
| total_economic_life | Integer | KEEP | ✓ |
| chronological_age | Integer | KEEP | ✓ |
| estimated_effective_age | Integer | KEEP | ✓ |
| estimated_remaining_life | Integer | KEEP | ✓ |
| high_priority_classified | Integer | REPLACE | → Now counted from priority_items |
| notes | Text | ENHANCE | → Now linked to priority_items descriptions |
| estimated_life_time | Integer | KEEP | ✓ |
| planned_retirement_year | Integer | KEEP | ✓ |
| **NEW** | | ADD | inspection_status (draft/completed/reviewed) |
| **NEW** | | ADD | inspection_by (inspector name) |
| **NEW** | | ADD | reviewed_by (reviewer name) |
| **NEW** | | ADD | total_systems_count (dynamic from inspection_systems) |
| **NEW** | | ADD | critical_items_count (dynamic from priority_items) |

---

## **🗂️ NEW DATABASE STRUCTURE DIAGRAM:**

```
users (unchanged)
├── id
├── email
├── active
└── ...

project_inspections (ENHANCED)
├── id (PK)
├── user_id (FK)
├── project_name
├── city, address, GPS
├── building_type, primary_use
├── area, floors
├── dates (construction, renovation, inspection, current)
├── fm_contractor
├── life metrics
├── inspection_status ← NEW
├── inspection_by ← NEW
├── reviewed_by ← NEW
├── created_at
└── updated_at
    │
    ├─→ assessment_categories (1:many)
    │   ├── id
    │   ├── category_name (Inspection Result, Building Score, FM Perf)
    │   ├── category_value
    │   ├── status
    │   └── created_at
    │
    ├─→ compliance_assessment (1:many)
    │   ├── id
    │   ├── assessment_category
    │   ├── finding
    │   ├── details
    │   ├── evidence_notes
    │   └── reviewed_date
    │
    ├─→ inspection_systems (1:many)
    │   ├── id
    │   ├── system_name (Fire_LifeSafety, Electrical, etc.)
    │   ├── item_count (35, 30, 5)
    │   ├── score_percentage (54%, 73%, 78%)
    │   ├── weight (17.00, 10.00)
    │   ├── weighted_score (9%, 7%)
    │   ├── status
    │   └── created_at
    │       │
    │       └─→ priority_items (1:many)
    │           ├── id
    │           ├── priority_level (1-5)
    │           ├── description
    │           ├── corrective_action
    │           ├── status
    │           ├── due_date
    │           └── created_at
    │
    └─→ inspection_files (optional - for attachments)
        ├── id
        ├── file_name
        ├── file_type
        ├── file_path
        └── uploaded_at
```

---

## **📋 COMPLETE FIELD MAPPING - Current vs New:**

### **Project Information Section (NO CHANGES)**
✓ Project/Building Name
✓ City
✓ Address
✓ GPS Coordinates
✓ Building Type
✓ Primary Use
✓ Gross Built Area (m²)
✓ No. of Floors
✓ Last Major Renovation Date
✓ FM Contractor
✓ Current Year
✓ Construction Year
✓ Estimated Life Time
✓ Planned Asset Retirement
✓ System Threshold (%)
✓ Inspection Date

### **Assessment Results Section (REORGANIZED)**
```
Current → New Structure

inspection_result (String)
  ↓
assessment_categories.finding
  - Pass
  - Fail
  - Partial
  - Pending

building_score (Float)
  ↓
assessment_categories.category_value
  - Score: 183 (0-100 scale or weighted)

fm_performance (Float)
  ↓
assessment_categories.category_value
  - Value: 61%

government_compliance (String)
  ↓
compliance_assessment.finding
  - Status: Not Complied

fire_life_safety (Float)
  ↓
inspection_systems[Fire_LifeSafety].score_percentage
  - Score: 54%

high_priority_classified (Integer)
  ↓
COUNT(priority_items WHERE priority_level >= 3)
  - Count: 183 items

Assessment Summary:
├── Inspection Result: FAIL
├── Building Score: 64%
├── High Priority Items: 183
├── FM Performance: 61%
└── Government Compliance: Not Complied
```

### **Systems Performance Section (NEW - Currently Missing)**
```
NEW Table: inspection_systems

System | Item Count | Score % | Weight | Weighted Score
─────────────────────────────────────────────────────────
Fire_LifeSafety         | 35 | 54% | 17.00 | 9%
Electrical              | 30 | 73% | 10.00 | 7%
Emergency_Power         | 5  | 78% | 2.00  | 2%
Mechanical_HVAC         | 35 | 60% | 3.00  | 2%
Plumbing_Water          | 35 | 63% | 8.00  | 5%
Gas_Systems             | 35 | 63% | 2.00  | 1%
Vertical_Transportation | 35 | 63% | 6.00  | 4%
BMS_Controls            | 35 | 63% | 6.00  | 4%
ELV_Systems             | 28 | 63% | 3.00  | 2%
Security_Safety         | 35 | 67% | 3.00  | 2%
Digital_ICT             | 35 | 64% | 2.00  | 1%
Structural              | 35 | 63% | 4.00  | 3%
Architectural_Fabric    | 35 | 64% | 2.00  | 1%
External_Parking        | 35 | 66% | 1.00  | 1%
Landscape               | 35 | 64% | 1.00  | 1%
Pools_WaterFeatures     | 35 | 61% | 1.00  | 1%
Waste_Management        | 35 | 65% | 2.00  | 1%
Sustainability          | 35 | 61% | 1.00  | 1%
Compliance_Documentation| 35 | 61% | 12.00 | 7%
FM_Performance          | 35 | 67% | 7.00  | 5%
Governance_Readiness    | 36 | 68% | 7.00  | 5%
─────────────────────────────────────────────────────────
TOTAL ITEMS             | 634| -   | 100.00| 100%
```

### **Priority Items Section (NEW - Currently Missing)**
```
NEW Table: priority_items

Priority Level (1-5):
1 = Critical (Must fix immediately)
2 = High (Fix within 30 days)
3 = Medium (Fix within 90 days)
4 = Low (Fix within 6 months)
5 = Maintenance (Fix during next maintenance)

Example entries from your chart:
├── Fire_LifeSafety System → 54% → 1 Critical Item
├── Electrical System → 73% → 0 Critical Items
├── HVAC System → 60% → 2 Critical Items
├── Plumbing → 63% → 1 Critical Item
└── ... (183 total high priority items)

Status: Open / In Progress / Resolved
```

### **Notes Section (ENHANCED)**
```
Current: Text blob
  ↓
NEW: Structured by system + priority

notes.system_reference → Links to inspection_systems
notes.priority_level → Links to priority_items
notes.corrective_action → Required action steps
notes.evidence → Supporting details
notes.attachments → File references
```

---

## **🎯 SUMMARY OF CHANGES:**

### **Tables to Create:**
1. ✅ `assessment_categories` - Stores inspection results
2. ✅ `inspection_systems` - Stores system performance data
3. ✅ `priority_items` - Stores critical findings
4. ✅ `compliance_assessment` - Stores compliance findings

### **Fields to Add to project_inspections:**
1. ✅ `inspection_status` - draft/completed/reviewed
2. ✅ `inspection_by` - Inspector name
3. ✅ `reviewed_by` - Reviewer name
4. ✅ `total_systems_count` - Auto-calculated
5. ✅ `critical_items_count` - Auto-calculated

### **Fields to Reorganize (Not Delete):**
- `inspection_result` → Still queryable via assessment_categories
- `building_score` → Still queryable via assessment_categories
- `fm_performance` → Still queryable via assessment_categories
- `government_compliance` → Still queryable via compliance_assessment
- `fire_life_safety` → Still queryable via inspection_systems
- `high_priority_classified` → Still queryable via COUNT priority_items

### **Data Integrity:**
✅ All existing data preserved
✅ Better normalization
✅ Supports 20+ systems per inspection
✅ Supports unlimited priority items
✅ Audit trail for compliance

---

## **🔄 Migration Plan (Zero Data Loss):**

```
Step 1: Create new tables
Step 2: Copy existing data to new structure
Step 3: Validate data consistency
Step 4: Update API endpoints
Step 5: Update UI forms
Step 6: Test thoroughly
Step 7: Deprecate old fields (optional)
Step 8: Archive old data (optional)
```

---

## **✅ BENEFITS OF THIS STRUCTURE:**

1. **Scalability** - Handle any number of systems & priorities
2. **Flexibility** - Easy to add new assessment types
3. **Compliance** - Better audit trail
4. **Performance** - Faster queries with proper relationships
5. **Data Integrity** - Referential integrity via foreign keys
6. **UI/UX** - Easier to build dynamic forms
7. **Reporting** - Better Power BI integration

---

## **❓ READY FOR APPROVAL?**

This proposal includes:
✅ 4 new tables
✅ 5 new fields on project_inspections
✅ Support for 20+ building systems
✅ Support for unlimited priority items
✅ Full backward compatibility
✅ Complete data mapping

**Proceed with implementation? (Yes/No)**

If approved, I will:
1. ✅ Create database migrations
2. ✅ Update SQLAlchemy models
3. ✅ Build robust forms (UI/UX)
4. ✅ Create API endpoints
5. ✅ Build inspection forms with system picker
6. ✅ Add priority items management
7. ✅ Update dashboard
8. ✅ Test everything
9. ✅ Push to GitHub
