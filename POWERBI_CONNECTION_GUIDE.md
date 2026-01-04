# 📊 Power BI - PostgreSQL Connection Guide

**Database Location:** Railway PostgreSQL  
**Status:** Ready to Connect

---

## 📍 DATABASE LOCATION & CREDENTIALS

### **Step 1: Get Database Connection Details from Railway**

1. Go to: https://railway.app/dashboard
2. Select your project
3. Click **PostgreSQL** service
4. Go to **Connect** tab
5. Copy the connection string that looks like:
   ```
   postgresql://username:password@host.railway.internal:5432/railway
   ```

### **Extract Connection Details:**
From the URL above, you need:

| Component | Extract From URL | Example |
|-----------|------------------|---------|
| **Host** | `host.railway.internal` | `postgres-prod.railway.internal` |
| **Port** | After `:` before `/` | `5432` |
| **Database** | After last `/` | `railway` |
| **Username** | Before `:` at start | `postgres` |
| **Password** | Between `:` and `@` | `abc123xyz` |

---

## 📊 DATABASE TABLES

Your database has **2 main tables**:

### **Table 1: `users`**
Stores login information

| Column | Type | Purpose |
|--------|------|---------|
| `id` | Integer | User ID (Primary Key) |
| `email` | String(120) | User email (Unique) |
| `password_hash` | String(255) | Encrypted password |
| `created_at` | DateTime | When user created |

**Sample Query:**
```sql
SELECT id, email, created_at FROM users;
```

---

### **Table 2: `project_inspections`**
Stores all project inspection data

| Column | Type | Purpose |
|--------|------|---------|
| `id` | Integer | Inspection ID (Primary Key) |
| `user_id` | Integer | Link to users table |
| **Project Info** | | |
| `project_name` | String | Building/Project name |
| `city` | String | City location |
| `address` | String | Full address |
| `gps_latitude` | Float | Latitude coordinate |
| `gps_longitude` | Float | Longitude coordinate |
| **Building Details** | | |
| `building_type` | String | e.g., "Residential", "Commercial" |
| `primary_use` | String | e.g., "Office", "Warehouse" |
| `gross_built_area` | Float | Area in m² |
| `number_of_floors` | Integer | Number of floors |
| **Dates** | | |
| `construction_year` | Integer | Year built |
| `last_renovation_date` | Date | Last renovation |
| `inspection_date` | Date | Inspection date |
| `current_year` | Integer | Current year |
| `estimated_life_time` | Integer | Expected lifespan (years) |
| `planned_retirement_year` | Integer | Planned retirement |
| **Assessment** | | |
| `inspection_result` | String | "Passed", "Not Complied", etc. |
| `building_score` | Float | 0-100 score |
| `fm_performance` | Float | Performance % |
| `government_compliance` | String | "Complied", "Not Complied" |
| `high_priority_classified` | Integer | Number of high priority items |
| **Safety & Life** | | |
| `fire_life_safety` | Float | Fire safety % |
| `total_economic_life` | Integer | Total economic life (years) |
| `chronological_age` | Integer | Actual age (years) |
| `estimated_effective_age` | Integer | Effective age (years) |
| `estimated_remaining_life` | Integer | Remaining life (years) |
| `system_threshold` | Float | System threshold % |
| **Other** | | |
| `fm_contractor` | String | Contractor name |
| `notes` | Text | Additional notes |
| `systems_data` | JSON | Systems performance data |
| `created_at` | DateTime | When created |
| `updated_at` | DateTime | Last updated |

---

## 🔗 CONNECT POWER BI TO POSTGRESQL

### **Method 1: Using Power BI Desktop (Recommended)**

#### **Step 1: Open Power BI Desktop**
1. Launch **Power BI Desktop**
2. Click **Get Data** (Home tab)
3. Search for **PostgreSQL** (or Database)
4. Select **PostgreSQL database**
5. Click **Connect**

#### **Step 2: Enter Connection Details**
Fill in the connection dialog:

| Field | Value |
|-------|-------|
| **Server** | `host.railway.internal` (from Railway) |
| **Database** | `railway` (from Railway) |
| **Data Connectivity Mode** | Keep as default |

