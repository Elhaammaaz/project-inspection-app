# Building Assessment Report (BCAR) v12 - Analysis

## File: Building Assessment Report (BCAR) – v12.xlsx

### Overview
This is a comprehensive Building Assessment & Compliance Reporting tool with 7 interconnected sheets containing multi-page assessment data, checklists, test registers, and corrective action tracking.

---

## Sheet Structure

### 1. **User Manual** (70 rows × 19 columns)
- Documentation/reference sheet for end users
- Contains instructions and guidelines
- **Action**: Display in app as reference/help section

### 2. **Executive Assessment Summary** (124 rows × 74 columns)
**Purpose**: Main input form & calculated summary report
**Key Sections**:

#### A. Project Information (Input Fields)
- Project / Building Name
- City
- Address
- GPS Coordinates (Latitude, Longitude)
- Building Type
- Primary Use
- Gross Built Area (m²)
- Number of Floors

#### B. Building Timeline & Details (Input Fields)
- Last Major Renovation Date
- FM Contractor / Service Provider
- Current Year
- Construction Year
- Estimated Life Time (years)
- Planned Asset Retirement Year
- System Threshold (%)
- Inspection Date

#### C. Calculated Results (Auto-calculated)
- **Inspection Result**: Pass/Fail status
- **Building Score**: Overall score percentage (0.53514 example = 53.514%)
- **High Priority Classified**: Count/flag
- **FM Performance**: Score
- **Government Compliance**: Status (Complied/Not Complied)
- **Fire & Life Safety**: Score
- **Total Economic Life**: Years
- **Chronological (Actual) Age**: Years calculated from construction year
- **Estimated Effective Age**: Years (condition-based)
- **Estimated Remaining Life**: Years (calculated)

#### D. Assessment Notes
- Auto-populated notes based on findings
- Shows requirement status
- Links to deficiencies and corrective actions

### 3. **Government Compliance Checklist** (35 rows × 8 columns)
**Purpose**: Track regulatory compliance requirements

**Columns**:
- Area (Legal & Municipal, Utility Connections, etc.)
- Requirement (specific compliance item)
- Status (Yes/No/Partial/N/A)
- Evidence Required (description of what's needed)
- Item Code (e.g., GC-LA-001)
- Evidence Ref (attachment reference)
- Remarks

**Key Categories**:
- Legal & Municipal Approvals (Building Completion, Occupancy License, Permits)
- Utility Connections (Electricity, Water, Sewerage)
- Safety Certificates (Fire, Pressure Equipment, Elevators)
- Insurance & Financial Documentation

### 4. **Lists** (302 rows × 12 columns)
**Purpose**: Lookup/dropdown tables for data validation

**Reference Data**:
- Priority levels: P1, P2, P3, P4
- Status options: Open, In Progress, Closed, Verified
- Responsibility: MEP Contractor, Main Contractor, FM Contractor, Specialist Vendor
- Evidence Types: Photo, Video, Test Report, IR Scan
- Years: 1900-2025 range
- Estimated Life Time: 0-50+ years
- System Threshold: 0.5-1.0 percentages
- Primary Use: RESIDENTIAL, COMMERCIAL, INDUSTRIAL, INSTITUTIONAL/PUBLIC
- Test Method Categories

### 5. **Building Assessment** (695 rows × 23 columns)
**Purpose**: Detailed inspection items for 21 building systems

**Structure** (per item):
- System: Category (Fire_LifeSafety, Structural, MEP, etc.)
- Subsystem: Component group
- Component: Specific item
- Item Code: Unique identifier (e.g., FL-CP-001)
- Inspection Item: What's being inspected
- Criteria: Pass/fail criteria
- Test Method: How to test
- Asset Tag No.: Equipment identifier
- Snag Location: Where issue found
- Snag Evidence Ref: Photo/document reference
- Snag Evidence Type: Photo, Video, Report, etc.
- Rate: Severity/priority rating
- Score %: Item score (0-100%)
- Item Weight: Weighting factor
- **Weighted Score**: Calculated (Score × Weight)

**Data**: 694 inspection items across building systems

### 6. **Test Register** (81 rows × 13 columns)
**Purpose**: Track all tests performed

**Columns**:
- Test ID: Unique test identifier
- Test Name: Description
- System: Which building system
- Standard / Reference: Test standard used
- Instrument: Equipment used
- Locations / Sampling: Where tested
- Acceptance Criteria: Pass threshold
- Readings: Test results
- Pass/Fail: Outcome
- Linked Item Codes: References to Building Assessment items
- Evidence Ref: Supporting documentation
- Witness: Person who witnessed test
- Date: Test date

**Data**: 80 test records

### 7. **CAPA Register** (63 rows × 11 columns)
**Purpose**: Track Corrective and Preventive Actions

**Columns**:
- CAPA ID: Unique identifier
- Priority: P1-P4
- System: Building system affected
- Item Code: Link to assessment item
- Finding: Issue description
- Required Action: What needs to be done
- Responsibility: Who's responsible
- Due Date: Deadline
- Estimated Cost: Budget
- Status: Open/In Progress/Closed
- Verification Evidence: Proof of completion

**Data**: 62 corrective action items

---

## Key Calculations & Formulas

1. **Building Score** = Weighted average of all system scores
2. **Chronological Age** = Current Year - Construction Year
3. **Estimated Effective Age** = Chronological Age × Condition Factor
4. **Estimated Remaining Life** = Total Economic Life - Estimated Effective Age
5. **Weighted Score (per item)** = Score % × Item Weight
6. **Fire & Life Safety Score** = Weighted average of FL system items
7. **FM Performance** = Overall system performance rating
8. **Compliance Status** = All mandatory compliance items met? (Yes/No)

---

## Database Design Approach

### Tables to Create:
1. **projects** - From Executive Assessment Summary (Project Info)
2. **project_assessments** - Calculated results per project
3. **compliance_items** - From Government Compliance Checklist
4. **compliance_status** - Track completion per project
5. **assessment_items** - From Building Assessment (694 items)
6. **assessment_scores** - Scores per project
7. **tests** - From Test Register
8. **capaactions** - From CAPA Register
9. **lookup_tables** - Priority, Status, Responsibility, etc.

### Relationships:
- One Project → Many Assessment Items
- One Project → Many Compliance Items
- One Project → Many Tests
- One Project → Many CAPA Actions
- Assessment Item → Test Results
- Assessment Item → CAPA Actions

---

## App Pages to Create

1. **Landing Page** - Features, benefits, login/register CTAs
2. **Login/Registration** - Secure authentication
3. **Dashboard** - Summary of all projects
4. **Project Upload** - Import Excel files
5. **Executive Summary** - Project info & calculated KPIs
6. **Building Assessment** - Detailed inspection items (searchable, filterable)
7. **Compliance Checklist** - Government requirements tracking
8. **Test Register** - All tests performed
9. **CAPA Register** - Corrective actions tracking
10. **Reports** - Summary reports & exports

---

## Upload Processing

When user uploads BCAR Excel file:
1. Parse all sheets
2. Extract project data from Executive Assessment Summary
3. Create project record in DB
4. Store all assessment items from Building Assessment sheet
5. Store compliance requirements from Government Compliance Checklist
6. Store test records from Test Register
7. Store CAPA items from CAPA Register
8. Calculate all metrics and store results
9. Make data available for viewing/editing through app pages

