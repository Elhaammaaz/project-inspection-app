# BCAR Database Documentation
## Building Condition Assessment Report System

---

## 📊 Entity Relationship Diagram (ERD)

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    BCAR DATABASE ARCHITECTURE                                            │
│                                                                                                          │
│  ┌─────────────┐                                                                                         │
│  │   USERS     │ ◄──────────────────────────────────────────────────────────────────────────────────┐   │
│  │   (PK: id)  │                                                                                    │   │
│  └──────┬──────┘                                                                                    │   │
│         │ 1:M                                                                                       │   │
│         ▼                                                                                           │   │
│  ┌─────────────┐     1:M      ┌─────────────────┐     1:M     ┌───────────────────┐                │   │
│  │  BUILDINGS  │─────────────►│   ASSESSMENTS   │────────────►│  ASSESSMENT_ITEMS │                │   │
│  │  (PK: id)   │              │   (PK: id)      │             │     (PK: id)      │                │   │
│  │  FK: user   │              │  FK: building   │             │  FK: assessment   │                │   │
│  └──────┬──────┘              └─────────────────┘             │  FK: system       │                │   │
│         │                                                      │  FK: subsystem    │                │   │
│         │ 1:M                                                  │  FK: component    │                │   │
│         ├──────────────────────────────────────────────────────┤  FK: responsibility│               │   │
│         │                                                      └─────────┬─────────┘                │   │
│         │                                                                │                          │   │
│         │ 1:M      ┌───────────────────────┐     1:M     ┌──────────────┴────────┐                 │   │
│         ├─────────►│ COMPLIANCE_CHECKLISTS │────────────►│   COMPLIANCE_ITEMS    │                 │   │
│         │          │      (PK: id)         │             │      (PK: id)         │                 │   │
│         │          │   FK: building        │             │   FK: checklist       │                 │   │
│         │          └───────────────────────┘             │   FK: compliance_area │                 │   │
│         │                                                └───────────────────────┘                 │   │
│         │                                                                                          │   │
│         │ 1:M      ┌─────────────────┐                                                             │   │
│         ├─────────►│  SYSTEM_SCORES  │◄─────────────────┐                                          │   │
│         │          │    (PK: id)     │                  │                                          │   │
│         │          │ FK: building    │                  │                                          │   │
│         │          │ FK: system      │                  │                                          │   │
│         │          └─────────────────┘                  │                                          │   │
│         │                                               │                                          │   │
│         │ 1:M      ┌─────────────────┐                  │                                          │   │
│         ├─────────►│  TEST_REGISTER  │                  │                                          │   │
│         │          │    (PK: id)     │                  │                                          │   │
│         │          │ FK: building    │──────────────────┤                                          │   │
│         │          │ FK: system      │                  │                                          │   │
│         │          └────────┬────────┘                  │                                          │   │
│         │                   │ M:M                       │                                          │   │
│         │                   ▼                           │                                          │   │
│         │          ┌─────────────────┐                  │                                          │   │
│         │          │ TEST_ITEM_LINKS │                  │                                          │   │
│         │          │    (PK: id)     │                  │                                          │   │
│         │          │ FK: test_record │                  │                                          │   │
│         │          │FK: assess_item  │                  │                                          │   │
│         │          └─────────────────┘                  │                                          │   │
│         │                                               │                                          │   │
│         │ 1:M      ┌─────────────────┐                  │                                          │   │
│         ├─────────►│  CAPA_REGISTER  │──────────────────┤                                          │   │
│         │          │    (PK: id)     │                  │                                          │   │
│         │          │ FK: building    │                  │        ┌─────────────┐                   │   │
│         │          │ FK: system      │                  │        │   SYSTEMS   │                   │   │
│         │          │FK: assess_item  │                  └───────►│  (PK: id)   │                   │   │
│         │          │FK: responsibility                           └──────┬──────┘                   │   │
│         │          └─────────────────┘                                  │ 1:M                      │   │
│         │                                                               ▼                          │   │
│         │ 1:1      ┌───────────────────────────┐                 ┌─────────────┐                   │   │
│         └─────────►│ EXECUTIVE_DASHBOARD_SUMMARY│                │ SUBSYSTEMS  │                   │   │
│                    │         (PK: id)           │                │  (PK: id)   │                   │   │
│                    │      FK: building          │                │ FK: system  │                   │   │
│                    └───────────────────────────┘                 └──────┬──────┘                   │   │
│                                                                         │ 1:M                      │   │
│                                                                         ▼                          │   │
│  ┌─────────────────────────────────────────────────────────────┐ ┌─────────────┐                   │   │
│  │                    LOOKUP TABLES                             │ │ COMPONENTS  │                   │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌────────────────────┐   │ │  (PK: id)   │                   │   │
│  │  │ RATES_LOOKUP │ │WEIGHTS_LOOKUP│ │RESPONSIBILITIES_   │   │ │FK: subsystem│                   │   │
│  │  │   (PK: id)   │ │   (PK: id)   │ │    LOOKUP          │   │ └─────────────┘                   │   │
│  │  └──────────────┘ └──────────────┘ │   (PK: id)         │   │                                   │   │
│  │                                    └────────────────────┘   │                                   │   │
│  │  ┌──────────────┐ ┌────────────────────┐                    │                                   │   │
│  │  │  PRIORITIES  │ │ COMPLIANCE_AREAS   │                    │                                   │   │
│  │  │   (PK: id)   │ │     (PK: id)       │                    │                                   │   │
│  │  └──────────────┘ └────────────────────┘                    │                                   │   │
│  └─────────────────────────────────────────────────────────────┘                                   │   │
│                                                                                                    │   │
│  ┌─────────────┐                                                                                   │   │
│  │ AUDIT_LOGS  │───────────────────────────────────────────────────────────────────────────────────┘   │
│  │  (PK: id)   │                                                                                        │
│  │  FK: user   │                                                                                        │
│  └─────────────┘                                                                                        │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Relationship Summary Table

