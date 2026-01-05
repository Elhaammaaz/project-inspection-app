# Power BI Dashboard Design - Building Inspection System
**Single Page - Main KPIs Dashboard**

---

## DASHBOARD LAYOUT & VISUALS

### **ROW 1: KEY METRICS (5 Card Visuals)**

#### **Card 1: Total Inspections**
- **Visual Type:** Card
- **Column:** `project_inspections[id]` (COUNTA)
- **DAX Measure:**
```dax
Total Inspections = COUNTA('project_inspections'[id])
```
- **Format:** Large number, Blue color

#### **Card 2: Average Building Score**
- **Visual Type:** Card
- **Column:** `project_inspections[building_score]`
- **DAX Measure:**
```dax
Avg Building Score = AVERAGE('project_inspections'[building_score])
```
- **Format:** Decimal (1), Green color, % symbol

#### **Card 3: High Priority Projects**
- **Visual Type:** Card
- **Column:** `project_inspections[high_priority_classified]`
- **DAX Measure:**
```dax
High Priority Count = CALCULATE(COUNTA('project_inspections'[id]), 'project_inspections'[high_priority_classified] = 1)
```
- **Format:** Red color (warning)

#### **Card 4: Completed Inspections**
- **Visual Type:** Card
- **Column:** `project_inspections[inspection_status]`
- **DAX Measure:**
```dax
Completed Inspections = CALCULATE(COUNTA('project_inspections'[id]), 'project_inspections'[inspection_status] = "completed")
```
- **Format:** Purple color

#### **Card 5: Average FM Performance**
- **Visual Type:** Card
- **Column:** `project_inspections[fm_performance]`
- **DAX Measure:**
```dax
Avg FM Performance = AVERAGE('project_inspections'[fm_performance])
```
- **Format:** Yellow color, % symbol

---

### **ROW 2: INSPECTION STATUS & COMPLIANCE**

#### **Visual 6: Inspection Status Distribution (Donut Chart)**
- **Type:** Donut Chart
- **Legend:** `project_inspections[inspection_status]` (draft, completed, reviewed)
- **Values:** COUNTA of `project_inspections[id]`
- **Size:** 30% width
- **Colors:** 
  - Draft: Gray
  - Completed: Green
  - Reviewed: Blue

#### **Visual 7: Government Compliance Status (Stacked Bar)**
- **Type:** Stacked Bar Chart
- **Axis:** `project_inspections[government_compliance]` (YES/NO/PENDING)
- **Value:** COUNTA of `project_inspections[id]`
- **Size:** 35% width
- **Show data labels**

#### **Visual 8: Building Score by Inspection Result (Clustered Column)**
- **Type:** Clustered Column Chart
- **Axis:** `project_inspections[inspection_result]`
- **Value:** AVG of `project_inspections[building_score]`
- **Size:** 35% width
- **DAX Measure:**
```dax
Avg Score by Result = AVERAGE('project_inspections'[building_score])
```

---

### **ROW 3: SYSTEM PERFORMANCE**

#### **Visual 9: Top 10 Building Systems Performance (Horizontal Bar)**
- **Type:** Horizontal Bar Chart
- **Axis:** `inspection_systems[system_name]` (Top 10)
- **Value:** AVG of `inspection_systems[score_percentage]`
- **Size:** 50% width
- **Sort:** Descending by score
- **DAX Measure:**
```dax
Avg System Score = AVERAGE('inspection_systems'[score_percentage])
```

#### **Visual 10: System Performance Summary (Table)**
- **Type:** Matrix/Table
- **Rows:** `inspection_systems[system_name]`
- **Values:**
  - Count of systems
  - Average score_percentage
  - Average weight
  - Average weighted_score
- **Size:** 50% width
- **Conditional Formatting:** Score color scale (Red: <50, Yellow: 50-75, Green: >75)

---

### **ROW 4: BUILDING AGE ANALYTICS & PERFORMANCE TREND**

#### **Visual 11: Chronological Age vs Remaining Life (Scatter Plot)**
- **Type:** Scatter Chart
- **X-Axis:** `project_inspections[chronological_age]`
- **Y-Axis:** `project_inspections[estimated_remaining_life]`
- **Size:** `project_inspections[building_score]` (bubble size)
- **Legend:** `project_inspections[building_type]`
- **Size:** 50% width
- **DAX Measure:**
```dax
Life Expectancy Ratio = DIVIDE(
    [Avg Remaining Life], 
    [Avg Chronological Age], 
    0
)
```

#### **Visual 12: FM Performance Trend (Line Chart)**
- **Type:** Line Chart with Markers
- **Axis:** `project_inspections[created_at]` (grouped by Month)
- **Value:** AVG of `project_inspections[fm_performance]`
- **Size:** 50% width
- **Include forecast:** Optional (3 months)

---

### **ROW 5: DETAILED METRICS TABLE**

#### **Visual 13: Project Details with Key Metrics (Matrix/Table)**
- **Type:** Matrix Table
- **Rows:** 
  - `project_inspections[project_name]`
  - `project_inspections[city]`
- **Values:**
  - `building_score`
  - `fm_performance`
  - `inspection_status`
  - `government_compliance`
  - `fire_life_safety`
  - `inspection_result`
- **Size:** 100% width
- **Conditional Formatting:**
  - Building Score: Green/Yellow/Red gradient
  - Status: Icon set or color coding

---

## DAX MEASURES (Copy-Paste Ready)

