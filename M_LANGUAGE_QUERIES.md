# M Language Queries for Power BI - 3 Tables (API-Based)

Use these M language queries in Power BI's **Power Query Editor** to connect via REST API.

**Base API URL:** `https://web-production-c26d2.up.railway.app/api`

---

## 1. USERS TABLE

```m
let
    Source = Json.Document(
        Web.Contents("https://web-production-c26d2.up.railway.app/api/users")
    ),
    data = Source[data],
    #"Converted to Table" = Table.FromList(data, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Expanded Columns" = Table.ExpandRecordColumn(#"Converted to Table", "Column1", 
        {"id", "email", "full_name", "created_at", "active", "approved_at", "approved_by_id"},
        {"id", "email", "full_name", "created_at", "active", "approved_at", "approved_by_id"}
    ),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded Columns",{
        {"id", Int64.Type},
        {"email", type text},
        {"full_name", type text},
        {"created_at", type datetime},
        {"active", Int64.Type},
        {"approved_at", type datetime},
        {"approved_by_id", Int64.Type}
    })
in
    #"Changed Type"
```

**Columns:**
- `id` (Integer) - Primary Key
- `email` (Text) - User email address
- `full_name` (Text) - User full name
- `created_at` (DateTime) - Account creation date
- `active` (Integer) - 0 = Pending, 1 = Approved
- `approved_at` (DateTime) - Approval date
- `approved_by_id` (Integer) - ID of admin who approved

---

## 2. PROJECT_INSPECTIONS TABLE

```m
let
    Source = Json.Document(
        Web.Contents("https://web-production-c26d2.up.railway.app/api/inspections")
    ),
    DataList = try Source[data] otherwise Source,
    #"Converted to Table" = Table.FromList(DataList, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Expanded Columns" = Table.ExpandRecordColumn(#"Converted to Table", "Column1", 
        {"address", "building_score", "building_type", "chronological_age", "city", "construction_year", 
         "created_at", "current_year", "estimated_effective_age", "estimated_life_time", "estimated_remaining_life", 
         "fire_life_safety", "fm_contractor", "fm_performance", "government_compliance", "gps_latitude", "gps_longitude", 
         "gross_built_area", "high_priority_classified", "id", "inspection_date", "inspection_result", 
         "last_renovation_date", "notes", "number_of_floors", "planned_retirement_year", "primary_use", 
         "project_name", "system_threshold", "total_economic_life", "updated_at", "user_id", "inspection_status", 
         "inspection_by", "reviewed_by"},
        {"address", "building_score", "building_type", "chronological_age", "city", "construction_year", 
         "created_at", "current_year", "estimated_effective_age", "estimated_life_time", "estimated_remaining_life", 
         "fire_life_safety", "fm_contractor", "fm_performance", "government_compliance", "gps_latitude", "gps_longitude", 
         "gross_built_area", "high_priority_classified", "id", "inspection_date", "inspection_result", 
         "last_renovation_date", "notes", "number_of_floors", "planned_retirement_year", "primary_use", 
         "project_name", "system_threshold", "total_economic_life", "updated_at", "user_id", "inspection_status", 
         "inspection_by", "reviewed_by"}
    ),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded Columns",{
        {"id", Int64.Type},
        {"user_id", Int64.Type},
        {"project_name", type text},
        {"city", type text},
        {"address", type text},
        {"gps_latitude", type number},
        {"gps_longitude", type number},
        {"building_type", type text},
        {"primary_use", type text},
        {"gross_built_area", type number},
        {"number_of_floors", Int64.Type},
        {"last_renovation_date", type datetime},
        {"fm_contractor", type text},
        {"current_year", Int64.Type},
        {"construction_year", Int64.Type},
        {"estimated_life_time", Int64.Type},
        {"planned_retirement_year", Int64.Type},
        {"system_threshold", type number},
        {"inspection_date", type datetime},
        {"total_economic_life", Int64.Type},
        {"chronological_age", Int64.Type},
        {"estimated_effective_age", Int64.Type},
        {"estimated_remaining_life", Int64.Type},
        {"inspection_result", type text},
        {"building_score", type number},
        {"high_priority_classified", Int64.Type},
        {"fm_performance", type number},
        {"government_compliance", type text},
        {"fire_life_safety", type number},
        {"notes", type text},
        {"inspection_status", type text},
        {"inspection_by", type text},
        {"reviewed_by", type text},
        {"created_at", type datetime},
        {"updated_at", type datetime}
    })
in
    #"Changed Type"
```

