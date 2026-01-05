// ============================================================================
// POWER BI M LANGUAGE QUERIES - ALL TABLES
// Building Assessment Report System
// API Base URL: https://web-production-c26d2.up.railway.app
// ============================================================================

// ============================================================================
// TEMPLATE QUERY - Use this as a base for any table
// ============================================================================

/*
let
    Source = Json.Document(Web.Contents("https://web-production-c26d2.up.railway.app/api/[ENDPOINT]")),
    DataList = try Source[data] otherwise Source,
    #"Converted to Table" = Table.FromList(DataList, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Expanded Columns" = Table.ExpandRecordColumn(#"Converted to Table", "Column1", [FIELD_LIST], [FIELD_LIST]),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded Columns", [TYPE_DEFINITIONS])
in
    #"Changed Type"
*/

// ============================================================================
// 1. INSPECTIONS TABLE
// ============================================================================

let
    Source = Json.Document(
        Web.Contents("https://web-production-c26d2.up.railway.app/api/inspections")
    ),
    DataList = try Source[data] otherwise Source,
    #"Converted to Table" = Table.FromList(DataList, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Expanded Columns" = Table.ExpandRecordColumn(#"Converted to Table", "Column1", 
        {"id", "user_id", "project_name", "city", "address", "gps_latitude", "gps_longitude", "building_type", 
         "primary_use", "gross_built_area", "number_of_floors", "last_renovation_date", "fm_contractor", 
         "current_year", "construction_year", "estimated_life_time", "planned_retirement_year", "system_threshold", 
         "inspection_date", "total_economic_life", "chronological_age", "estimated_effective_age", 
         "estimated_remaining_life", "inspection_result", "building_score", "high_priority_classified", 
         "fm_performance", "government_compliance", "fire_life_safety", "notes", "inspection_status", 
         "inspection_by", "reviewed_by", "created_at", "updated_at"},
        {"id", "user_id", "project_name", "city", "address", "gps_latitude", "gps_longitude", "building_type", 
         "primary_use", "gross_built_area", "number_of_floors", "last_renovation_date", "fm_contractor", 
         "current_year", "construction_year", "estimated_life_time", "planned_retirement_year", "system_threshold", 
         "inspection_date", "total_economic_life", "chronological_age", "estimated_effective_age", 
         "estimated_remaining_life", "inspection_result", "building_score", "high_priority_classified", 
         "fm_performance", "government_compliance", "fire_life_safety", "notes", "inspection_status", 
         "inspection_by", "reviewed_by", "created_at", "updated_at"}
    ),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded Columns", {
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
        {"reviewed_at", type text},
        {"created_at", type datetime},
        {"updated_at", type datetime}
    })
in
    #"Changed Type"


// ============================================================================
// 2. USERS TABLE
// ============================================================================

let
    Source = Json.Document(
        Web.Contents("https://web-production-c26d2.up.railway.app/api/users")
    ),
    DataList = try Source[data] otherwise Source,
    #"Converted to Table" = Table.FromList(DataList, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Expanded Columns" = Table.ExpandRecordColumn(#"Converted to Table", "Column1",
        {"id", "email", "full_name", "active", "can_view_dashboard", "can_view_reports", "can_export_data", 
         "can_manage_users", "dashboard_approved_date", "reports_approved_date", "export_approved_date", 
         "created_at", "approved_at"},
        {"id", "email", "full_name", "active", "can_view_dashboard", "can_view_reports", "can_export_data", 
         "can_manage_users", "dashboard_approved_date", "reports_approved_date", "export_approved_date", 
         "created_at", "approved_at"}
    ),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded Columns", {
        {"id", Int64.Type},
        {"email", type text},
        {"full_name", type text},
        {"active", Int64.Type},
        {"can_view_dashboard", Int64.Type},
        {"can_view_reports", Int64.Type},
        {"can_export_data", Int64.Type},
        {"can_manage_users", Int64.Type},
        {"dashboard_approved_date", type datetime},
        {"reports_approved_date", type datetime},
        {"export_approved_date", type datetime},
        {"created_at", type datetime},
        {"approved_at", type datetime}
    })