### **Performance Metrics**
```dax
// Total Inspections
Total Inspections = COUNTA('project_inspections'[id])

// Average Building Score
Avg Building Score = AVERAGE('project_inspections'[building_score])

// High Priority Count
High Priority Count = CALCULATE(
    COUNTA('project_inspections'[id]), 
    'project_inspections'[high_priority_classified] = 1
)

// Completed Inspections
Completed Inspections = CALCULATE(
    COUNTA('project_inspections'[id]), 
    'project_inspections'[inspection_status] = "completed"
)

// Average FM Performance
Avg FM Performance = AVERAGE('project_inspections'[fm_performance])

// Completion Rate %
Completion Rate = DIVIDE(
    [Completed Inspections],
    [Total Inspections],
    0
)

// Average System Score
Avg System Score = AVERAGE('inspection_systems'[score_percentage])

// High Priority %
High Priority % = DIVIDE(
    [High Priority Count],
    [Total Inspections],
    0
)

// Average Chronological Age
Avg Chronological Age = AVERAGE('project_inspections'[chronological_age])

// Average Remaining Life
Avg Remaining Life = AVERAGE('project_inspections'[estimated_remaining_life])

// Life Expectancy Ratio
Life Expectancy Ratio = DIVIDE(
    [Avg Remaining Life],
    [Avg Chronological Age],
    0
)

// Government Compliance Count
Compliant Projects = CALCULATE(
    COUNTA('project_inspections'[id]),
    'project_inspections'[government_compliance] = "YES"
)

// Compliance Rate %
Compliance Rate = DIVIDE(
    [Compliant Projects],
    [Total Inspections],
    0
)

// Average Fire & Life Safety Score
Avg Fire Safety = AVERAGE('project_inspections'[fire_life_safety])

// Average Gross Built Area
Avg Built Area = AVERAGE('project_inspections'[gross_built_area])

// Total Users
Total Users = COUNTA('users'[id])

// Active Users
Active Users = CALCULATE(
    COUNTA('users'[id]),
    'users'[active] = 1
)

// Systems Requiring Attention (Score < 60)
Systems At Risk = CALCULATE(
    COUNTA('inspection_systems'[id]),
    'inspection_systems'[score_percentage] < 60
)

// Average Weight Distribution
Avg System Weight = AVERAGE('inspection_systems'[weight])

// Total Weighted Score
Total Weighted Score = SUM('inspection_systems'[weighted_score])
```

---

## SLICERS (Top of Page)

Add these slicers for interactivity:

1. **Slicer 1: Project Name** 
   - Column: `project_inspections[project_name]`
   - Type: Dropdown (vertical list)
   - Size: 20% width

2. **Slicer 2: City**
   - Column: `project_inspections[city]`
   - Type: Dropdown
   - Size: 15% width

3. **Slicer 3: Building Type**
   - Column: `project_inspections[building_type]`
   - Type: Dropdown
   - Size: 15% width

4. **Slicer 4: Inspection Status**
   - Column: `project_inspections[inspection_status]`
   - Type: Buttons (draft | completed | reviewed)
   - Size: 20% width

5. **Slicer 5: Date Range**
   - Column: `project_inspections[inspection_date]`
   - Type: Between (date range picker)
   - Size: 30% width

---

## DASHBOARD STRUCTURE

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SLICERS: Project | City | Building Type | Status | Date Range        │
├─────────────────────────────────────────────────────────────────────────┤
│ │Total │ Avg Score │ High Priority │ Completed │ FM Performance      │
│ │Insp  │    (%)    │     Count     │ Insp      │      (%)             │
├─────────────────────────────────────────────────────────────────────────┤
│ │Status Distribution    │ Compliance Status      │ Avg Score by Result     │
│ │(Donut - 30%)         │ (Stacked Bar - 35%)    │ (Column - 35%)         │
├─────────────────────────────────────────────────────────────────────────┤
│ │Top 10 Systems (Horiz Bar - 50%)  │ System Summary Table (50%)        │
├─────────────────────────────────────────────────────────────────────────┤
│ │Age vs Remaining Life (Scatter - 50%) │ FM Performance Trend (50%)     │
├─────────────────────────────────────────────────────────────────────────┤
│ │Project Details Table (100%)                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## COLOR SCHEME

- **Primary:** Dark Blue (#1f77b4)
- **Success:** Green (#2ca02c) - Good scores >75
- **Warning:** Yellow (#ff7f0e) - Medium scores 50-75
- **Critical:** Red (#d62728) - Poor scores <50
- **Neutral:** Gray (#7f7f7f) - Draft/pending status
- **Background:** Light Gray (#f0f0f0)

---

## CONDITIONAL FORMATTING RULES

### **Building Score Column (Table)**
- Value < 50: Red background, white text
- Value 50-70: Yellow background, dark text
- Value > 70: Green background, white text

### **Inspection Status Column (Table)**
- "draft": Gray badge
- "completed": Green badge
- "reviewed": Blue badge

### **FM Performance Column (Table)**
- Value < 60: Red
- Value 60-75: Yellow
- Value > 75: Green

---

## KEY INSIGHTS TO HIGHLIGHT

1. **Overall Health Score** - Average building_score across all projects
2. **At-Risk Systems** - Count of systems scoring < 60%
3. **Compliance Gap** - Projects without government approval
4. **Age Distribution** - Compare chronological_age vs estimated_remaining_life
5. **Performance Leaders** - Top 3 systems by average score
6. **Bottlenecks** - Most common inspection_result status

---

## TIPS FOR POWER BI

✅ Use format painter for consistent styling  
✅ Set interaction filters between visuals  
✅ Use drill-through on project names → system details  
✅ Add bookmarks for "High Priority View" and "Compliance View"  
✅ Use RLS (Row-Level Security) to show users only their projects  
✅ Schedule refresh every 6 hours for real-time updates  
✅ Add tooltips with calculated measures for deeper insight  
✅ Use sparklines in tables for trend visualization