**Key Columns (33 fields total):**
- **IDs:** `id`, `user_id`
- **Project Info:** `project_name`, `city`, `address`, `gps_latitude`, `gps_longitude`
- **Building Details:** `building_type`, `primary_use`, `gross_built_area`, `number_of_floors`
- **Timeline:** `construction_year`, `current_year`, `last_renovation_date`, `planned_retirement_year`
- **Life/Age:** `total_economic_life`, `chronological_age`, `estimated_effective_age`, `estimated_remaining_life`
- **Assessment:** `inspection_result`, `building_score`, `fm_performance`, `government_compliance`, `fire_life_safety`
- **Status:** `inspection_status`, `high_priority_classified`
- **Audit:** `inspection_by`, `reviewed_by`, `created_at`, `updated_at`

---

## 3. INSPECTION_SYSTEMS TABLE

```m
let
    Source = Json.Document(
        Web.Contents("https://web-production-c26d2.up.railway.app/api/systems")
    ),
    data = Source[data],
    #"Converted to Table" = Table.FromList(data, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Expanded Columns" = Table.ExpandRecordColumn(#"Converted to Table", "Column1", 
        {"id", "project_inspection_id", "system_name", "item_count", "score_percentage", "weight", "weighted_score", "status", "created_at", "updated_at"},
        {"id", "project_inspection_id", "system_name", "item_count", "score_percentage", "weight", "weighted_score", "status", "created_at", "updated_at"}
    ),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded Columns",{
        {"id", Int64.Type},
        {"project_inspection_id", Int64.Type},
        {"system_name", type text},
        {"item_count", Int64.Type},
        {"score_percentage", type number},
        {"weight", type number},
        {"weighted_score", type number},
        {"status", type text},
        {"created_at", type datetime},
        {"updated_at", type datetime}
    })
in
    #"Changed Type"
```

**Columns (10 fields):**
- `id` (Integer) - Primary Key
- `project_inspection_id` (Integer) - Foreign Key to project_inspections
- `system_name` (Text) - System name (21 types available)
- `item_count` (Integer) - Number of items inspected
- `score_percentage` (Number) - Score 0-100 (e.g., 54, 73, 78)
- `weight` (Number) - System weight (e.g., 17.00, 10.00)
- `weighted_score` (Number) - Calculated weighted score
- `status` (Text) - Critical, Warning, Good
- `created_at` (DateTime) - Creation timestamp
- `updated_at` (DateTime) - Last update timestamp

**21 Building Systems:**
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
12. Structural
13. Architectural_Fabric
14. External_Parking
15. Landscape
16. Pools_WaterFeatures
17. Waste_Management
18. Sustainability
19. Compliance_Documentation
20. FM_Performance
21. Governance_Readiness

---

## COMBINED QUERY (All 3 Tables with Relationships)

```m
let
    // Users Table
    UsersSource = Json.Document(Web.Contents("https://web-production-c26d2.up.railway.app/api/users")),
    UsersTable = Table.FromList(UsersSource, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    UsersExpanded = Table.ExpandRecordColumn(UsersTable, "Column1", 
        {"id", "email", "full_name", "created_at", "active"},
        {"id", "email", "full_name", "created_at", "active"}
    ),
    
    // ProjectInspections Table
    InspectionsSource = Json.Document(Web.Contents("https://web-production-c26d2.up.railway.app/api/inspections")),
    InspectionsTable = Table.FromList(InspectionsSource, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    InspectionsExpanded = Table.ExpandRecordColumn(InspectionsTable, "Column1", 
        {"id", "user_id", "project_name", "building_score", "inspection_date", "created_at"},
        {"id", "user_id", "project_name", "building_score", "inspection_date", "created_at"}
    ),
    
    // InspectionSystems Table
    SystemsSource = Json.Document(Web.Contents("https://web-production-c26d2.up.railway.app/api/systems")),
    SystemsData = SystemsSource[data],
    SystemsTable = Table.FromList(SystemsData, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    SystemsExpanded = Table.ExpandRecordColumn(SystemsTable, "Column1", 
        {"id", "project_inspection_id", "system_name", "score_percentage", "weight", "weighted_score"},
        {"id", "project_inspection_id", "system_name", "score_percentage", "weight", "weighted_score"}
    )
in
    {UsersExpanded, InspectionsExpanded, SystemsExpanded}
```

---

## HOW TO USE IN POWER BI