| Parent Table | Child Table | Relationship | FK Column | Description |
|-------------|-------------|--------------|-----------|-------------|
| `users` | `buildings` | 1:M | `created_by_id` | One user can create many buildings |
| `users` | `audit_logs` | 1:M | `user_id` | One user can have many audit log entries |
| `buildings` | `assessments` | 1:M | `building_id` | One building can have many assessments |
| `buildings` | `compliance_checklists` | 1:M | `building_id` | One building can have many compliance checklists |
| `buildings` | `system_scores` | 1:M | `building_id` | One building has scores for multiple systems |
| `buildings` | `test_register` | 1:M | `building_id` | One building can have many tests |
| `buildings` | `capa_register` | 1:M | `building_id` | One building can have many CAPAs |
| `buildings` | `executive_dashboard_summary` | 1:1 | `building_id` | One building has one executive summary |
| `assessments` | `assessment_items` | 1:M | `assessment_id` | One assessment has many inspection items |
| `systems` | `subsystems` | 1:M | `system_id` | One system has many subsystems |
| `systems` | `assessment_items` | 1:M | `system_id` | Items belong to a system |
| `systems` | `system_scores` | 1:M | `system_id` | Scores per system |
| `systems` | `test_register` | 1:M | `system_id` | Tests belong to a system |
| `systems` | `capa_register` | 1:M | `system_id` | CAPAs belong to a system |
| `subsystems` | `components` | 1:M | `subsystem_id` | One subsystem has many components |
| `subsystems` | `assessment_items` | 1:M | `subsystem_id` | Items belong to a subsystem |
| `components` | `assessment_items` | 1:M | `component_id` | Items belong to a component |
| `compliance_checklists` | `compliance_items` | 1:M | `checklist_id` | One checklist has many items |
| `compliance_areas_lookup` | `compliance_items` | 1:M | `compliance_area_id` | Items categorized by compliance area |
| `responsibilities_lookup` | `assessment_items` | 1:M | `responsibility_id` | Items assigned to responsibilities |
| `responsibilities_lookup` | `capa_register` | 1:M | `responsibility_id` | CAPAs assigned to responsibilities |
| `test_register` | `test_item_links` | 1:M | `test_record_id` | Tests linked to items |
| `assessment_items` | `test_item_links` | 1:M | `assessment_item_id` | Items linked to tests |
| `assessment_items` | `capa_register` | 1:M | `assessment_item_id` | CAPAs linked to items |

