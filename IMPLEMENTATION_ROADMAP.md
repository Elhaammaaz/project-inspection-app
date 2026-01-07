# Production Implementation Roadmap - BCAR Web Application

**Status:** Phase 1 - Core Engine Complete | Phase 2 - Starting Now  
**Last Updated:** January 6, 2026  
**Target Completion:** 2 weeks to production-ready

---

## ✅ COMPLETED IN PHASE 1

### Authentication & User Management
- [x] User registration with email validation
- [x] Secure login (bcrypt hashing via Werkzeug)
- [x] Session management (Flask-Login)
- [x] CSRF protection enabled
- [x] Demo account for testing

### Core Data Models (8 tables)
- [x] User (with password hashing)
- [x] Project (building/assessment record)
- [x] AssessmentItem (inspection items)
- [x] ComplianceItem (regulatory requirements)
- [x] TestRecord (testing activities)
- [x] CAPARecord (corrective actions)
- [x] SystemWeight (scoring weights)
- [x] LookupTable (reference data)

### Frontend Templates & Routes
- [x] Login/Register pages
- [x] Dashboard with 4 main sections
- [x] Projects list page
- [x] Inspections/Building Assessment form
- [x] Systems & Compliance Checklist page
- [x] Reports & Analytics page (3 tabs)
- [x] All CRUD routes (create, read, update)
- [x] Search & filter by system/status/priority

### Business Calculations Engine ✅ TESTED
- [x] Item score calculation: Rate/5 * 100
- [x] Weighted score: Score% * Weight / 100
- [x] System-level aggregation (avg scores)
- [x] Overall project score (compliance %)
- [x] Status distribution counts (Open/In Progress/Closed/Verified)
- [x] Priority distribution (P1/P2/P3/P4)
- [x] Risk level classification (Critical/High/Medium/Low/Acceptable)
- [x] Risk distribution counts
- [x] Test results summarization
- [x] CAPA status counting
- [x] Compliance item status counting

**Test Results:**
```
Sample data (5 items across 3 systems):
- Overall Score: 76.0% ✓
- Compliance %: 80.0% ✓
- Status Counts: 5 Open ✓
- Priority Distribution: 5 P3 ✓
- Risk Distribution: 0 Critical, 1 High, 1 Medium, 1 Low, 2 Acceptable ✓
- Systems Detected: Fire_LifeSafety, Electrical, HVAC ✓
```

### Data Integration
- [x] Excel file analyzed (7 sheets)
- [x] Data mapped to models
- [x] Reference data structure identified
- [x] Sample data import started

---

## 🚀 PHASE 2: Production Features (This Week)

### 2.1 PostgreSQL Migration (Priority: HIGH)
**Current:** SQLite (development only)  
**Target:** PostgreSQL with connection pooling  
**Tasks:**
- [ ] Add PostgreSQL driver (psycopg2 already installed)
- [ ] Create production config with DATABASE_URL
- [ ] Add connection pooling (SQLAlchemy pool_size, max_overflow)
- [ ] Create migration script (SQLite → PostgreSQL)
- [ ] Test data integrity post-migration
- [ ] Add backup procedures

**Implementation Time:** 2 hours

### 2.2 Comprehensive Data Seeding (Priority: HIGH)
**Current:** Manual form entry only  
**Target:** Auto-populate all reference data from Excel  
**Tasks:**
- [ ] Extract all Systems from Excel (21+ systems)
- [ ] Extract Subsystems per system
- [ ] Extract Components per subsystem
- [ ] Extract all 694 Assessment Items from "Building Assessment" sheet
- [ ] Extract Government Compliance requirements from "Government Compliance Checklist"
- [ ] Extract Test templates from "Test Register" sheet
- [ ] Extract CAPA templates from "CAPA Register" sheet
- [ ] Create seeding script to populate LookupTable
- [ ] Create seed data fixtures for testing

**Implementation Time:** 4 hours

### 2.3 Role-Based Access Control (Priority: HIGH)
**Current:** Single user (owner) level  
**Target:** 4 role levels with row-level security  
**Schema additions needed:**

```sql
-- New tables
CREATE TABLE roles (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE permissions (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE role_permissions (
    role_id INTEGER FOREIGN KEY references roles,
    permission_id INTEGER FOREIGN KEY references permissions,
    PRIMARY KEY (role_id, permission_id)
);

ALTER TABLE users ADD COLUMN role_id INTEGER FOREIGN KEY references roles;

CREATE TABLE project_access (
    id INTEGER PRIMARY KEY,
    user_id INTEGER FOREIGN KEY references users,
    project_id INTEGER FOREIGN KEY references projects,
    role_id INTEGER FOREIGN KEY references roles,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, project_id)
);
```

**Roles:**
1. **Admin** - Full system access, user management, all projects
2. **Project Manager** - Create/manage projects, assign teams
3. **Assessor** - Create/edit assessment data, enter field data
4. **Reviewer** - View/approve assessments, can't edit
5. **Auditor** (read-only) - View all, audit trails

**Implementation Time:** 6 hours

---

## 📊 PHASE 3: Executive Dashboard & Analytics (Next Week)

### 3.1 Dynamic Dashboard (Priority: HIGH)
**Current:** Static hardcoded data  
**Needed:**
- [ ] Real-time KPI cards (calculated from data)
- [ ] Chart: Compliance % by system (bar chart)
- [ ] Chart: Risk distribution (pie chart)
- [ ] Chart: Status breakdown (donut chart)
- [ ] Chart: CAPA completion trend (line chart)
- [ ] Alerts for: Critical items, Overdue CAPAs, Non-compliant systems
- [ ] Executive summary PDF export

