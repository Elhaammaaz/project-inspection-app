# 🗂️ DATABASE TABLES - QUICK REFERENCE

## 📍 WHERE IS YOUR DATABASE?

**Hosting:** Railway PostgreSQL  
**Location:** `host.railway.internal:5432`  
**Database Name:** `railway`  
**Connection:** Secure (SSL required)

---

## 📋 YOUR DATABASE TABLES

### **TABLE 1: `users`**
```
┌─────────────────────────────────┐
│ USERS TABLE                     │
├─────────────────────────────────┤
│ id                  (Integer)   │ Primary Key
│ email               (String)    │ Unique, indexed
│ password_hash       (String)    │ Encrypted
│ created_at          (DateTime)  │ Timestamp
└─────────────────────────────────┘

Row Count: 1 (demo user)
```

**Sample Data:**
```
id | email                | created_at
---|----------------------|--------------------
1  | demo@example.com     | 2025-12-31 10:00:00
```

---

### **TABLE 2: `project_inspections`** ⭐ MAIN TABLE
```
┌───────────────────────────────────────────────────────────────────┐
│ PROJECT_INSPECTIONS TABLE (Your Main Data)                        │
├───────────────────────────────────────────────────────────────────┤
│
│ IDENTIFIERS
│ ├─ id                          (Integer)  Primary Key
│ ├─ user_id                     (Integer)  Links to users table
│ │
│ PROJECT INFORMATION
│ ├─ project_name                (String)   📍 Building/Project name
│ ├─ city                        (String)   📍 City location
│ ├─ address                     (String)   📍 Full address
│ ├─ gps_latitude                (Float)    📍 Latitude
│ ├─ gps_longitude               (Float)    📍 Longitude
│ │
│ BUILDING DETAILS
│ ├─ building_type               (String)   e.g., "Residential"
│ ├─ primary_use                 (String)   e.g., "Office"
│ ├─ gross_built_area            (Float)    Area in m²
│ ├─ number_of_floors            (Integer)  
│ │
│ DATES & TIMELINE
│ ├─ construction_year           (Integer)  
│ ├─ last_renovation_date        (Date)     
│ ├─ inspection_date             (Date)     📌 Key for trending
│ ├─ current_year                (Integer)  
│ ├─ estimated_life_time         (Integer)  Years
│ ├─ planned_retirement_year     (Integer)  
│ │
│ ASSESSMENT RESULTS ⭐ BEST FOR CHARTS
│ ├─ inspection_result           (String)   "Passed", "Not Complied", etc.
│ ├─ building_score              (Float)    0-100 (KPI METRIC!)
│ ├─ fm_performance              (Float)    Performance % (KPI!)
│ ├─ government_compliance       (String)   "Complied", "Not Complied"
│ ├─ high_priority_classified    (Integer)  Count of high priority items
│ │
│ SAFETY METRICS ⭐ BEST FOR DASHBOARDS
│ ├─ fire_life_safety            (Float)    % (KPI!)
│ ├─ total_economic_life         (Integer)  Years
│ ├─ chronological_age           (Integer)  Years
│ ├─ estimated_effective_age     (Integer)  Years
│ ├─ estimated_remaining_life    (Integer)  Years
│ │
│ OTHER
│ ├─ fm_contractor               (String)   Contractor name
│ ├─ system_threshold            (Float)    %
│ ├─ notes                       (Text)     Free text
│ ├─ systems_data                (JSON)     Complex data
│ ├─ created_at                  (DateTime) When created
│ ├─ updated_at                  (DateTime) Last updated
│
└───────────────────────────────────────────────────────────────────┘

Rows: Will grow as you add inspections
Indexes: id, user_id, created_at (for faster queries)
```

---

## 🎯 KEY COLUMNS FOR POWER BI VISUALIZATIONS

### **FOR DASHBOARDS:**
- ✅ `project_name` - Display in tables
- ✅ `building_score` - KPI gauge/card
- ✅ `building_type` - Category filter
- ✅ `city` - Map visualization
- ✅ `inspection_date` - Timeline slicer
- ✅ `government_compliance` - Pie/donut chart
- ✅ `fire_life_safety` - Trend line
- ✅ `inspection_result` - Status indicator

### **FOR ANALYSIS:**
- `gross_built_area` - Size analysis
- `number_of_floors` - Building complexity
- `high_priority_classified` - Risk assessment
- `fm_performance` - Performance metrics
- `estimated_remaining_life` - Planning

---

## 🔗 RELATIONSHIP

```
users (1) ─── (Many) project_inspections
  ↓                        ↓
  id  ←─────── user_id  (Foreign Key)
```

**Meaning:** One user can have many project inspections

---

## 📊 SAMPLE POWER BI VISUALS YOU CAN CREATE

| Visual | Based On | Column(s) |
|--------|----------|-----------|
| **KPI Card** | Building Score | `building_score` |
| **Gauge** | Fire Safety % | `fire_life_safety` |
| **Pie Chart** | Compliance Status | `government_compliance` |
| **Bar Chart** | Buildings by Type | `building_type` |
| **Line Chart** | Score Trend | `inspection_date`, `building_score` |
| **Map** | Projects Location | `gps_latitude`, `gps_longitude`, `city` |
| **Table** | All Inspections | All columns |
| **Clustered Bar** | City Comparison | `city`, `avg(building_score)` |
| **Donut Chart** | Inspection Results | `inspection_result` |
| **Scatter** | Area vs Score | `gross_built_area`, `building_score` |

---

## 🚀 HOW TO ACCESS IN POWER BI

### **Step 1: Get Connection Details from Railway**
1. Go to Railway dashboard
2. PostgreSQL service → Connect tab
3. Copy the connection string

### **Step 2: Connect Power BI**
1. Power BI Desktop → Get Data
2. PostgreSQL
3. Host: `host.railway.internal`
4. Database: `railway`
5. Username & Password from Railway

### **Step 3: Load Tables**
- ✅ Select `users`
- ✅ Select `project_inspections` (THIS IS YOUR MAIN TABLE!)

### **Step 4: Create Visualizations**
- Drag columns to the visualization area
- Create filters, slicers, and KPIs

---

## 💡 RECOMMENDED STARTING QUERIES

### **Query 1: Get All Data**
```sql
SELECT * FROM project_inspections
ORDER BY inspection_date DESC;
```

### **Query 2: Summary by City**
```sql
SELECT 
    city,
    COUNT(*) as total,
    AVG(building_score) as avg_score,
    AVG(fire_life_safety) as avg_fire_safety
FROM project_inspections
GROUP BY city;
```

### **Query 3: Compliance Overview**
```sql
SELECT 
    government_compliance,
    COUNT(*) as count,
    AVG(building_score) as avg_score
FROM project_inspections
GROUP BY government_compliance;
```

### **Query 4: High Priority Issues**
```sql
SELECT 
    project_name,
    city,
    high_priority_classified,
    inspection_result
FROM project_inspections
WHERE high_priority_classified > 0
ORDER BY high_priority_classified DESC;
```

---

## ✅ READY TO GO!

**Your database is on Railway with 2 tables:**
- `users` → User authentication data
- `project_inspections` → All your inspection data

**Connect Power BI using the guide above and start building dashboards!** 📊