---

## 📚 Table Definitions

---

### 1. USERS (`users`)
**Purpose:** User accounts with role-based access control for the application.

| Column | Type | PK | FK | Nullable | Description |
|--------|------|----|----|----------|-------------|
| `id` | INTEGER | ✅ | | NO | Primary key, auto-increment |
| `username` | VARCHAR(80) | | | NO | Unique username for login |
| `email` | VARCHAR(120) | | | NO | Unique email address |
| `password_hash` | VARCHAR(255) | | | NO | Encrypted password (bcrypt) |
| `role` | VARCHAR(50) | | | NO | User role: Admin, ProjectManager, Assessor, Reviewer, Viewer |
| `is_active` | BOOLEAN | | | YES | Account active status (for approval workflow) |
| `created_at` | DATETIME | | | YES | Account creation timestamp |
| `updated_at` | DATETIME | | | YES | Last update timestamp |

**Indexes:** `username` (UNIQUE), `email` (UNIQUE)

---

### 2. AUDIT_LOGS (`audit_logs`)
**Purpose:** Complete audit trail for governance and compliance tracking.

| Column | Type | PK | FK | Nullable | Description |
|--------|------|----|----|----------|-------------|
| `id` | INTEGER | ✅ | | NO | Primary key |
| `user_id` | INTEGER | | ✅ users.id | YES | User who performed the action |
| `table_name` | VARCHAR(50) | | | NO | Name of affected table |
| `record_id` | INTEGER | | | YES | ID of affected record |
| `action` | VARCHAR(20) | | | NO | Action type: CREATE, UPDATE, DELETE |
| `old_values` | JSON | | | YES | Previous values before change |
| `new_values` | JSON | | | YES | New values after change |
| `timestamp` | DATETIME | | | YES | When the action occurred |

**Indexes:** `user_id`, `timestamp`

---

### 3. SYSTEMS (`systems`)
**Purpose:** Master list of 21 building systems for assessment categorization.

| Column | Type | PK | FK | Nullable | Description |
|--------|------|----|----|----------|-------------|
| `id` | INTEGER | ✅ | | NO | Primary key |
| `system_code` | VARCHAR(20) | | | NO | Unique system code (e.g., "SYS-01") |
| `system_name` | VARCHAR(100) | | | NO | System name (e.g., "Fire & Life Safety") |
| `description` | TEXT | | | YES | Detailed description |
| `order` | INTEGER | | | YES | Display order |
| `active` | BOOLEAN | | | YES | Whether system is active |
| `created_at` | DATETIME | | | YES | Creation timestamp |

**Sample Systems:**
- Fire & Life Safety
- HVAC
- Electrical
- Plumbing
- Structural
- Elevators & Escalators
- Building Envelope
- Interior Finishes
- Site & Landscaping

---

### 4. SUBSYSTEMS (`subsystems`)
**Purpose:** Sub-categories under each building system.

| Column | Type | PK | FK | Nullable | Description |
|--------|------|----|----|----------|-------------|
| `id` | INTEGER | ✅ | | NO | Primary key |
| `system_id` | INTEGER | | ✅ systems.id | NO | Parent system |
| `subsystem_code` | VARCHAR(30) | | | NO | Unique subsystem code |
| `subsystem_name` | VARCHAR(100) | | | NO | Subsystem name |
| `description` | TEXT | | | YES | Detailed description |
| `order` | INTEGER | | | YES | Display order |
| `active` | BOOLEAN | | | YES | Whether subsystem is active |

**Example:** For "Fire & Life Safety" system → "Fire Detection", "Fire Suppression", "Emergency Exits"

---

### 5. COMPONENTS (`components`)
**Purpose:** Specific components under each subsystem for detailed inspection.