Click **OK** → Then enter username and password

#### **Step 3: Authentication**
When prompted:
- **Username:** `postgres` (from Railway)
- **Password:** Your database password (from Railway)
- Click **Connect**

#### **Step 4: Select Tables**
- ☑️ Check `users` (for user data)
- ☑️ Check `project_inspections` (main data - THIS IS YOUR KEY TABLE!)
- Click **Load**

#### **Step 5: Create Relationships**
Power BI may ask to create relationships:
- **Link:** `project_inspections.user_id` → `users.id`
- Click **Create relationships**

---

### **Method 2: Using Power BI Service (Online)**

1. Go to https://powerbi.microsoft.com
2. Click **Datasets**
3. Click **New Dataset**
4. Select **PostgreSQL**
5. Enter same connection details above
6. Create scheduled refresh in settings

---

## 🚀 SAMPLE POWER BI QUERIES

Once connected, you can create visualizations with queries like:

### **Query 1: All Project Inspections**
```sql
SELECT 
    project_name,
    city,
    building_type,
    building_score,
    inspection_result,
    inspection_date
FROM project_inspections
ORDER BY created_at DESC;
```

### **Query 2: Compliance Overview**
```sql
SELECT 
    government_compliance,
    COUNT(*) as count,
    AVG(building_score) as avg_score
FROM project_inspections
GROUP BY government_compliance;
```

### **Query 3: By Building Type**
```sql
SELECT 
    building_type,
    COUNT(*) as total_inspections,
    AVG(building_score) as avg_score,
    AVG(fire_life_safety) as avg_fire_safety
FROM project_inspections
GROUP BY building_type;
```

### **Query 4: High Priority Items**
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

## 🔐 SECURITY NOTES

✅ **SSL Required:** Railway uses SSL  
✅ **Encrypted Connection:** Data in transit is encrypted  
⚠️ **Keep Credentials Safe:** Don't share database password  
✅ **IP Whitelisting:** Railway handles this automatically

---

## ⚠️ TROUBLESHOOTING

### **Connection Failed**
**Solution:**
1. Verify host is: `host.railway.internal` (NOT localhost)
2. Verify port is: `5432`
3. Check credentials in Railway dashboard again
4. Ensure PostgreSQL service is running in Railway

### **Tables Not Visible**
**Solution:**
1. Tables are in `public` schema (default)
2. Click "Load More" in Power BI navigator
3. Refresh connection

### **Slow Connection**
**Solution:**
1. Check Railway PostgreSQL status (not restarting)
2. Use specific columns instead of SELECT *
3. Add filters to reduce data

---

## 📈 RECOMMENDED VISUALIZATIONS

Once data is loaded in Power BI:

1. **Building Score Distribution** → Column Chart
2. **Compliance Status** → Pie Chart (government_compliance)
3. **Projects by City** → Map visualization
4. **Building Type Analysis** → Clustered bar chart
5. **Inspection Results Trend** → Line chart (by inspection_date)
6. **High Priority Items** → Gauge chart
7. **FM Performance** → Scatter plot
8. **Fire & Safety Rating** → Heatmap

---

## 🔄 AUTO-REFRESH DATA

In Power BI Desktop:
1. File → Options and settings → Data source settings
2. Select your PostgreSQL connection
3. Click "Edit Permissions"
4. Enable **Scheduled Refresh** (if using Power BI Service)
5. Set refresh frequency (e.g., daily, hourly)

---

## 💡 TIPS

✅ Use **Direct Query** for real-time data  
✅ Use **Import** for faster dashboards (refresh needed)  
✅ Create **relationships** between users and project_inspections  
✅ Use **date filters** for inspection_date to narrow down views  
✅ Create **KPI cards** for building_score, fire_life_safety  

---

## 📝 CONNECTION STRING (For Reference)

When Power BI asks, provide:
```
postgresql://postgres:PASSWORD@host.railway.internal:5432/railway?sslmode=require
```

Replace `PASSWORD` with your actual database password from Railway.

---

**Ready to Connect! 🎉 Follow Steps 1-5 above and your Power BI dashboard will show all inspection data.**