**Implementation Time:** 8 hours

### 3.2 Advanced Search & Filters (Priority: MEDIUM)
**Current:** Basic system/status/priority filters  
**Needed:**
- [ ] Full-text search (item code, description, remarks)
- [ ] Date range filters (inspection, due, created)
- [ ] Multi-select filters with AND/OR logic
- [ ] Saved filter presets per user
- [ ] Export filtered results (Excel, PDF, CSV)
- [ ] Advanced search interface with autocomplete

**Implementation Time:** 5 hours

### 3.3 Audit Trail System (Priority: MEDIUM)
**Needed:**
- [ ] AuditLog model (what changed, who changed it, when, why)
- [ ] Auto-tracking on all AssessmentItem changes
- [ ] Change history view per item
- [ ] Audit report generation
- [ ] Database triggers for compliance

**Implementation Time:** 4 hours

---

## 🔐 PHASE 4: Security & Validation (End of Week 2)

### 4.1 Business Rule Validation (Priority: HIGH)
**Needed:**
- [ ] No invalid system/subsystem/component combinations
- [ ] Required fields per status
- [ ] Can't close item without evidence reference
- [ ] Can't mark as compliant without test evidence
- [ ] CAPA required if item score < 50%
- [ ] Due date must be future date
- [ ] Test result must link to valid assessment item

**Implementation Time:** 3 hours

### 4.2 Input Sanitization & SQL Injection Prevention (Priority: CRITICAL)
- [x] SQLAlchemy parameterized queries (already in place)
- [ ] Form validation on all inputs
- [ ] File upload validation (if applicable)
- [ ] Rate limiting on API endpoints
- [ ] CORS configuration

**Implementation Time:** 2 hours

### 4.3 Testing Suite (Priority: HIGH)
**Needed:**
- [ ] Unit tests for all calculation functions
- [ ] Integration tests for workflows
- [ ] Database constraint tests
- [ ] API endpoint tests
- [ ] UI end-to-end tests
- [ ] Security penetration testing

**Implementation Time:** 8 hours

---

## 📝 PHASE 5: Documentation & Deployment (Week 2 End)

### 5.1 Documentation (Priority: HIGH)
- [ ] README with setup instructions
- [ ] Architecture diagram (ER diagram)
- [ ] API documentation (endpoints, request/response)
- [ ] Database schema documentation
- [ ] Deployment guide (Docker, production server)
- [ ] User guide (how to use the app)
- [ ] Admin guide (configuration, backups)

**Implementation Time:** 6 hours

### 5.2 Deployment Preparation (Priority: HIGH)
- [ ] Docker containerization
- [ ] Environment configuration (dev/staging/prod)
- [ ] Database backup automation
- [ ] Logging system setup
- [ ] Monitoring/alerting
- [ ] CI/CD pipeline (GitHub Actions)

**Implementation Time:** 8 hours

---

## 📈 SUCCESS METRICS

| Metric | Target | Status |
|--------|--------|--------|
| Data completeness | 100% of Excel data imported | Starting |
| Calculation accuracy | ±0.1% vs Excel formulas | ✅ Verified |
| Response time | < 500ms for dashboard | TBD |
| Uptime | 99.9% | TBD |
| Security | 0 SQL injection vulnerabilities | Testing |
| Test coverage | > 90% | Starting |
| User satisfaction | > 4.5/5 rating | Pending |

---

## 🛠️ TECH STACK (FINAL)

**Backend:**
- Flask 2.3.3
- PostgreSQL (production)
- SQLAlchemy 3.0.5 (ORM)
- Flask-Login (auth)
- Flask-WTF (forms)
- psycopg2 (PostgreSQL driver)

**Frontend:**
- Bootstrap 5 (responsive UI)
- Chart.js or Plotly (dashboards)
- jQuery or Alpine.js (interactivity)
- Font Awesome (icons)

**DevOps:**
- Docker (containerization)
- GitHub Actions (CI/CD)
- PostgreSQL backups
- Nginx (reverse proxy)

**Testing:**
- pytest (unit tests)
- coverage (code coverage)
- Selenium (end-to-end tests)
- Postman (API testing)

---

## 📋 DAILY CHECKLIST

### Day 1 (Today)
- [x] Audit current implementation (40% complete)
- [x] Implement calculation engine ✅
- [x] Test calculations with sample data ✅
- [ ] PostgreSQL setup

### Day 2
- [ ] Complete PostgreSQL migration
- [ ] Data seeding script
- [ ] RBAC implementation (part 1)

### Day 3
- [ ] RBAC completion
- [ ] Audit trail system
- [ ] Search & filtering

### Day 4-5
- [ ] Dashboard KPI implementation
- [ ] Charts & visualizations
- [ ] Executive reports

### Day 6-7
- [ ] Testing suite
- [ ] Documentation
- [ ] Security hardening

### Day 8-10
- [ ] Deployment preparation
- [ ] Final integration tests
- [ ] Performance optimization
- [ ] Go-live readiness

---

## 🎯 NEXT IMMEDIATE ACTIONS

**Priority 1 (Do Now):**
1. Switch to PostgreSQL (create production DB)
2. Implement RBAC (users can have roles)
3. Seed all reference data from Excel

**Priority 2 (This Week):**
1. Build executive dashboard
2. Implement audit trail
3. Add comprehensive validation

**Priority 3 (Polish):**
1. Create test suite
2. Write documentation
3. Deploy to production

---

**Lead:** Senior Full-Stack Engineer  
**Architecture:** Clean separation of concerns  
**Design Pattern:** MVC + Service layer  
**Goal:** Production-quality code ready for BI integration