| Column | Type | PK | FK | Nullable | Description |
|--------|------|----|----|----------|-------------|
| `id` | INTEGER | ✅ | | NO | Primary key |
| `subsystem_id` | INTEGER | | ✅ subsystems.id | NO | Parent subsystem |
| `component_code` | VARCHAR(30) | | | NO | Unique component code |
| `component_name` | VARCHAR(100) | | | NO | Component name |
| `description` | TEXT | | | YES | Detailed description |
| `order` | INTEGER | | | YES | Display order |
| `active` | BOOLEAN | | | YES | Whether component is active |

**Example:** For "Fire Detection" subsystem → "Smoke Detectors", "Heat Detectors", "Fire Alarm Panel"

---

### 6. BUILDINGS (`buildings`)
**Purpose:** Step 1 - Building/Project information header with all property details.

| Column | Type | PK | FK | Nullable | Description |
|--------|------|----|----|----------|-------------|
| `id` | INTEGER | ✅ | | NO | Primary key |
| `project_name` | VARCHAR(200) | | | NO | Project/Building name |
| `building_code` | VARCHAR(50) | | | NO | Unique building identifier |
| `city` | VARCHAR(100) | | | NO | City location |
| `address` | VARCHAR(255) | | | NO | Full address |
| `latitude` | FLOAT | | | YES | GPS latitude coordinate |
| `longitude` | FLOAT | | | YES | GPS longitude coordinate |
| `building_type` | VARCHAR(100) | | | NO | Type: Hospital, Commercial, Residential, etc. |
| `primary_use` | VARCHAR(100) | | | NO | Primary use: Healthcare, Office, Retail, etc. |
| `gross_built_area_m2` | FLOAT | | | NO | Total built area in square meters |
| `number_of_floors` | INTEGER | | | YES | Number of floors |
| `construction_year` | INTEGER | | | YES | Year of construction |
| `last_major_renovation_date` | DATE | | | YES | Last major renovation date |
| `estimated_life_time_years` | INTEGER | | | YES | Estimated total lifespan |
| `planned_asset_retirement_year` | INTEGER | | | YES | Planned retirement year |
| `fm_contractor` | VARCHAR(200) | | | YES | Facilities Management contractor |
| `inspection_date` | DATE | | | NO | Date of inspection |
| `current_year` | INTEGER | | | NO | Current assessment year |
| `system_threshold_percent` | FLOAT | | | YES | Pass/fail threshold (default 75%) |
| `created_by_id` | INTEGER | | ✅ users.id | NO | User who created the building |
| `status` | VARCHAR(20) | | | YES | Status: Draft, InProgress, Complete |
| `created_at` | DATETIME | | | YES | Creation timestamp |
| `updated_at` | DATETIME | | | YES | Last update timestamp |

**Indexes:** `building_code` (UNIQUE)

---

### 7. ASSESSMENTS (`assessments`)
**Purpose:** Step 2 - Assessment session container for a building inspection.

| Column | Type | PK | FK | Nullable | Description |
|--------|------|----|----|----------|-------------|
| `id` | INTEGER | ✅ | | NO | Primary key |
| `building_id` | INTEGER | | ✅ buildings.id | NO | Associated building |
| `assessment_code` | VARCHAR(50) | | | NO | Unique assessment code |
| `status` | VARCHAR(20) | | | YES | Status: Open, In Progress, Closed |
| `notes` | TEXT | | | YES | Assessment notes |
| `created_at` | DATETIME | | | YES | Creation timestamp |
| `updated_at` | DATETIME | | | YES | Last update timestamp |

**Indexes:** `assessment_code` (UNIQUE), `building_id`

---

### 8. ASSESSMENT_ITEMS (`assessment_items`)
**Purpose:** Step 2 - Individual inspection items with ratings and scores.