in
    #"Changed Type"


// ============================================================================
// 3. USER PROFILES TABLE
// ============================================================================

let
    Source = Json.Document(
        Web.Contents("https://web-production-c26d2.up.railway.app/api/user-profiles")
    ),
    DataList = try Source[data] otherwise Source,
    #"Converted to Table" = Table.FromList(DataList, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Expanded Columns" = Table.ExpandRecordColumn(#"Converted to Table", "Column1",
        {"id", "user_id", "department", "job_title", "phone", "office_location", "role", 
         "can_view_dashboard", "can_view_reports", "dashboard_access_approved_at", 
         "theme", "notifications_enabled", "created_at", "updated_at"},
        {"id", "user_id", "department", "job_title", "phone", "office_location", "role", 
         "can_view_dashboard", "can_view_reports", "dashboard_access_approved_at", 
         "theme", "notifications_enabled", "created_at", "updated_at"}
    ),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded Columns", {
        {"id", Int64.Type},
        {"user_id", Int64.Type},
        {"department", type text},
        {"job_title", type text},
        {"phone", type text},
        {"office_location", type text},
        {"role", type text},
        {"can_view_dashboard", Int64.Type},
        {"can_view_reports", Int64.Type},
        {"dashboard_access_approved_at", type datetime},
        {"theme", type text},
        {"notifications_enabled", Int64.Type},
        {"created_at", type datetime},
        {"updated_at", type datetime}
    })
in
    #"Changed Type"


// ============================================================================
// 4. INSPECTION SYSTEMS TABLE
// ============================================================================

let
    Source = Json.Document(
        Web.Contents("https://web-production-c26d2.up.railway.app/api/inspection-systems")
    ),
    DataList = try Source[data] otherwise Source,
    #"Converted to Table" = Table.FromList(DataList, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Expanded Columns" = Table.ExpandRecordColumn(#"Converted to Table", "Column1",
        {"id", "inspection_id", "system_name", "component_name", "condition_rating", "age", "material", 
         "estimated_remaining_life", "planned_replacement_date", "maintenance_notes", "priority", "created_at", "updated_at"},
        {"id", "inspection_id", "system_name", "component_name", "condition_rating", "age", "material", 
         "estimated_remaining_life", "planned_replacement_date", "maintenance_notes", "priority", "created_at", "updated_at"}
    ),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded Columns", {
        {"id", Int64.Type},
        {"inspection_id", Int64.Type},
        {"system_name", type text},
        {"component_name", type text},
        {"condition_rating", type text},
        {"age", Int64.Type},
        {"material", type text},
        {"estimated_remaining_life", Int64.Type},
        {"planned_replacement_date", type datetime},
        {"maintenance_notes", type text},
        {"priority", type text},
        {"created_at", type datetime},
        {"updated_at", type datetime}
    })
in
    #"Changed Type"


// ============================================================================
// 5. DASHBOARD ACCESS REQUESTS TABLE
// ============================================================================

let
    Source = Json.Document(
        Web.Contents("https://web-production-c26d2.up.railway.app/api/dashboard-access-requests")
    ),
    DataList = try Source[data] otherwise Source,
    #"Converted to Table" = Table.FromList(DataList, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Expanded Columns" = Table.ExpandRecordColumn(#"Converted to Table", "Column1",
        {"id", "user_id", "status", "requested_at", "approved_at", "approved_by_id", "rejection_reason", "created_at"},
        {"id", "user_id", "status", "requested_at", "approved_at", "approved_by_id", "rejection_reason", "created_at"}
    ),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded Columns", {
        {"id", Int64.Type},
        {"user_id", Int64.Type},
        {"status", type text},
        {"requested_at", type datetime},
        {"approved_at", type datetime},
        {"approved_by_id", Int64.Type},
        {"rejection_reason", type text},
        {"created_at", type datetime}
    })