### Direct API Connection (Recommended)
1. Open **Power BI Desktop**
2. Go to **Home** → **Get Data** → **Web**
3. Enter URL: `https://web-production-c26d2.up.railway.app/api/inspections`
4. Click **Load**
5. In Power Query Editor, click **Advanced Editor**
6. Replace the query with one of the M queries above
7. Click **Done** and **Load**

### Step-by-Step for Each Table

**For PROJECT_INSPECTIONS:**
1. Copy the **PROJECT_INSPECTIONS TABLE** query
2. **Home** → **Get Data** → **Web**
3. Enter: `https://web-production-c26d2.up.railway.app/api/inspections`
4. Click **Advanced Editor** and paste the query
5. Click **Done**

**For INSPECTION_SYSTEMS:**
1. Copy the **INSPECTION_SYSTEMS TABLE** query
2. **Home** → **Get Data** → **Web**
3. Enter: `https://web-production-c26d2.up.railway.app/api/systems`
4. Click **Advanced Editor** and paste the query
5. Click **Done**

**For USERS:**
1. Copy the **USERS TABLE** query
2. **Home** → **Get Data** → **Web**
3. Enter: `https://web-production-c26d2.up.railway.app/api/users`
4. Click **Advanced Editor** and paste the query
5. Click **Done**

---

## RELATIONSHIPS TO SET IN POWER BI

After loading the tables, create these relationships:

1. **Users → ProjectInspections**
   - From: `users[id]`
   - To: `project_inspections[user_id]`
   - Cardinality: One-to-Many (1:*)

2. **ProjectInspections → InspectionSystems**
   - From: `project_inspections[id]`
   - To: `inspection_systems[project_inspection_id]`
   - Cardinality: One-to-Many (1:*)

---

## SAMPLE POWER QUERY FOR SUMMARY REPORT

```m
let
    // Load inspections
    InspectionsSource = Json.Document(
        Web.Contents("https://web-production-c26d2.up.railway.app/api/inspections")
    ),
    InspectionsTable = Table.FromList(InspectionsSource, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    InspectionsExpanded = Table.ExpandRecordColumn(InspectionsTable, "Column1", 
        {"id", "project_name", "building_score", "building_type", "city", "inspection_date"},
        {"id", "project_name", "building_score", "building_type", "city", "inspection_date"}
    ),
    
    // Load systems
    SystemsSource = Json.Document(
        Web.Contents("https://web-production-c26d2.up.railway.app/api/systems")
    ),
    SystemsData = SystemsSource[data],
    SystemsTable = Table.FromList(SystemsData, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    SystemsExpanded = Table.ExpandRecordColumn(SystemsTable, "Column1", 
        {"project_inspection_id", "system_name", "score_percentage", "weight", "weighted_score"},
        {"project_inspection_id", "system_name", "score_percentage", "weight", "weighted_score"}
    ),
    
    // Merge tables
    Merged = Table.NestedJoin(
        InspectionsExpanded,
        {"id"},
        SystemsExpanded,
        {"project_inspection_id"},
        "Systems",
        JoinKind.LeftOuter
    ),
    
    // Expand systems columns
    Expanded = Table.ExpandTableColumn(Merged, "Systems",
        {"system_name", "score_percentage", "weight", "weighted_score"},
        {"SystemName", "SystemScore", "SystemWeight", "WeightedScore"}
    )
in
    Expanded
```

---

## CONNECTION PARAMETERS

**API Base URLs:**
- Users: `https://web-production-c26d2.up.railway.app/api/users`
- Project Inspections: `https://web-production-c26d2.up.railway.app/api/inspections`
- Inspection Systems: `https://web-production-c26d2.up.railway.app/api/systems`

**Database Connection (Direct SQL - PostgreSQL):**
```
Server: interchange.proxy.rlwy.net
Port: 30821
Database: railway
User: postgres
Password: eqPAxKlJkmkfsZahQcoazkamJfBgtxhB
```

⚠️ **Note:** Do NOT use SQL Server connection type for PostgreSQL. Use the API queries instead.

---

## TIPS

✅ Load tables separately first, then create relationships in Power BI  
✅ Use the `created_at` and `updated_at` fields for trend analysis  
✅ Build calculated columns from `building_score` and `weighted_score`  
✅ Create slicers for `system_name` to filter by building system  
✅ Use `inspection_status` to show only completed inspections  
✅ Combine `chronological_age` and `estimated_remaining_life` for lifecycle analysis
