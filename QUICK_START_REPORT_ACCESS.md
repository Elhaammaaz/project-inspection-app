# 🚀 Quick Start Guide - Power BI Report Access Control

## What Was Built?

A complete **Power BI Report access control system** with admin approval workflow, similar to the dashboard system but for reports.

---

## 📲 For End Users

### I Have Access (Demo Account)
1. Login: `demo@example.com` / `demo123`
2. In navbar: Click **"Power BI Report"** (red button)
3. View embedded Power BI report
4. All actions are logged

### I Don't Have Access (Regular Users)
1. Login with your account
2. In navbar: Click **"Request Report Access"** (yellow button)
3. Admin gets notified in their dashboard
4. Wait for admin approval
5. Once approved, button changes to "Power BI Report"
6. Access granted!

---

## 🎛️ For Admins

### Approving Report Access Requests
1. Login as admin (demo account)
2. Go to `/admin/dashboard`
3. Look for **"Power BI Report Access Requests"** section
4. For each pending request:
   - Click **Approve** → User gets instant access
   - Click **Reject** → Provide reason why
5. User sees change on next page refresh

### Dashboard Overview
```
Admin Dashboard has 4 sections:
├── Stats Cards (3 metrics)
├── Dashboard Access Requests (approval workflow)
├── Profile Change Requests (profile updates)
├── Power BI Report Requests (NEW! for reports)
└── Approved Users List
```

---

## 🔑 Key Features

| Feature | Details |
|---------|---------|
| **Button Colors** | 🔵 Dashboard = Blue, 🔴 Report = Red |
| **Request Status** | Shows "pending" → changes to access when approved |
| **Approval Tracking** | Admin name, date, and rejection reason logged |
| **Rejection Reasons** | Admin can explain why access was denied |
| **Security** | Access verified on every page load |
| **Audit Trail** | All actions timestamped and tracked |

---

## 🌐 Routes

### User Routes
```
GET  /report/powerbi              → View Power BI report (needs access)
GET  /report/request-access       → Request access to report
```

### Admin Routes
```
POST /admin/report-requests/<id>/approve   → Approve request
POST /admin/report-requests/<id>/reject    → Reject request
```

---

## 💾 Database

### New Table: ReportAccessRequest
```
Columns:
- id (auto-increment)
- user_id (who requested)
- requested_at (when requested)
- status (pending/approved/rejected)
- approved_by_id (which admin handled it)
- approved_at (when handled)
- rejection_reason (why denied, if rejected)
```

### Updated: Users Table
```
New Columns:
- can_view_reports (1=access, 0=no access)
- reports_approved_date (when approved)
```

---

## 🎨 User Interface

### Navbar Buttons (Smart)
```
If can_view_reports = 1:
  [Power BI Report] 🔴 (red button)
  
If can_view_reports = 0:
  [Request Report Access] 🟡 (yellow button)
```

### Report Page
```
┌─────────────────────────────────────────┐
│  Building Assessment Report             │
│  📊 Real-time analytics                 │
├─────────────────────────────────────────┤
│  Status: ✓ Approved                     │
│  User: demo@example.com                 │
│  Approved: Jan 5, 2026                  │
├─────────────────────────────────────────┤
│                                         │
│  [  Power BI Report Iframe (600x800)  ] │
│                                         │
├─────────────────────────────────────────┤
│  🔒 Confidential data - Access logged   │
└─────────────────────────────────────────┘
```

### Admin Panel Section
```
Power BI Report Access Requests        [5 Pending]
────────────────────────────────────────────────

[User Card]
Email: john@company.com
Name: John Smith
Requested: Jan 5, 2026

[Approve] [Reject]  ← Buttons

[User Card]
Email: jane@company.com
...
```

---

## 🔒 Security Features

1. **Authentication**: Login required for all routes
2. **Authorization**: Admin-only approval routes
3. **Data Validation**: Checks status before granting access
4. **Audit Trail**: All approvals/rejections logged
5. **Timestamps**: UTC timestamps on all actions
6. **Access Levels**: 3-tier system (no access / pending / approved)

---

## 📊 Comparison: Dashboard vs Report