| Column | Type | PK | FK | Nullable | Description |
|--------|------|----|----|----------|-------------|
| `id` | INTEGER | ✅ | | NO | Primary key |
| `assessment_id` | INTEGER | | ✅ assessments.id | NO | Parent assessment |
| `system_id` | INTEGER | | ✅ systems.id | NO | Building system |
| `subsystem_id` | INTEGER | | ✅ subsystems.id | NO | Subsystem |
| `component_id` | INTEGER | | ✅ components.id | NO | Component |
| `item_code` | VARCHAR(50) | | | NO | Unique item code |
| `inspection_item` | VARCHAR(255) | | | NO | Inspection item description |
| `criteria` | TEXT | | | YES | Acceptance criteria |
| `test_method` | VARCHAR(255) | | | YES | Testing methodology |
| `asset_tag_no` | VARCHAR(100) | | | YES | Asset tag number |
| `snag_location` | VARCHAR(255) | | | YES | Location of snag/issue |
| `snag_evidence_ref` | VARCHAR(100) | | | YES | Evidence reference |
| `snag_evidence_type` | VARCHAR(50) | | | YES | Type of evidence (Photo, Document) |
| `rate` | INTEGER | | | YES | Rating 1-5 (Poor to Excellent) |
| `item_weight` | FLOAT | | | YES | Item weight for scoring |
| `risk_criticality` | INTEGER | | | YES | Risk level 0-5 |
| `responsibility_id` | INTEGER | | ✅ responsibilities_lookup.id | YES | Responsible party |
| `priority` | VARCHAR(20) | | | YES | Priority: P1, P2, P3, P4 |
| `status` | VARCHAR(20) | | | YES | Status: Open, In Progress, Closed, Verified |
| `due_date` | DATE | | | YES | Due date for action |
| `remarks` | TEXT | | | YES | Additional remarks |
| `score` | FLOAT | | | YES | **Calculated:** Rate × 2 × 10 |
| `score_percent` | FLOAT | | | YES | **Calculated:** Score / 100 |
| `weighted_score` | FLOAT | | | YES | **Calculated:** Score% × Weight |
| `evidence_file_path` | VARCHAR(500) | | | YES | Path to evidence file |
| `created_at` | DATETIME | | | YES | Creation timestamp |
| `updated_at` | DATETIME | | | YES | Last update timestamp |

**Score Calculation:**
```
Score = Rate × 2 × 10
Score % = Score / 100
Weighted Score = Score % × Item Weight
```

---

### 9. COMPLIANCE_CHECKLISTS (`compliance_checklist`)
**Purpose:** Step 3 - Government compliance checklist container.

| Column | Type | PK | FK | Nullable | Description |
|--------|------|----|----|----------|-------------|
| `id` | INTEGER | ✅ | | NO | Primary key |
| `building_id` | INTEGER | | ✅ buildings.id | NO | Associated building |
| `checklist_code` | VARCHAR(50) | | | NO | Unique checklist code |
| `status` | VARCHAR(20) | | | YES | Status: Open, In Progress, Complete |
| `created_at` | DATETIME | | | YES | Creation timestamp |
| `updated_at` | DATETIME | | | YES | Last update timestamp |

---

### 10. COMPLIANCE_ITEMS (`compliance_items`)
**Purpose:** Step 3 - Individual compliance requirements.

| Column | Type | PK | FK | Nullable | Description |
|--------|------|----|----|----------|-------------|
| `id` | INTEGER | ✅ | | NO | Primary key |
| `checklist_id` | INTEGER | | ✅ compliance_checklist.id | NO | Parent checklist |
| `compliance_area_id` | INTEGER | | ✅ compliance_areas_lookup.id | NO | Compliance area category |
| `item_code` | VARCHAR(50) | | | NO | Item code |
| `requirement` | TEXT | | | NO | Requirement description |
| `evidence_required` | BOOLEAN | | | YES | Whether evidence is required |
| `status` | VARCHAR(20) | | | YES | Status: Yes, No, Partial, N/A |
| `evidence_ref` | VARCHAR(100) | | | YES | Evidence reference |
| `remarks` | TEXT | | | YES | Remarks |
| `evidence_file_path` | VARCHAR(500) | | | YES | Path to evidence file |
| `created_at` | DATETIME | | | YES | Creation timestamp |
| `updated_at` | DATETIME | | | YES | Last update timestamp |

---

### 11. SYSTEM_SCORES (`system_scores`)
**Purpose:** Step 4 - Aggregated scores per building system.