in
    #"Changed Type"


// ============================================================================
// 6. PROFILE CHANGE REQUESTS TABLE
// ============================================================================

let
    Source = Json.Document(
        Web.Contents("https://web-production-c26d2.up.railway.app/api/profile-change-requests")
    ),
    DataList = try Source[data] otherwise Source,
    #"Converted to Table" = Table.FromList(DataList, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Expanded Columns" = Table.ExpandRecordColumn(#"Converted to Table", "Column1",
        {"id", "user_id", "field_name", "old_value", "new_value", "status", "requested_at", 
         "approved_at", "approved_by_id", "rejection_reason", "created_at"},
        {"id", "user_id", "field_name", "old_value", "new_value", "status", "requested_at", 
         "approved_at", "approved_by_id", "rejection_reason", "created_at"}
    ),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded Columns", {
        {"id", Int64.Type},
        {"user_id", Int64.Type},
        {"field_name", type text},
        {"old_value", type text},
        {"new_value", type text},
        {"status", type text},
        {"requested_at", type datetime},
        {"approved_at", type datetime},
        {"approved_by_id", Int64.Type},
        {"rejection_reason", type text},
        {"created_at", type datetime}
    })
in
    #"Changed Type"


// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

// SafeGetData - Handles missing fields gracefully
(data as record, field as text, defaultValue as any) =>
    try
        if Record.HasFields(data, field) then
            Record.Field(data, field)
        else
            defaultValue
    otherwise
        defaultValue


// GetDateOrNull - Converts text to datetime or returns null
(dateText as text) =>
    try
        if dateText = null or dateText = "" then
            null
        else
            DateTime.FromText(dateText)
    otherwise
        null


// ============================================================================
// NOTES FOR POWER BI USERS
// ============================================================================

/*
HOW TO USE THESE QUERIES:

1. In Power BI Desktop, go to: Get Data > Web > Web (recommended)

2. Enter the API endpoint URL:
   - Inspections: https://web-production-c26d2.up.railway.app/api/inspections
   - Users: https://web-production-c26d2.up.railway.app/api/users
   - User Profiles: https://web-production-c26d2.up.railway.app/api/user-profiles
   - Inspection Systems: https://web-production-c26d2.up.railway.app/api/inspection-systems
   - Dashboard Requests: https://web-production-c26d2.up.railway.app/api/dashboard-access-requests
   - Profile Changes: https://web-production-c26d2.up.railway.app/api/profile-change-requests

3. Click OK, then when prompted, go to Advanced Editor

4. Copy and paste the corresponding query from this file

5. Click Done and let Power BI load the data

6. Create relationships between tables:
   - Inspections.user_id → Users.id
   - Inspections.id → InspectionSystems.inspection_id
   - Users.id → UserProfiles.user_id
   - DashboardAccessRequests.user_id → Users.id
   - ProfileChangeRequests.user_id → Users.id

DATA TYPES:
- Int64.Type: For IDs and whole numbers (age, number_of_floors, etc.)
- type text: For names, descriptions, text fields
- type number: For decimals (coordinates, building_score, etc.)
- type datetime: For timestamps (created_at, updated_at, etc.)

FILTERING:
All queries include a try/otherwise block to handle API responses with or without a "data" wrapper.
If your API returns data directly as array, the query will still work.

REFRESH SCHEDULE:
Recommended: Every hour or daily depending on update frequency
Go to: Power Query Editor > Refresh > Set Refresh Schedule

TROUBLESHOOTING:
- If columns are missing: Check the API response structure
- If data types are wrong: Update the type definition section
- If connection fails: Check firewall/VPN and API availability
- If slow: Consider adding filters or pagination parameters to the URL
*/