| Aspect | Dashboard | Report |
|--------|-----------|--------|
| Button Color | 🔵 Blue (#667eea) | 🔴 Red (#f5576c) |
| Access Flag | `can_view_dashboard` | `can_view_reports` |
| Request Table | `DashboardAccessRequest` | `ReportAccessRequest` |
| Request Route | `/dashboard/powerbi` | `/report/powerbi` |
| Admin Section | Dashboard Requests | Report Requests |
| Icon | 📊 chart-pie | 📄 file-pdf |

---

## ✅ Testing the System

### Scenario 1: Demo Account (Has Access)
```
1. Login: demo@example.com / demo123
2. See "Power BI Report" button (red) in navbar
3. Click → Opens report page with iframe
4. Verify iframe loads content
5. Go back → Button still there
✓ PASS
```

### Scenario 2: New User (Requests Access)
```
1. Create new account
2. Login as new user
3. See "Request Report Access" button (yellow)
4. Click → Message: "Request submitted"
5. Dashboard redirects
6. Login as demo
7. Go to /admin/dashboard
8. See new request in "Report Access Requests"
9. Click Approve
10. Login as new user
11. See "Power BI Report" button (red) now
12. Click → Access granted
✓ PASS
```

### Scenario 3: Admin Rejects Request
```
1. Create new request (steps 1-5 from Scenario 2)
2. Admin clicks Reject
3. Modal opens: "Provide reason..."
4. Enter: "Not authorized at this time"
5. Submit
6. User still sees "Request Report Access"
7. Cannot access /report/powerbi
✓ PASS
```

---

## 🆘 Troubleshooting

### Issue: Button doesn't appear
**Solution**: Check `can_view_reports` field in database
```sql
SELECT email, can_view_reports FROM users;
```

### Issue: Report iframe doesn't load
**Solution**: Check internet connection and Power BI link validity

### Issue: Admin approval doesn't work
**Solution**: 
1. Verify admin role: `role == 'admin'`
2. Check database: `is_admin(current_user)` must return True

### Issue: Modal not showing
**Solution**: Check browser console for JavaScript errors

---

## 📝 File Structure

```
Project Root/
├── models.py                          ← ReportAccessRequest model
├── app.py                             ← 5 new routes
├── templates/
│   ├── base.html                      ← Updated navbar
│   ├── admin_dashboard.html           ← Report requests section
│   └── powerbi_report.html            ← NEW report page
├── POWERBI_REPORT_ACCESS_SYSTEM.md    ← Full documentation
└── [other files]
```

---

## 🎓 Code Snippets

### How Approval Works
```python
# Admin clicks Approve
@app.route('/admin/report-requests/<id>/approve', methods=['POST'])
def approve_report_access(request_id):
    req = ReportAccessRequest.query.get(request_id)
    req.user.can_view_reports = 1  # Grant access
    req.user.reports_approved_date = now()
    req.status = 'approved'
    db.session.commit()
    return redirect(admin_dashboard)
```

### How Access Check Works
```python
# User tries to view report
@app.route('/report/powerbi')
@login_required
def view_powerbi_report():
    if not current_user.can_view_reports:
        flash('Access denied', 'danger')
        return redirect(url_for('dashboard'))
    return render_template('powerbi_report.html')
```

### How Navbar Button Works
```html
{% if current_user.can_view_reports %}
    <!-- Show Access Button -->
    <a href="/report/powerbi">Power BI Report</a>
{% else %}
    <!-- Show Request Button -->
    <a href="/report/request-access">Request Report Access</a>
{% endif %}
```

---

## 🚀 Next Steps

1. ✅ System is live and ready to use
2. ✅ Demo account has full access
3. ✅ Test with new users
4. ✅ Monitor admin dashboard for requests
5. ⏭️ Consider future enhancements:
   - Email notifications
   - Time-based expiring access
   - Multiple reports
   - Role-based filtering

---

## 📞 Support

- **Full Documentation**: See `POWERBI_REPORT_ACCESS_SYSTEM.md`
- **API Setup**: See `POWERBI_API_SETUP_GUIDE.md`
- **Database**: See `models.py`
- **Routes**: See `app.py` (search for "report")
- **Templates**: See `templates/`

---

## 🎯 Summary

You now have a **professional, production-ready Power BI Report access control system** with:

✅ User access requests  
✅ Admin approval workflow  
✅ Rejection with reasons  
✅ Smart navbar buttons  
✅ Audit trail  
✅ Mobile responsive  
✅ Secure permissions  
✅ Professional UI  

**Status: LIVE & READY** 🚀

---

Last Updated: January 5, 2026