| Column | Type | PK | FK | Nullable | Description |
|--------|------|----|----|----------|-------------|
| `id` | INTEGER | ✅ | | NO | Primary key |
| `building_id` | INTEGER | | ✅ buildings.id | NO | Associated building |
| `system_id` | INTEGER | | ✅ systems.id | NO | Building system |
| `item_count` | INTEGER | | | YES | Number of items assessed |
| `score_percent` | FLOAT | | | YES | Average score percentage |
| `weight` | FLOAT | | | NO | System weight (user editable) |
| `weighted_score` | FLOAT | | | YES | **Calculated:** Score% × Weight / 100 |
| `created_at` | DATETIME | | | YES | Creation timestamp |
| `updated_at` | DATETIME | | | YES | Last update timestamp |

**Unique Constraint:** `(building_id, system_id)`

---

### 12. TEST_REGISTER (`test_register`)
**Purpose:** Step 5 - Test records with results and evidence.

| Column | Type | PK | FK | Nullable | Description |
|--------|------|----|----|----------|-------------|
| `id` | INTEGER | ✅ | | NO | Primary key |
| `building_id` | INTEGER | | ✅ buildings.id | NO | Associated building |
| `system_id` | INTEGER | | ✅ systems.id | NO | Building system |
| `test_id` | VARCHAR(50) | | | NO | Unique test identifier |
| `test_name` | VARCHAR(200) | | | NO | Test name |
| `standard_reference` | VARCHAR(100) | | | YES | Standard/Code reference (ASHRAE, NFPA) |
| `instrument` | VARCHAR(150) | | | YES | Testing instrument used |
| `locations_sampling` | TEXT | | | YES | Sampling locations |
| `acceptance_criteria` | TEXT | | | YES | Acceptance criteria |
| `readings` | JSON | | | YES | Test readings (structured data) |
| `result` | VARCHAR(50) | | | YES | Result: Pass, Fail, Need Attention |
| `witness` | VARCHAR(100) | | | YES | Witness name |
| `test_date` | DATE | | | NO | Date of test |
| `evidence_ref` | VARCHAR(100) | | | YES | Evidence reference |
| `evidence_file_path` | VARCHAR(500) | | | YES | Path to evidence file |
| `remarks` | TEXT | | | YES | Remarks |
| `created_at` | DATETIME | | | YES | Creation timestamp |
| `updated_at` | DATETIME | | | YES | Last update timestamp |

**Indexes:** `test_id` (UNIQUE), `building_id`

---

### 13. TEST_ITEM_LINKS (`test_item_links`)
**Purpose:** Many-to-Many relationship between tests and assessment items.

| Column | Type | PK | FK | Nullable | Description |
|--------|------|----|----|----------|-------------|
| `id` | INTEGER | ✅ | | NO | Primary key |
| `test_record_id` | INTEGER | | ✅ test_register.id | NO | Test record |
| `assessment_item_id` | INTEGER | | ✅ assessment_items.id | NO | Assessment item |
| `created_at` | DATETIME | | | YES | Link creation timestamp |

---

### 14. CAPA_REGISTER (`capa_register`)
**Purpose:** Step 6 - Corrective and Preventive Actions register.

| Column | Type | PK | FK | Nullable | Description |
|--------|------|----|----|----------|-------------|
| `id` | INTEGER | ✅ | | NO | Primary key |
| `building_id` | INTEGER | | ✅ buildings.id | NO | Associated building |
| `system_id` | INTEGER | | ✅ systems.id | NO | Building system |
| `assessment_item_id` | INTEGER | | ✅ assessment_items.id | YES | Related assessment item |
| `capa_id` | VARCHAR(50) | | | NO | Unique CAPA identifier |
| `priority` | VARCHAR(20) | | | NO | Priority: P1-Critical, P2-High, P3-Medium, P4-Low |
| `finding` | TEXT | | | NO | Finding description |
| `required_action` | TEXT | | | NO | Required corrective action |
| `responsibility_id` | INTEGER | | ✅ responsibilities_lookup.id | YES | Responsible party |
| `due_date` | DATE | | | NO | Action due date |
| `estimated_cost` | FLOAT | | | YES | Estimated cost (SAR) |
| `status` | VARCHAR(20) | | | YES | Status: Open, In Progress, Closed, Verified, Overdue |
| `verification_evidence` | VARCHAR(500) | | | YES | Verification evidence path |
| `verification_date` | DATE | | | YES | Verification date |
| `remarks` | TEXT | | | YES | Remarks |
| `created_at` | DATETIME | | | YES | Creation timestamp |
| `updated_at` | DATETIME | | | YES | Last update timestamp |

