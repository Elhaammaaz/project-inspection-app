# BCAR Excel Simulation App - Architecture Guide

## Overview

This application **simulates the Excel Building Assessment Report (BCAR)** as a web-based application. It does NOT import the Excel file into a database. Instead, it REPLICATES how the Excel file works with all its calculations, data structures, and workflows.

## How It Works

### 1. **Data Seeding (One-time Setup)**

When you create a new project, you have the option to "seed" the project data from the Excel file. This:
- Reads all 694 inspection items from the "Building Assessment" sheet
- Loads all government compliance items from "Government Compliance Checklist"
- Imports test records from "Test Register"
- Imports CAPA records from "CAPA Register"
- Extracts dropdown reference data from "Lists" sheet

This data becomes the **permanent structure** for that project - it doesn't change.

### 2. **Data Entry (User-Editable Fields)**

For each assessment item, users can edit ONLY these fields:
- **Rate** (1-5 dropdown) - How well does it meet criteria?
- **Item Weight** (0.1-5.0 dropdown) - Importance of this item
- **Evidence Type** (Photo, Video, Report, IR Scan) - Type of supporting evidence
- **Priority** (P1-P4) - Urgency classification
- **Status** (Open, In Progress, Closed, Verified) - Current status
- **Remarks** - Additional notes
- **Due Date** - Target completion date
- **Responsibility** - Who is responsible

All other fields are read-only (System, Subsystem, Component, Item Code, Criteria, etc.)

### 3. **Automatic Calculations (Like Excel)**

All metrics calculate automatically in real-time based on user edits:

```
Score % = Rate / 5 * 100
Weighted Score = Score % * Item Weight / 100
System Average = Average of all Score % for that system
Building Score = Average of all System Weighted Scores
```

These match exactly what Excel calculates!

## File Structure

```
app.py                    # Flask application with 20+ routes
models.py                 # Database models (Project, AssessmentItem, etc.)
calculations.py           # CalculationEngine - all Excel formulas
forms.py                  # WTForms for data entry
seed_data.py              # BCAREXCELSeeder - loads Excel data into DB
config.py                 # Configuration settings
templates/                # HTML templates for web interface
  landing.html            # Welcome page
  login.html              # User login
  register.html           # User registration
  dashboard.html          # Project list with statistics
  project_form.html       # Create/edit project info
  project_summary.html    # Executive Summary dashboard
  assessment_items.html   # List view of all 694 items (searchable/filterable)
  assessment_item_edit.html  # Edit single item
  compliance_items.html   # Government compliance checklist
  test_records.html       # Test register
  capa_records.html       # CAPA register
  system_weights.html     # System weight adjustments
```

## Database Models

### Project
Stores project information like:
- Building name, type, location
- Construction year, planned retirement year
- Inspection date, system threshold
- All fields from Excel "Executive Assessment Summary" sheet rows 5-15

### AssessmentItem (694 pre-loaded items)
Each of the 694 inspection items with:
- **Fixed fields** (read-only): System, Subsystem, Component, Item Code, Criteria, Test Method
- **Editable fields**: Rate, Item Weight, Priority, Status, Responsibility, Evidence, Remarks, Due Date
- **Calculated fields** (automatic): Score %, Weighted Score

### ComplianceItem
Government compliance tracking items with Status field

### TestRecord
Test register items for tracking testing activities

### CAPARecord
Corrective and Preventive Actions register

### SystemWeight
Per-system weighting adjustments for Building Score calculation

## Workflow Example

### Step 1: User creates a new project
```
/project/new → Fill in building info (like Excel form) → Save
```

### Step 2: System seeds Excel data
```
/project/{id}/seed → Loads 694 items + compliance + tests + CAPA → Redirect to project summary
```

### Step 3: User edits assessment items
```
/project/{id}/assessment → See all 694 items in table view
  → Filter by system, priority, status
  → Click item to edit
  → Change Rate (1-5), Weight, Priority, Status
  → Save → Score % and Weighted Score auto-calculate
  → Building Score updates automatically
```

### Step 4: View executive summary
```
/project/{id} → Dashboard shows:
  - Building Score (%)
  - Inspection Result (Pass/Fail/Needs Attention)
  - High Priority Items count (P1 + P2)
  - Fire & Life Safety score
  - Government Compliance status (Complied/Not Complied)
  - Age Analysis (Chronological, Effective, Remaining Life)
  - System breakdown (all 12 systems with scores)
```

### Step 5: Track compliance and actions
```
/project/{id}/compliance → Manage compliance items
/project/{id}/tests → Track test results
/project/{id}/capa → Manage corrective actions
```

## Calculation Engine (calculations.py)

This is where ALL Excel formulas are replicated:

