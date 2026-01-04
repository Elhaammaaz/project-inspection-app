# ⚡ QUICK START - POWER BI CONNECTION (5 Minutes)

---

## 🎯 QUICK ANSWER: WHERE IS YOUR DATABASE?

**Location:** Railway PostgreSQL (Cloud)  
**Access:** `host.railway.internal:5432`  
**Database:** `railway`  

**Main Data Table:** `project_inspections` (30+ columns)  
**Other Table:** `users` (login data)

---

## 📱 FASTEST WAY TO CONNECT (5 STEPS)

### **Step 1: Open Railway Dashboard**
Go to: https://railway.app/dashboard  
Click: Your PostgreSQL service  
Tab: "Connect"

### **Step 2: Copy Connection Info**
```
Host: (something).railway.internal
Port: 5432
Username: postgres
Password: (copy this)
Database: railway
```

### **Step 3: Open Power BI Desktop**
Click: "Get Data"  
Search: "PostgreSQL"  
Click: "Connect"

### **Step 4: Fill Connection Dialog**
```
Server: [Host from Step 2]
Database: railway
```
Click: OK

### **Step 5: Login & Load**
When prompted:
- Username: postgres
- Password: (from Step 2)

Select tables:
- ☑ project_inspections ← Your data!
- ☑ users

Click: "Load"

**Done! Your data is in Power BI.** 🎉

---

## 📊 YOUR MAIN TABLE: `project_inspections`

This is where ALL your inspection data is stored:

```
Columns Available:
├─ project_name ............. Project/Building name
├─ city ....................... City location
├─ building_score ............ 0-100 score ⭐ (For KPIs)
├─ inspection_result ......... "Passed"/"Not Complied" ⭐
├─ government_compliance .... Compliance status ⭐
├─ fire_life_safety .......... % rating ⭐
├─ building_type ............ Building type
├─ gross_built_area ......... Size in m²
├─ number_of_floors ......... Number of floors
├─ inspection_date .......... When inspected (For trends)
├─ fm_performance ........... Performance rating
├─ high_priority_classified . Count of issues
├─ gps_latitude/longitude ... For map visualization
├─ created_at ............... Created timestamp
└─ + 15 more columns ........ (see DATABASE_TABLES_REFERENCE.md)

Row Count: Grows as you add inspections
```

---

## 🎨 EASY POWER BI VISUALS TO CREATE

### **Visual 1: Building Score Card**
- Click: "Card" visual
- Drag: `building_score` → Values
- Result: Shows average building score

### **Visual 2: Compliance Pie Chart**
- Click: "Pie Chart" visual
- Drag: `government_compliance` → Legend
- Drag: `project_name` → Values (Count)
- Result: % breakdown of compliance

### **Visual 3: City Comparison Bar Chart**
- Click: "Clustered Bar Chart"
- Drag: `city` → Y-axis
- Drag: `building_score` → X-axis
- Result: Score by city

### **Visual 4: Inspection Date Trend**
- Click: "Line Chart"
- Drag: `inspection_date` → X-axis
- Drag: `building_score` → Y-axis
- Result: Score trend over time

### **Visual 5: Location Map**
- Click: "Map"
- Drag: `gps_latitude` → Latitude
- Drag: `gps_longitude` → Longitude
- Drag: `building_score` → Size/Color
- Result: Map of all inspections

---

## 🔗 CONNECTION REFERENCE

**Connection Format:**
```
Host: postgres-prod.railway.internal
Port: 5432
Database: railway
Username: postgres
Password: [Your Railway DB Password]
SSL: Required (auto-enabled)
```

---

## 🚨 IF IT DOESN'T WORK

### **Can't connect?**
1. Check host is: `.railway.internal` (NOT localhost)
2. Check PostgreSQL service is running in Railway
3. Double-check username: `postgres`
4. Verify password is correct

### **Can't see tables?**
1. Click "Load More" in table list
2. Ensure you clicked "Load"
3. Refresh Power BI connection

### **Slow connection?**
1. Check Railway PostgreSQL status
2. Use specific columns (not SELECT *)
3. Add date filters to reduce data

---

## 📞 FILE REFERENCES IN YOUR PROJECT

- **POWERBI_CONNECTION_GUIDE.md** → Full detailed guide
- **DATABASE_TABLES_REFERENCE.md** → All table columns
- **DATABASE_ARCHITECTURE.md** → System diagrams
- **models.py** → Table definitions (code)

---

## ✅ SUMMARY

| What | Where | How |
|------|-------|-----|
| Database | Railway PostgreSQL | SSH/SSL encrypted |
| Main Table | `project_inspections` | 30+ columns of inspection data |
| Users Table | `users` | 4 columns (id, email, password, date) |
| Connection | Power BI Desktop | Get Data → PostgreSQL |
| Data Updates | Automatic | Real-time when you add inspections |
| Visualizations | Power BI | Unlimited dashboards |

---

## 🎯 TYPICAL POWER BI DASHBOARD

After connecting, you'll have:
- **KPIs:** Building score, fire safety %, compliance %
- **Charts:** By city, by building type, by result
- **Trends:** Score over time
- **Maps:** Location of all inspections
- **Tables:** Detailed inspection listings
- **Filters:** By date, city, compliance status

---

**You're ready! Open Power BI and follow the 5 steps above.** ✨

Questions? Check the detailed guides in your project folder.