**Indexes:** `capa_id` (UNIQUE), `building_id`

**Computed Property:** `is_overdue()` - Returns true if status not Closed/Verified and due_date < today

---

### 15. EXECUTIVE_DASHBOARD_SUMMARY (`executive_dashboard_summary`)
**Purpose:** Step 7 - Pre-computed executive dashboard metrics.

| Column | Type | PK | FK | Nullable | Description |
|--------|------|----|----|----------|-------------|
| `id` | INTEGER | ✅ | | NO | Primary key |
| `building_id` | INTEGER | | ✅ buildings.id | NO | Associated building (UNIQUE) |
| `overall_building_score` | FLOAT | | | YES | Overall building score % |
| `overall_compliance_percent` | FLOAT | | | YES | Overall compliance % |
| `threshold_pass` | BOOLEAN | | | YES | Whether building passes threshold |
| `total_assessment_items` | INTEGER | | | YES | Total items assessed |
| `items_open` | INTEGER | | | YES | Items with Open status |
| `items_in_progress` | INTEGER | | | YES | Items In Progress |
| `items_closed` | INTEGER | | | YES | Items Closed |
| `items_verified` | INTEGER | | | YES | Items Verified |
| `risk_critical` | INTEGER | | | YES | Count of critical risk items |
| `risk_high` | INTEGER | | | YES | Count of high risk items |
| `risk_medium` | INTEGER | | | YES | Count of medium risk items |
| `risk_low` | INTEGER | | | YES | Count of low risk items |
| `risk_acceptable` | INTEGER | | | YES | Count of acceptable risk items |
| `capa_open` | INTEGER | | | YES | Open CAPAs |
| `capa_in_progress` | INTEGER | | | YES | In Progress CAPAs |
| `capa_closed` | INTEGER | | | YES | Closed CAPAs |
| `capa_overdue` | INTEGER | | | YES | Overdue CAPAs |
| `test_pass` | INTEGER | | | YES | Tests passed |
| `test_fail` | INTEGER | | | YES | Tests failed |
| `test_need_attention` | INTEGER | | | YES | Tests needing attention |
| `notes_observations` | TEXT | | | YES | Executive notes |
| `computed_at` | DATETIME | | | YES | Last computation timestamp |

---

## 📘 Lookup Tables

### 16. RATES_LOOKUP (`rates_lookup`)
| Column | Type | PK | Description |
|--------|------|----|----|
| `id` | INTEGER | ✅ | Primary key |
| `rate_value` | INTEGER | | Rating value (1-5) |
| `description` | VARCHAR(100) | | Description (Poor, Below Average, Average, Good, Excellent) |
| `active` | BOOLEAN | | Active flag |

**Values:**
| Rate | Description |
|------|-------------|
| 1 | Poor |
| 2 | Below Average |
| 3 | Average |
| 4 | Good |
| 5 | Excellent |

---

### 17. WEIGHTS_LOOKUP (`weights_lookup`)
| Column | Type | PK | Description |
|--------|------|----|----|
| `id` | INTEGER | ✅ | Primary key |
| `weight_value` | FLOAT | | Weight value |
| `description` | VARCHAR(100) | | Description |
| `active` | BOOLEAN | | Active flag |

**Values:** 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0

---

### 18. RESPONSIBILITIES_LOOKUP (`responsibilities_lookup`)
| Column | Type | PK | Description |
|--------|------|----|----|
| `id` | INTEGER | ✅ | Primary key |
| `name` | VARCHAR(100) | | Responsibility name |
| `description` | VARCHAR(255) | | Description |
| `active` | BOOLEAN | | Active flag |

**Values:** MEP, Main Contractor, FM, Specialist, Client, FM Contractor, Building Owner, Consultant, Assessor, Government Authority