```python
# Score calculation
score_percent = (rate / 5.0) * 100

# Weighted score
weighted_score = (score_percent * item_weight) / 100

# System metrics
system_avg_score = average(all score_percent for items in system)
system_weighted = (total_weighted * system_weight) / 100

# Building score
building_score = average(all system_weighted_scores)

# Inspection result
if building_score >= 100:
    return "Pass"
elif building_score >= threshold:
    return "Passed but Need Attention"
else:
    return "Fail"

# Compliance status
if any(item.status != "Yes"):
    return "Not Complied"
else:
    return "Complied"

# Age analysis
chronological_age = current_year - construction_year
remaining_life = planned_retirement_year - current_year
```

## Data Seeding (seed_data.py)

The `BCAREXCELSeeder` class handles loading Excel data:

```python
seeder = BCAREXCELSeeder('Building Assessment Report (BCAR) – v12.xlsx')
seeder.seed_all(project_id)
```

What it seeds:
1. **Assessment Items** (694 items from Building Assessment sheet)
   - Columns A-D: System, Subsystem, Component, Item Code (fixed)
   - Columns 5-11: Item description, criteria, test method, asset tag, etc (fixed)
   - Columns 12-14: Rate (editable), Item Weight (editable), Evidence (editable)
   - Columns 15-23: Priority, Status, Responsibility, CAPA ID, Due Date, Remarks (editable)

2. **Compliance Items** (from Government Compliance Checklist)
   - Fixed: Compliance area, description
   - Editable: Status, Remarks

3. **Test Records** (from Test Register)
   - Fixed: Test code, description, system
   - Editable: Test date, result, conducted by, remarks

4. **CAPA Records** (from CAPA Register)
   - Fixed: CAPA ID, finding description, root cause
   - Editable: Action, responsible party, dates, status

5. **System Weights** (initialized for all systems)
   - Default weight: 1.0 (can be adjusted by user)

6. **Lookup Tables** (from Lists sheet)
   - Priority: P1, P2, P3, P4
   - Status: Open, In Progress, Closed, Verified
   - Responsibility: MEP Contractor, Main Contractor, FM Contractor, Specialist, Client/Owner

## Systems in BCAR

The 12 building systems tracked:
1. Fire_LifeSafety
2. Electrical
3. Emergency_Power
4. Mechanical_HVAC
5. Plumbing_Water
6. Gas_Systems
7. Vertical_Transportation
8. BMS_Controls
9. ELV_Systems
10. Security_Safety
11. Digital_ICT
12. (Others from Excel)

Each system can be weighted differently, and the Building Score is calculated as the weighted average.

## Key Features

✅ **Excel Simulation**: App replicates exactly how Excel works with same formulas
✅ **694 Items Pre-loaded**: All items come from Excel file structure
✅ **Smart Dropdowns**: Only editable fields have dropdowns (Rate, Weight, Status, Priority)
✅ **Real-time Calculations**: All metrics update instantly on edit
✅ **Searchable/Filterable**: Find items by system, priority, status, code
✅ **Multi-sheet Support**: Compliance, Tests, CAPA all tracked separately
✅ **User Accounts**: Secure login, multiple users can have multiple projects
✅ **Executive Summary**: Dashboard view like Excel's summary sheet
✅ **Age Analysis**: Automatic calculations for building lifecycle
✅ **System Weighting**: Adjust weight of each system independently

## Running the App

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment variables (optional for PostgreSQL)
export DATABASE_URL="postgresql://user:pass@localhost/bcar"

# 3. Create database tables
python -c "from app import create_app; app = create_app(); app.app_context().push()"

# 4. Run the app
python app.py

# 5. Navigate to http://localhost:5000
# 6. Register → Create Project → Seed Data → Start using!
```

## Comparison: Excel vs App

| Feature | Excel | App |
|---------|-------|-----|
| Data Entry | Multiple cells on 694 rows | Web form with validation |
| Calculations | Formulas in columns M, O, etc | Python calculations.py |
| Filtering | Excel filters | Web UI with search + filters |
| Multi-user | File sharing (not ideal) | Secure login + separate projects |
| Compliance tracking | Manual checklist | Dedicated page with status tracking |
| Test & CAPA | Separate sheets | Dedicated pages with full CRUD |
| Age analysis | Excel formulas | Auto-calculated on dashboard |
| Reports | Static sheets | Dynamic HTML + PDF export ready |
| Backup | Manual | Database backups |

## Notes

- This is a **simulation**, not an importer. The Excel file is read once to populate the database, then the app works independently.
- All data is stored in a PostgreSQL database (can use SQLite for development).
- The app is designed to be used like a form-based data entry system, similar to how Excel is used but with better UI/UX.
- All calculations are done in Python code (not SQL), making them easy to modify and debug.
- The app respects the structure of the Excel file exactly - all 694 items, all 12 systems, all field names.
