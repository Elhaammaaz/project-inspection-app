# Power BI Integration - API Endpoints & Setup Guide

## 🔗 API Base URL
```
https://web-production-c26d2.up.railway.app
```

## 📊 Available Endpoints for Power BI

### 1. **Inspections Data**
```
GET /api/inspections
```
**Description**: All building inspection records with complete assessment data
**Sample Fields**: project_name, building_score, inspection_result, city, address, etc.
**Use in Power BI**: Main fact table for dashboards

### 2. **Users Data**
```
GET /api/users
```
**Description**: All registered users with access permissions
**Sample Fields**: email, full_name, active, can_view_dashboard, can_view_reports, etc.
**Use in Power BI**: Lookup table for user analysis

### 3. **User Profiles**
```
GET /api/user-profiles
```
**Description**: Extended user profile information
**Sample Fields**: department, job_title, phone, office_location, role, theme, etc.
**Use in Power BI**: Dimension table for user details

### 4. **Inspection Systems**
```
GET /api/inspection-systems
```
**Description**: Individual building systems and components within inspections
**Sample Fields**: system_name, component_name, condition_rating, priority, etc.
**Use in Power BI**: Detail table for system-level analysis

### 5. **Dashboard Access Requests**
```
GET /api/dashboard-access-requests
```
**Description**: Tracking of dashboard access approval requests
**Sample Fields**: status, requested_at, approved_at, approval_reason, etc.
**Use in Power BI**: Audit and tracking table

### 6. **Profile Change Requests**
```
GET /api/profile-change-requests
```
**Description**: User profile update approval workflow
**Sample Fields**: field_name, old_value, new_value, status, etc.
**Use in Power BI**: Change management tracking

---

## 🔐 Authentication & Access

**Authentication Method**: No API Key Required (Currently)
- Direct HTTP access to all endpoints
- If authentication is added later, headers will be needed in Power BI

**Headers to Add (if needed)**:
```
Authorization: Bearer [TOKEN]
Content-Type: application/json
```

---

## 📈 Sample Relationship Diagram

```
┌─────────────────┐
│     Users       │
│  (Dimension)    │
└────────┬────────┘
         │ id
         ↓ user_id
┌─────────────────┐         ┌──────────────────┐
│   Inspections   │────────→│  Inspection      │
│  (Fact Table)   │         │  Systems         │
└─────────────────┘         │  (Details)       │
         ↑                   └──────────────────┘
         │
         │ (relationships)
         │
┌────────────────────┐  ┌─────────────────────┐
│  User Profiles     │  │ Dashboard Access    │
│  (Dimension)       │  │ Requests (Audit)    │
└────────────────────┘  └─────────────────────┘
```

---

## 🚀 Step-by-Step Power BI Setup

### Step 1: Connect to API
1. Open Power BI Desktop
2. Go to **Get Data** → **Web**
3. Enter URL: `https://web-production-c26d2.up.railway.app/api/inspections`
4. Click **OK**

### Step 2: Transform Data
1. Power BI will show you a preview
2. Click **Transform Data** (if needed)
3. Click **Advanced Editor**
4. Replace the query with one from `POWERBI_M_QUERIES_ALL_TABLES.m`
5. Click **Done**

### Step 3: Create Relationships
1. Go to **Model** view
2. Create relationships:
   - `Inspections[user_id]` → `Users[id]`
   - `Inspections[id]` → `InspectionSystems[inspection_id]`
   - `Users[id]` → `UserProfiles[user_id]`

### Step 4: Set Up Refresh
1. Go to **Power Query Editor**
2. Right-click each query → **Refresh**
3. Set schedule: **Power Query Editor** → **Refresh** → **Configure Refresh**
4. Recommended: Every 1-4 hours

### Step 5: Build Dashboard
1. Create visualizations using the imported tables
2. Use filters for user roles, dates, regions, etc.
3. Add slicers for interactivity

---

## 📋 Recommended Visualizations

### For Inspections Table:
- **Card**: Total Building Score Average
- **Map**: GPS coordinates (gps_latitude, gps_longitude)
- **Bar Chart**: Building Score by City
- **Table**: Inspection Results by Project Name
- **Gauge**: High Priority Classified %

### For Users Table:
- **Card**: Active Users Count
- **Pie Chart**: Access Permissions Distribution
- **Table**: Users by Department/Role
- **Column Chart**: Approvals Over Time

### For Inspection Systems:
- **Treemap**: Systems by Condition Rating
- **Table**: Components by Priority
- **Ribbon Chart**: System Performance Over Time

---

## ⚙️ Troubleshooting

### Issue: "Web connection failed"
**Solution**: 
- Check internet connection
- Verify API is running: `https://web-production-c26d2.up.railway.app/health`
- Check firewall/VPN settings

### Issue: "Column not found" errors
**Solution**:
- Verify API schema matches M query fields
- Check API response in browser
- Update field names if needed

### Issue: Slow data loading
**Solution**:
- Add filter parameters to URL: `/api/inspections?limit=1000`
- Load less frequently (change refresh schedule)
- Split into multiple queries by date range

### Issue: Data not refreshing
**Solution**:
- Check Power BI refresh settings
- Verify API is accessible from Power BI server
- Check for query timeout (increase timeout in query settings)

---

## 🔄 Auto-Refresh Configuration

### Desktop Refresh:
1. **File** → **Options and settings** → **Options**
2. **Data Load** → Set refresh interval

### Power BI Service Refresh:
1. **Settings** (gear icon) → **Settings**
2. **Datasets** → Select your dataset
3. **Scheduled refresh** → Enable
4. Set time and frequency

### Recommended Frequency:
- **Hourly**: For real-time dashboards
- **Daily**: For standard reporting
- **Weekly**: For archived data

---

## 📊 Key Metrics to Measure

```
Building Assessment Report KPIs:

1. Average Building Score: AVG(Inspections[building_score])
2. High Priority Buildings: COUNT(Inspections WHERE high_priority_classified = 1)
3. User Access Rate: COUNT(Users WHERE can_view_dashboard = 1) / COUNT(Users)
4. Inspection Completion Rate: COUNT WHERE inspection_result IS NOT NULL / Total
5. Average Building Age: AVG(Inspections[chronological_age])
6. System Health: AVERAGE(InspectionSystems[condition_rating])
```

---

## 💾 Export & Sharing

### Export to Excel:
- Use Power BI's **Export to Excel** feature
- Works with all tables and relationships

### Share Dashboard:
- **Publish** to Power BI Service
- Grant access to team members
- Set refresh schedules on the cloud

### Embed in Web:
- Use Power BI Embedded or iFrame
- Perfect for the Building Assessment Report web app

---

## 🔒 Data Security Notes

- Ensure API credentials are secure
- Use HTTPS (already implemented)
- Set appropriate row-level security (RLS) in Power BI
- Audit access logs regularly
- Refresh sensitive data appropriately

---

## 📞 Support & Documentation

For issues or updates:
1. Check API logs: `/api/health`
2. Review this file for updates
3. Test endpoints manually in browser or Postman
4. Check Power BI documentation for M Language syntax

---

**Last Updated**: January 5, 2026
**API Version**: 1.0
**Power BI Compatibility**: Desktop & Service