---

### 19. PRIORITIES_LOOKUP (`priorities_lookup`)
| Column | Type | PK | Description |
|--------|------|----|----|
| `id` | INTEGER | ✅ | Primary key |
| `priority_name` | VARCHAR(50) | | Priority name |
| `order` | INTEGER | | Display order |
| `active` | BOOLEAN | | Active flag |

**Values:**
| Priority | Description |
|----------|-------------|
| P1 | Critical - Immediate action |
| P2 | High - Within 7 days |
| P3 | Medium - Within 30 days |
| P4 | Low - Within 90 days |

---

### 20. COMPLIANCE_AREAS_LOOKUP (`compliance_areas_lookup`)
| Column | Type | PK | Description |
|--------|------|----|----|
| `id` | INTEGER | ✅ | Primary key |
| `area_name` | VARCHAR(100) | | Compliance area name |
| `description` | TEXT | | Description |
| `regulation_code` | VARCHAR(50) | | Regulation code |
| `active` | BOOLEAN | | Active flag |

**Sample Areas:**
- Civil Defense Approval (CD-001)
- Municipality License (MUN-001)
- Electricity Company Approval (SEC-001)
- Water Authority Approval (NWC-001)
- Environmental Compliance (ENV-001)

---

## 🔗 Power BI API Endpoints

| Table | API Endpoint |
|-------|--------------|
| Users | `/api/powerbi/users` |
| Systems | `/api/powerbi/systems` |
| Subsystems | `/api/powerbi/subsystems` |
| Components | `/api/powerbi/components` |
| Buildings | `/api/powerbi/buildings` |
| Assessments | `/api/powerbi/assessments` |
| Assessment Items | `/api/powerbi/assessment_items` |
| Compliance Checklists | `/api/powerbi/compliance_checklists` |
| Compliance Items | `/api/powerbi/compliance_items` |
| Compliance Areas | `/api/powerbi/compliance_areas` |
| System Scores | `/api/powerbi/system_scores` |
| Test Registers | `/api/powerbi/test_registers` |
| CAPA Registers | `/api/powerbi/capa_registers` |
| Executive Dashboard | `/api/powerbi/executive_dashboard` |
| Responsibilities | `/api/powerbi/responsibilities` |
| Priorities | `/api/powerbi/priorities` |
| Rates | `/api/powerbi/rates` |
| Weights | `/api/powerbi/weights` |
| Audit Logs | `/api/powerbi/audit_logs` |

**Base URL:** `https://web-production-c26d2.up.railway.app`

---

## 📊 Data Model for Power BI

### Recommended Relationships in Power BI:

```
┌─────────────┐          ┌─────────────────┐          ┌───────────────────┐
│   Systems   │ 1 ────── M │    Subsystems   │ 1 ────── M │    Components     │
└─────────────┘          └─────────────────┘          └───────────────────┘
       │
       │ 1
       │
       M
┌─────────────────┐          ┌─────────────────┐
│  System Scores  │ M ────── 1 │    Buildings    │
└─────────────────┘          └─────────────────┘
                                    │
                                    │ 1
                    ┌───────────────┼───────────────┐
                    M               M               M
            ┌───────────────┐ ┌─────────────┐ ┌─────────────┐
            │  Assessments  │ │ Comp.Lists  │ │    CAPAs    │
            └───────┬───────┘ └──────┬──────┘ └─────────────┘
                    │ 1              │ 1
                    M                M
            ┌───────────────┐ ┌─────────────┐
            │  Assess Items │ │ Comp. Items │
            └───────────────┘ └─────────────┘
```

---

## 📝 Notes

1. **All timestamps** are stored in UTC
2. **Soft deletes** are implemented via `active` boolean flags on lookup tables
3. **Audit logging** captures all CREATE, UPDATE, DELETE operations
4. **Score calculations** are performed server-side when items are saved
5. **CASCADE deletes** are configured on parent-child relationships
6. **Unique constraints** prevent duplicate records where business logic requires

---

*Document generated: January 2026*
*BCAR System v2.0 - Dar Al Riyadh*
